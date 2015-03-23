readme.rst: readme.md
	pandoc $< -o $@

.PHONY: test
test:
	twitter-fave-mentions --version
	twitter-auto-follow --version