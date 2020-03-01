.DEFAULT_GOAL=help

install:  ## install
	pip3 install --editable .

pep8:  ## Pep8
	yapf -i $$(find * -type f -name '*.py')
	flake8 ./metal ./tests


test:  ## test
	pip3 -q install -r test-requirements.txt
	pytest
	flake8 ./metal ./tests

clean:  ## clean
	find * -type f -name *.pyc | xargs rm -f
	find * -type f -name *~ |xargs rm -f
	rm -rf *.egg-info
	rm -rf dist/

help:  ## Print list of Makefile targets
	@# Taken from https://github.com/spf13/hugo/blob/master/Makefile
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  cut -d ":" -f1- | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
