.DEFAULT_GOAL := help

APP:=git-migration

install:  ## Install an editable version of this app
install:
	pipenv install --dev
	pipenv run pip install --editable .

uninstall:  ## Uninstall this app
	pipenv run pip uninstall -y $(APP)

format:  ## Auto-format and check pep8
	pipenv run yapf -i $$(find * -type f -name '*.py')
	pipenv run flake8 ./app ./tests

test:  ## Run tests
	pipenv run pytest
	pipenv run flake8 ./app ./tests

dist:  ## Create a binary dist
dist: clean
	(cd $(BASE) && $(PYTHON) setup.py sdist)

clean:  ## Clean all temporary files
clean:
	pipenv --rm || true
	find * -type f -name *.pyc | xargs rm -f
	find * -type f -name *~ | xargs rm -f
	find * -type d -name __pycache__ | xargs rm -rf
	rm -rf *.egg-info
	rm -rf dist/
	rm -f *.csv
	rm -rf .cache/
	rm -rf .eggs/

help:  ## Print list of Makefile targets
	@# Taken from https://github.com/spf13/hugo/blob/master/Makefile
	@grep --with-filename -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  cut -d ":" -f2- | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | sort
