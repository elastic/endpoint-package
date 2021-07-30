ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
# we are intentionally pinning the ECS version here, when ecs releases a new version 
# we'll discuss whether we need to release a new package and bump the version here
ECS_GIT_REF ?= v1.10.0

# This variable specifies to location of the package-storage repo. It is used for automatically creating a PR
# to release a new endpoint package. This can be overridden with the location on your file system using the config.mk
# file.
PACKAGE_STORAGE_REPO ?= $(ROOT_DIR)/../package-storage

ifeq (, $(shell which pipenv))
    $(error No pipenv in $(PATH), please install pipenv (brew install pipenv))
endif

# the config.mk file can be used to override variables in the Makefile
ifneq (,$(wildcard $(ROOT_DIR)/config.mk))
    $(info loading $(ROOT_DIR)/config.mk file)
    include $(ROOT_DIR)/config.mk
endif

# the ecs repo will be cloned in the out directory unless this is already set and exists at the specified path
ECS_DIR ?= $(ROOT_DIR)/out/ecs
REAL_ECS_DIR := $(abspath $(ECS_DIR))
$(info ecs dir: $(REAL_ECS_DIR))
$(info ecs git ref: $(ECS_GIT_REF))

SED := sed
PACKAGES_DIR := $(ROOT_DIR)/out/packages
# Default location for packages, this will be used in conjunction with the package defined in this repo
CUST_SCHEMA_DIR := $(ROOT_DIR)/custom_schemas
SUB_TOP_DIR := $(ROOT_DIR)/custom_subsets
SUB_ROOT_DIR := $(SUB_TOP_DIR)/elastic_endpoint
SUB_EVENTS_DIR := $(SUB_TOP_DIR)/elastic_endpoint/events
SUB_METADATA_DIR := $(SUB_TOP_DIR)/elastic_endpoint/metadata
EVENT_SCHEMA_GEN := $(ROOT_DIR)/scripts/event_schema_generator
EXCEPTION_LIST_GEN := $(ROOT_DIR)/scripts/exceptions
GO_TOOLS := $(ROOT_DIR)/scripts/go-tools/bin
SUB_DIRS := $(sort $(dir $(wildcard $(SUB_ROOT_DIR)/*/)))

# Get the package version from the manifest file
get_pack_version = $(shell awk '/^version: /{print $$2}' $(ROOT_DIR)/package/endpoint/manifest.yml)
PACKAGE_VERSION := $(call get_pack_version)

# Given a path this returns the directory (e.g. events, metadata)
schema_name = $(shell basename $(1))
package_file = $(ROOT_DIR)/out/$(1)/generated/beats/fields.ecs.yml
TARGETS := $(foreach schema_dir,$(SUB_DIRS),$(call schema_name,$(schema_dir))-target)

# Parameters
# 1: path to subset specific ecs output files
define gen_exception_files
	cd $(EXCEPTION_LIST_GEN) && pipenv run python main.py \
		$(ROOT_DIR)/out/$(1)
endef

# Parameters
# 1: schema name (e.g. events, metadata)
define gen_mapping_files
	cd $(REAL_ECS_DIR) && pipenv run python scripts/generator.py \
		--out $(ROOT_DIR)/out/$(1) \
		--include $(CUST_SCHEMA_DIR) \
		--ref $(ECS_GIT_REF) \
		--subset $(SUB_ROOT_DIR)/$(1)/*
	$(call gen_exception_files,$(1))
	# remove the first 8 lines
	$(SED) -i $(call package_file,$(1)) -e '1,8d'
	# remove indentation
	$(SED) -i $(call package_file,$(1)) -e 's/^  //g'
	mkdir -p $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/beats $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/ecs $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/elasticsearch $(ROOT_DIR)/generated/$(1)

	# move the generated ecs file directly to the package
	mv $(ROOT_DIR)/generated/$(1)/beats/fields.ecs.yml $(ROOT_DIR)/package/endpoint/data_stream/$(1)/fields/fields.yml
	rm -r $(ROOT_DIR)/generated/$(1)/beats

	# remove unused files
	rm -r $(ROOT_DIR)/generated/$(1)/elasticsearch/6
	rm $(ROOT_DIR)/generated/$(1)/ecs/ecs_nested.yml
	rm $(ROOT_DIR)/generated/$(1)/ecs/subset/*/ecs_nested.yml
endef

# Parameters
# 1: schema name (e.g. events, metadata)
define gen_schema_files
	mkdir -p $(ROOT_DIR)/schemas/v1/$(1)
	cd $(EVENT_SCHEMA_GEN) && pipenv run python main.py \
		--out-schema-dir $(ROOT_DIR)/schemas/v1/$(1) \
		--ecs_git_ref $(ECS_GIT_REF) \
		$(REAL_ECS_DIR) \
		$(CUST_SCHEMA_DIR) \
		$(SUB_ROOT_DIR)/$(1)/*.yaml \
		$(SUB_ROOT_DIR)/$(1)/*.yml \
		$(ROOT_DIR)/out/schema/$(1)
endef

ifeq ($(shell uname -s), Darwin)
ifeq (, $(shell which gsed))
# add mac gsed install target
# mac's freebsd sed command doesn't accept the same parameters as linux
all: mac-deps
endif
SED := gsed
endif

.PHONY: all
all: setup-tools
	$(MAKE) gen-files

.PHONY: mac-deps
mac-deps:
	@echo Installing gsed for mac
	brew install gnu-sed

.PHONY: clean
clean:
	rm -rf $(ROOT_DIR)/out
	# this will be produced by running elastic-package check or build
	rm -rf $(ROOT_DIR)/build
	rm -rf $(GO_TOOLS)

$(REAL_ECS_DIR):
	git clone --branch $(ECS_GIT_REF) https://github.com/elastic/ecs.git $(REAL_ECS_DIR)

.PHONY: setup-go-tools
setup-go-tools:
	GOBIN=$(GO_TOOLS) go install github.com/elastic/elastic-package

.PHONY: setup-tools
setup-tools: $(REAL_ECS_DIR) setup-go-tools
	pipenv install
	cd $(REAL_ECS_DIR) && PIPENV_NO_INHERIT=1 pipenv --python 3.7 install -r scripts/requirements.txt

gen-files: $(TARGETS)
	go run $(ROOT_DIR)/scripts/generate-docs
	cd $(ROOT_DIR)/package/endpoint && $(GO_TOOLS)/elastic-package format
	cd $(ROOT_DIR)/package/endpoint && $(GO_TOOLS)/elastic-package lint

%-target:
	$(call gen_mapping_files,$*)
	$(call gen_schema_files,$*)

.PHONY: check-docker
check-docker:
	docker -v || { echo "please install docker before running the package registry"; exit 1; }
	docker-compose -v || { echo "please install docker-compose before running the package registry"; exit 1; }

$(ROOT_DIR)/out:
	mkdir -p $(ROOT_DIR)/out

# This target removes the current staged package and uses the current changes in package/endpoint
# It handles parsing out the package version from the manifest.yml file
.PHONY: build-package
build-package: $(ROOT_DIR)/out
	rm -rf $(PACKAGES_DIR)
	mkdir -p $(PACKAGES_DIR)/endpoint/$(PACKAGE_VERSION)
	cp -r $(ROOT_DIR)/package/endpoint/* $(PACKAGES_DIR)/endpoint/$(PACKAGE_VERSION)

# Use this target to run the package registry with your modifications to the endpoint package
.PHONY: run-registry
run-registry: check-docker build-package
	docker-compose pull
	docker-compose up

# Use this target to run the linter on the current state of the package
.PHONY: lint
lint: setup-go-tools
	cd $(ROOT_DIR)/package/endpoint && $(GO_TOOLS)/elastic-package lint

# Use this target to release the package (dev or prod) to the package storage repo
.PHONY: release
release:
	pipenv run python $(ROOT_DIR)/scripts/release_manager/main.py $(PACKAGE_STORAGE_REPO) $(ROOT_DIR)/package

# Use this target to promote a package that exists in the package-storage repo from one environment to another
.PHONY: promote
promote: setup-go-tools
	$(GO_TOOLS)/elastic-package promote

# Update elastic-package tooling
.PHONY: update-elastic-package
update-elastic-package:
	GO111MODULE=on go get -u github.com/elastic/elastic-package
	go mod tidy
	go mod vendor
