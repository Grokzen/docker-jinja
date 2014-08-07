help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  run-coverage    runs tox then coverage report locally"
	@echo "  clean           remove temporary files created by build tools"
	@echo "  cleantox        remove files created by tox"
	@echo "  cleanegg        remove temporary files created by build tools"
	@echo "  cleanpy         remove temporary python files"
	@echo "  cleanall        all the above + tmp files from development tools"
	@echo "  sdist           make a source distribution"

run-coverage:
	coverage erase
	tox
	coverage combine
	coverage report


clean:
	-rm -f MANIFEST
	-rm -rf dist/
	-rm -rf build/

cleancov:
	-rm -rf htmlcov/

cleantox:
	-rm -rf .tox/

cleanegg:
	-rm -rf docker_jinja.egg-info/

cleanpy:
	-find . -type f -name "*~" -exec rm -f "{}" \;
	-find . -type f -name "*.orig" -exec rm -f "{}" \;
	-find . -type f -name "*.rej" -exec rm -f "{}" \;
	-find . -type f -name "*.pyc" -exec rm -f "{}" \;
	-find . -type f -name "*.parse-index" -exec rm -f "{}" \;
	-find . -type d -name "__pycache__" -exec rm -rf "{}" \;

cleanall: clean cleanegg cleanpy cleancov

sdist: clean cleanegg cleanpy
	python setup.py sdist
