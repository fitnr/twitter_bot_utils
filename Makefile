PYTHON=python
PYTHON3=python3

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

docs.zip: $(wildcard docs/*.rst docs/*/*.rst)
	$(MAKE) -C docs html
	cd docs/_build/html; \
	zip -qr ../../../$@ . -x '*/.DS_Store' .DS_Store

.PHONY: test deploy clean cov
test:
	$(PYTHON) setup.py --version --url
	coverage run --include=twitter_bot_utils/*,build/lib/* setup.py -q test
	coverage report
	coverage html
	fave-mentions --version
	auto-follow --version
	twitter-auth --version

deploy: README.rst | clean
	python setup.py register
	$(PYTHON) setup.py sdist
	$(PYTHON3) setup.py bdist_wheel
	twine upload dist/*
	git push
	git push --tags

clean: ; rm -rf build dist