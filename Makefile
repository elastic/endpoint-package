ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifeq (, $(shell which pipenv))
	$(error No pipenv in $(PATH), please install pipenv (brew install pipenv))
endif

# This needs to be created, and include the following:
# ECS_DIR := <path to the ecs repo>
ifeq (,$(wildcard $(ROOT_DIR)/config.mk))
    $(error config.mk file does not exist, please create it)
endif

include $(ROOT_DIR)/config.mk
REAL_ECS_DIR := $(realpath $(ECS_DIR))
$(info ecs dir: $(REAL_ECS_DIR))

CUST_SCHEMA_DIR := $(ROOT_DIR)/custom_schemas
SUB_TOP_DIR := $(ROOT_DIR)/custom_subsets
SUB_ROOT_DIR := $(SUB_TOP_DIR)/elastic_endpoint
SUB_EVENTS_DIR := $(SUB_TOP_DIR)/elastic_endpoint/events
SUB_METADATA_DIR := $(SUB_TOP_DIR)/elastic_endpoint/metadata
EVENT_SCHEMA_GEN := $(ROOT_DIR)/scripts/event_schema_generator
SUB_DIRS := $(sort $(dir $(wildcard $(SUB_ROOT_DIR)/*/)))

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
		$(REAL_ECS_DIR) \
		$(CUST_SCHEMA_DIR) \
		$(SUB_ROOT_DIR)/$(1)/*.yaml \
		$(SUB_ROOT_DIR)/$(1)/*.yml \
		$(ROOT_DIR)/out/schema/$(1)
endef

.PHONY: all
all: install_pipfile gen_files

.PHONY: install_pipfile
install_pipfile:
	cd $(EVENT_SCHEMA_GEN) && pipenv install
	cd $(REAL_ECS_DIR) && pipenv --python 3.7 install -r scripts/requirements.txt

gen_files: $(TARGETS)

%_target:
	$(call gen_mapping_files,$*)
	$(call gen_schema_files,$*)
