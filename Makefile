include *.mk

.PHONY: build dist test release publish-test

PACKAGE_NAME=data-product-hub
testpypi = https://test.pypi.org/legacy/


clean-build:
	rm -rf dist

build-image:
	docker build -t data-product-hub-deployer .

build:
	pip install --upgrade build

dist:
	python -m build

publish-test: clean-build build dist
	@twine upload --verbose --repository-url https://test.pypi.org/legacy/ --username '__token__' --password $(PYPI_PASSWORD_TEST) dist/*


publish-prod: clean-build build dist
	@twine upload --username '__token__' --password $(PYPI_PASSWORD_PROD) dist/*