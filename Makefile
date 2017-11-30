# Copyright 2014-17 Neil Freeman contact@fakeisthenewreal.org
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

PYTHON=python
PYTHON3=python3

.PHONY: all
all: README.rst docs.zip

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	- python setup.py check --restructuredtext --strict

docs.zip: docs/source/conf.py $(wildcard docs/*.rst docs/*/*.rst twitter_bot_utils/*.py) 
	$(MAKE) -C docs html
	cd docs/_build/html; \
	zip -qr ../../../$@ . -x '*/.DS_Store' .DS_Store

.PHONY: test deploy clean cov
test:
	$(PYTHON) setup.py --version --url
	coverage run --include=twitter_bot_utils/*,build/lib/* setup.py -q test
	coverage report
	coverage html
	tbu --version
	tbu like --help
	tbu follow --help
	tbu auth --help

deploy: README.rst | clean
	python setup.py register
	$(PYTHON) setup.py sdist
	$(PYTHON3) setup.py bdist_wheel
	twine upload dist/*
	git push
	git push --tags

clean: ; rm -rf build dist