IN_ENV := . .venv/bin/activate;

env:
	python3 -m venv .venv
	$(IN_ENV) pip install packaging

check_version_increase:
	$(IN_ENV) python check_version.py ../setup.py