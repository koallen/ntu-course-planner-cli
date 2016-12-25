all: build

build:
	source venv/bin/activate && python setup.py bdist_wheel

upload:
	source venv/bin/activate && twine upload dist/*
