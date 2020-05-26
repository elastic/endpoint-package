ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
# we are intentionally pinning the ECS version here, when ecs releases a new version 
# we'll discuss whether we need to release a new package and bump the version here
ECS_GIT_REF ?= v1.5.0

# This variable specifies to location of the package-storage repo. It is used for automatically creating a PR
# to release a new endpoint package. This can be overridden with the location on your file system using the config.mk
# file.
PACKAGE_STORAGE_REPO ?= $(ROOT_DIR)/../package-storage

ifeq (, $(shell which pipenv))
	$(error No pipenv in $(PATH), please install pipenv (brew install pipenv))
endif

# This needs to be created, and include the following:
# ECS_DIR := <path to the ecs repo>
ifeq (,$(wildcard $(ROOT_DIR)/config.mk))
    $(error config.mk file does not exist, please create it)
endif

include $(ROOT_DIR)/config.mk
ifeq ($(ECS_DIR),)
  $(error ECS_DIR not defined by config config.mk)
endif
REAL_ECS_DIR := $(realpath $(ECS_DIR))
$(info ecs dir: $(REAL_ECS_DIR))
$(info ecs git ref: $(ECS_GIT_REF))

# set mage binary path based on whether the gopath is set
ifeq ($(GOPATH),)
	MAGE_BIN := $(HOME)/go/bin/mage
else
	MAGE_BIN := $(GOPATH)/bin/mage
endif

MAGE_DIR := $(ROOT_DIR)/out/mage
REG_DIR := $(ROOT_DIR)/out/package-registry
PACKAGES_DIR := $(ROOT_DIR)/out/packages
# Default location for packages, this will be used in conjunction with the package defined in this repo
DEF_PACKAGES_DIR := $(REG_DIR)/build/package-storage/packages
CUST_SCHEMA_DIR := $(ROOT_DIR)/custom_schemas
SUB_TOP_DIR := $(ROOT_DIR)/custom_subsets
SUB_ROOT_DIR := $(SUB_TOP_DIR)/elastic_endpoint
SUB_EVENTS_DIR := $(SUB_TOP_DIR)/elastic_endpoint/events
SUB_METADATA_DIR := $(SUB_TOP_DIR)/elastic_endpoint/metadata
EVENT_SCHEMA_GEN := $(ROOT_DIR)/scripts/event_schema_generator
SUB_DIRS := $(sort $(dir $(wildcard $(SUB_ROOT_DIR)/*/)))

# Get the package version from the manifest file
PACKAGE_VERSION := $(shell awk '/^version: /{print $$2}' $(ROOT_DIR)/package/endpoint/manifest.yml)
TAG_NAME := v$(PACKAGE_VERSION)

# Given a path this returns the directory (e.g. events, metadata)
schema_name = $(shell basename $(1))
package_file = $(ROOT_DIR)/out/$(1)/generated/beats/fields.ecs.yml
TARGETS := $(foreach schema_dir,$(SUB_DIRS),$(call schema_name,$(schema_dir))_target)

# Parameters
# 1: schema name (e.g. events, metadata)
define gen_mapping_files
	cd $(REAL_ECS_DIR) && pipenv run python scripts/generator.py \
		--out $(ROOT_DIR)/out/$(1) \
		--include $(CUST_SCHEMA_DIR) \
		--ref $(ECS_GIT_REF) \
		--subset $(SUB_ROOT_DIR)/$(1)/*
	# remove the first 8 lines
	sed -i '' -e '1,8d' $(call package_file,$(1))
	# remove indentation
	sed -i '' -e 's/^  //g' $(call package_file,$(1))
	mkdir -p $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/beats $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/ecs $(ROOT_DIR)/generated/$(1)
	cp -r $(ROOT_DIR)/out/$(1)/generated/elasticsearch $(ROOT_DIR)/generated/$(1)

	# remove unused files
	rm -r $(ROOT_DIR)/generated/$(1)/elasticsearch/6
	rm $(ROOT_DIR)/generated/$(1)/ecs/ecs_flat.yml
endef

# Parameters
# 1: schema name (e.g. events, metadata)
define gen_schema_files
	cd $(EVENT_SCHEMA_GEN) && pipenv run python main.py \
		--out-schema-dir $(ROOT_DIR)/schemas/v1 \
		--ecs_git_ref $(ECS_GIT_REF) \
		$(REAL_ECS_DIR) \
		$(CUST_SCHEMA_DIR) \
		$(SUB_ROOT_DIR)/$(1)/*.yaml \
		$(SUB_ROOT_DIR)/$(1)/*.yml \
		$(ROOT_DIR)/out/schema/$(1)
endef

.PHONY: all
all: install_pipfile gen_files

.PHONY: clean
clean:
	rm -rf $(ROOT_DIR)/out

.PHONY: install_pipfile
install_pipfile:
	cd $(EVENT_SCHEMA_GEN) && pipenv install
	cd $(REAL_ECS_DIR) && pipenv --python 3.7 install -r scripts/requirements.txt

gen_files: $(TARGETS)

%_target:
	$(call gen_mapping_files,$*)
	$(call gen_schema_files,$*)

.PHONY: check-go
check-go:
	go version || { echo "please install go before running the package registry"; exit 1; }

$(ROOT_DIR)/out:
	mkdir -p $(ROOT_DIR)/out

$(MAGE_BIN):
	git clone https://github.com/magefile/mage $(MAGE_DIR)
	cd $(MAGE_DIR) && go run bootstrap.go

$(REG_DIR):
	git clone https://github.com/elastic/package-registry $(REG_DIR)

# This target removes the current staged package and uses the current changes in package/endpoint
# It handles parsing out the package version from the manifest.yml file
.PHONY: build-package
build-package:
	rm -rf $(PACKAGES_DIR)
	mkdir -p $(PACKAGES_DIR)/endpoint/$(PACKAGE_VERSION)
	cp -r $(ROOT_DIR)/package/endpoint/ $(PACKAGES_DIR)/endpoint/$(PACKAGE_VERSION)

# Use this target to run the package registry with your modifications to the endpoint package
.PHONY: run-registry
run-registry: check-go $(ROOT_DIR)/out $(MAGE_BIN) $(REG_DIR) build-package
	cd $(REG_DIR) && git pull
	cd $(ROOT_DIR)/out/package-registry && PACKAGE_PATHS="$(PACKAGES_DIR),$(DEF_PACKAGES_DIR)" mage build && go run .

# This target uses the hub tool to create a PR to the package-storage repo with the contents of the
# modified endpoint package in this repo
.PHONY: create-storage-pr
create-storage-pr:
	hub --version || { echo "please install hub before running the release-package command"; exit 1; }
	-cd $(PACKAGE_STORAGE_REPO) && git remote add upstream git@github.com:elastic/package-storage.git; \
		git checkout master; \
		git branch -D endpoint-release-$(PACKAGE_VERSION); \
		git push -d origin endpoint-release-$(PACKAGE_VERSION);
	cd $(PACKAGE_STORAGE_REPO) && git fetch upstream; \
		git switch -c endpoint-release-$(PACKAGE_VERSION) --track upstream/master
	mkdir -p $(PACKAGE_STORAGE_REPO)/packages/endpoint/$(PACKAGE_VERSION)
	rm -rf $(PACKAGE_STORAGE_REPO)/packages/endpoint/$(PACKAGE_VERSION)
	cp -r $(ROOT_DIR)/package/endpoint/ $(PACKAGE_STORAGE_REPO)/packages/endpoint/$(PACKAGE_VERSION)
	cd $(PACKAGE_STORAGE_REPO) && git add $(PACKAGE_STORAGE_REPO)/packages/endpoint/$(PACKAGE_VERSION) \
		&& git commit -m "Adding package version $(PACKAGE_VERSION)" \
		&& git push -u origin endpoint-release-$(PACKAGE_VERSION)
	cd $(PACKAGE_STORAGE_REPO) && hub pull-request \
		-m "Endpoint package version $(PACKAGE_VERSION)" \
		-m "Releasing new endpoint package" \
		-b elastic:master -d

.PHONY: tag-version
tag-version:
	-git remote add upstream git@github.com:elastic/endpoint-app-team.git
	-git tag $(TAG_NAME)
	-git push upstream $(TAG_NAME)

.PHONY: bump-version
bump-version:
	pipenv install
	pipenv run bump2version minor

# Use this target to tag and release
.PHONY: release-package
release-package: tag-version create-storage-pr bump-version

test:
	cd $(EVENT_SCHEMA_GEN) && pipenv install; pipenv install --dev; \
	pipenv run python -m pytest test_main.py
