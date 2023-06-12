IN_ENV = if [ -e .venv/bin/activate ]; then . .venv/bin/activate; fi;

package:
	$(IN_ENV) python setup.py sdist
	$(IN_ENV) twine upload dist/*

test: 
	$(IN_ENV) cd test && python3 -m unittest

doc:
	cd doc && make html

format:
	black -q -l 100 $$(git ls-files '*.py')
	
pylint:
	pylint $$(git ls-files '*.py')

env:
	python3 -m venv .venv
	$(IN_ENV) pip install -e .
	$(IN_ENV) pip install -r requirements.txt


.PHONY: test doc