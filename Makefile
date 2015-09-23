readme.rst: readme.md
	pandoc $< -o $@

.PHONY: test
test:
	python setup.py --version --url
	twitter-fave-mentions --version
	twitter-auto-follow --version