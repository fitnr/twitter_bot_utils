PYTHON=python
PYTHON3=python3

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

.PHONY: test deploy
test:
	$(PYTHON) setup.py test
	$(PYTHON) setup.py --version --url
	fave-mentions --version
	auto-follow --version

deploy: README.rst
	rm -rf dist build
	$(PYTHON) setup.py sdist
	rm -rf dist build
	$(PYTHON3) setup.py sdist bdist_wheel
	twine upload dist/*
	git push
	git push --tags
