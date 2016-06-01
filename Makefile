
SCRIPT_DIR ?= "make_scripts"


build_dist:
	@$(SCRIPT_DIR)/build_dist.bash

# Removes development/build directories that accumulate over time.
clean:
	@$(SCRIPT_DIR)/clean.bash

lint3.4:
	@$(SCRIPT_DIR)/lint3.4.bash
test:
	tox
	
# Creates virtual environments for development using the Python executables in $ENV_LIST. 
# Existing environments are recreated.	
venv:
	@$(SCRIPT_DIR)/venv.bash

