IN_ENV = . .venv/bin/activate;

package: .venv/bin/activate
	$(IN_ENV) pip install setuptools
	$(IN_ENV) python setup.py sdist
	$(IN_ENV) twine upload dist/*

test: .venv/bin/activate
	$(IN_ENV) pip install .
	$(IN_ENV) cd test && python3 -m unittest
	$(IN_ENV) pip uninstall -y yinstruments

doc:
	cd doc && make html

format: .venv/bin/activate
	$(IN_ENV) black -q -l 100 $$(git ls-files '*.py')

pylint:
	pylint $$(git ls-files '*.py')

env: .venv/bin/activate

.venv/bin/activate: requirements.txt
	python3 -m venv .venv
	$(IN_ENV) pip install -r requirements.txt
	$(IN_ENV) pip install -e .


.PHONY: test doc env format pylint