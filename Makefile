SHELL := /bin/bash
.PHONY: setup install lambda lambda_layer_pandas
# A phony target is one that is not really the name of a file; rather it is just a name for a recipe to be executed when you make an explicit request. There are two reasons to 
use a phony target: to 
# avoid a conflict with a file of the same name, and to improve performance.

all: setup

setup:
	python3 -m venv ~/.venv/always_free
        # https://docs.python.org/3/library/venv.html#creating-virtual-environments
	# After running `Make setup`, add an alias to your .zshrc file, i.e. `cd ~/Documents/projects/always_free && source ~/.venv/always_free/bin/activate`
install:
	pip install -r requirements.txt
