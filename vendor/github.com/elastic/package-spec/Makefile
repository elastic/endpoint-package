.PHONY: test

# Updates the spec in language libraries
update: code/*
	@$(foreach lang,$^,make -C $(lang) update;)

# Checks that language libraries have latest specs
check: code/*
	@$(foreach lang,$^,make -C $(lang) check;)

# Tests the language libraries' code
test: code/*
	@$(foreach lang,$^,make -C $(lang) test;)
