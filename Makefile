install:
	python setup.py install

format:
	autoflake -i **/*.py
	isort -i toma_starter/**/*.py
	yapf -i **/*.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf toma.egg-info

build:
	make clean
	python3 setup.py sdist bdist_wheel

test:
	PYTHONPATH=./ python3 tests/server.py

publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	twine upload dist/*