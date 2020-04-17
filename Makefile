ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

ifeq (, $(shell which pipenv))
	$(error No pipenv in $(PATH), consider doing brew install pipenv)
endif

# This needs to be created, and include the following:
# ECS_DIR := <full path to the ecs repo>
ifeq (,$(wildcard $(ROOT_DIR)/config.mk))
    $(error config.mk file does not exist, please create it)
endif

include $(ROOT_DIR)/config.mk

CUST_SCHEMA_DIR := $(ROOT_DIR)/custom_schemas
SUB_TOP_DIR := $(ROOT_DIR)/custom_subsets
SUB_EVENTS_DIR := $(SUB_TOP_DIR)/elastic_endpoint/events
SUB_METADATA_DIR := $(SUB_TOP_DIR)/elastic_endpoint/metadata

package_file = $(ROOT_DIR)/out/$(1)/generated/beats/fields.ecs.yml

# Parameters
# 1: out directory name
# 2: subset glob
define gen_mapping_files
	cd $(ECS_DIR) && pipenv run python scripts/generator.py \
		--out $(ROOT_DIR)/out/$(1) \
		--include $(CUST_SCHEMA_DIR) \
		--subset $(2)
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

define gen_schema_files
	pipenv run python $(ROOT_DIR)/scripts/event_schema_generator/main.py \
		--out-schema-dir $(ROOT_DIR)/schemas/v1 \
		$(ECS_DIR) \
		$(CUST_SCHEMA_DIR) \
		$(1) \
		$(2)
endef

.PHONY: all
all: install_pipfile gen_files

.PHONY: install_pipfile
install_pipfile:
	pipenv install
	cd $(ECS_DIR) && pipenv install -r scripts/requirements.txt

.PHONY: gen_files
gen_files:
	$(call gen_mapping_files,events,$(SUB_EVENTS_DIR)/*)
	$(call gen_schema_files,$(SUB_EVENTS_DIR)/*.yaml,$(ROOT_DIR)/out/schema/events)
	$(call gen_mapping_files,metadata,$(SUB_METADATA_DIR)/*)
	$(call gen_schema_files,$(SUB_METADATA_DIR)/*.yaml,$(ROOT_DIR)/out/schema/metadata)

