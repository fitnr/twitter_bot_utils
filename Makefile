PYTHON=python
PYTHON3=python3

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

.PHONY: test deploy clean cov
test:
	$(PYTHON) setup.py test
	$(PYTHON) setup.py --version --url
	fave-mentions --version
	auto-follow --version

deploy: README.rst | clean
	$(PYTHON) setup.py sdist
	twine upload dist/*
	$(MAKE) clean
	$(PYTHON3) setup.py sdist bdist_wheel
	twine upload dist/*
	git push
	git push --tags

cov:
	coverage run setup.py test
	coverage html
	open htmlcov/index.html

clean: ; rm -rf build dist