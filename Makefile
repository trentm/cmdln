
PYTHON ?= python


all:

.PHONY: clean
clean:
	rm -rf dist build MANIFEST {.,docs,lib,examples,test}/*.pyc

.PHONY: test
test:
	$(PYTHON) test/test_doctests.py
	(cd test && $(PYTHON) test.py)

# TODO: add python 3.3 and 3.4 testing
.PHONY: testall
testall: test25 test26 test27
.PHONY: test25
test25:
	@echo "# Test with python 2.5"
	@python2.5 --version
	make test PYTHON=python2.5
.PHONY: test26
test26:
	@echo "# Test with python 2.6"
	@python2.6 --version
	make test PYTHON=python2.6
.PHONY: test27
test27:
	@echo "# Test with python 2.7"
	@python2.7 --version
	make test PYTHON=python2.7
.PHONY: test33
test33:
	@echo "# Test with python 3.3"
	@python3.3 --version
	make test PYTHON=python3.3
.PHONY: test34
test34:
	@echo "# Test with python 3.4"
	@python3.4 --version
	make test PYTHON=python3.4


# Ensure CHANGES.md and package.json have the same version.
.PHONY: versioncheck
versioncheck:
	@export VERSION=$(shell PYTHONPATH=`pwd`/lib python -c 'import cmdln; print(cmdln.__version__)') \
	    && echo version is: $$VERSION \
	    && [[ $$VERSION == `grep '^## ' CHANGES.md | head -1 | awk '{print $$2}'` ]]
	@echo PASS: all versions match

.PHONY: cutarelease
cutarelease: versioncheck
	[[ `git status | tail -n1` == "nothing to commit, working directory clean" ]]
	./tools/cutarelease.py -p cmdln -f lib/cmdln.py

# Only have this around to retry package uploads on a tag created by
# 'make cutarelease' because PyPI upload is super-flaky (at least for me).
.PHONY: pypi-upload
pypi-upload:
	COPY_EXTENDED_ATTRIBUTES_DISABLE=1 python setup.py sdist --formats zip upload
