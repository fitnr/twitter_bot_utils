PYTHON=python

README.rst: README.md
	pandoc $< -o $@

.PHONY: test
test:
	$(PYTHON) setup.py --version --url
	twitter-fave-mentions --version
	twitter-auto-follow --version