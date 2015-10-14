PYTHON=python
PYTHON3=python3

README.rst: README.md
	pandoc $< -o $@

.PHONY: test deploy
test:
	$(PYTHON) setup.py --version --url
	twitter-fave-mentions --version
	twitter-auto-follow --version

deploy:
	rm -r dist build
	$(PYTHON) setup.py sdist
	rm -r build
	$(PYTHON3) setup.py sdist bdist_wheel
	twine upload dist/*
	git push
	git push --tags
