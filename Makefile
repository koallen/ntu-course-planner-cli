.PHONY: build upload

build:
	. venv/bin/activate && python setup.py bdist_wheel

upload:
	. venv/bin/activate && twine upload dist/*
