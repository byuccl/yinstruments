IN_ENV = if [ -e .venv/bin/activate ]; then . .venv/bin/activate; fi;

package:
	$(IN_ENV) python setup.py sdist
	$(IN_ENV) twine upload dist/*

test: 
	$(IN_ENV) pip install .
	$(IN_ENV) cd test && python3 -m unittest
	$(IN_ENV) pip uninstall -y yinstruments

doc:
	cd doc && make html

format:
	$(IN_ENV) black -q -l 100 $$(git ls-files '*.py')

pylint:
	pylint $$(git ls-files '*.py')

env: .venv/bin/activate

.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(IN_ENV) pip install -r requirements.txt
	$(IN_ENV) pip install -e .


.PHONY: test doc env format pylint