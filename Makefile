
PYTHON ?= python


all:

.PHONY: test
test:
	$(PYTHON) test/test_doctests.py
	(cd test && $(PYTHON) test.py)

# TODO: add python 3.4
.PHONY: testall
testall: test25 test26 test27 test33
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
	@echo version is: $(shell cat package.json | json version)
	[[ `cat package.json | json version` == `grep '^## ' CHANGES.md | head -1 | awk '{print $$2}'` ]]

.PHONY: cutarelease
cutarelease: versioncheck
	[[ `git status | tail -n1` == "nothing to commit, working directory clean" ]]
	./tools/cutarelease.py -p dashdash -f package.json
