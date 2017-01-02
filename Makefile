src_dir := httpmeter

python ?= python3.5
virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
pytest := $(virtualenv_dir)/bin/py.test
linter := $(virtualenv_dir)/bin/flake8
py_requirements ?= requirements/prod.txt requirements/dev.txt
coverage := $(virtualenv_dir)/bin/coverage


test: $(virtualenv_dir)
	PYTHONPATH=$(PYTHONPATH):. $(coverage) run \
		--source $(src_dir) --branch $(pytest) -s tests
	$(coverage) report -m
.PHONY: test

lint: $(virtualenv_dir)
	$(linter) $(src_dir)
.PHONY: lint

$(virtualenv_dir): $(py_requirements)
	virtualenv $@ -p $(python)
	for r in $^ ; do \
		$(pip) install -r $$r ; \
	done
