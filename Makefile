
install:
	pip install --editable .

pep8:
	yapf -i $$(find * -type f -name '*.py')
	flake8 ./metal ./tests


test:
	pip -q install -r test-requirements.txt
	pytest
	flake8 ./metal ./tests

clean:
	find * -type f -name *.pyc | xargs rm -f
	find * -type f -name *~ |xargs rm -f
	rm -rf *.egg-info
	rm -rf dist/

