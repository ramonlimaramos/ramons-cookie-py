PLATFORM = $(shell uname)

PROJECT_NAME={{cookiecutter.pkg_name}}
PROJECT_TAG?={{cookiecutter.pkg_name}}
GITHUB_PROJECT={{cookiecutter.github_usr}}/{{cookiecutter.repository_name}}

VIRTUALENV_ARGS=-p {{cookiecutter.pyversion}}

PYTHON_MODULES={{cookiecutter.pkg_name}}

DOCS_RST?= #${shell find docs -type f -iname '*.rst'}


WGET = wget -q

ifeq "" "$(shell which wget)"
WGET = curl -O -s -L
endif

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

SQLITE_DATABASE_URI=sqlite:////tmp/{{cookiecutter.directory_name}}.db
POSTGRES_DATABASE_URI=postgresql://root:root@localhost:15432/{{cookiecutter.directory_name}}-integration

default: test

include extras/makefiles/python.mk
# include extras/makefiles/github.mk
# include extras/makefiles/deploy.mk

clean: python_clean
	@rm -rf docs/_build

purge: python_purge
	@rm -rf docs/plantuml.jar
	@rm -rf docs/node_modules
	@rm -rf docs/package-lock.json

build: python_build ${CHECKPOINT_DIR}/.python_develop

run: build
	${VIRTUALENV} FLASK_ENV=development FLASK_APP={{cookiecutter.pkg_name}}.main flask run

gunicorn: build
	${VIRTUALENV} {{cookiecutter.pyrunner}} -m gunicorn -w 1 -b 0.0.0.0:5000 {{cookiecutter.pkg_name}}.main:app --log-level=-debug --reload

test: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} py.test ${PYTHON_MODULES} --ignore ${PYTHON_MODULES}/tests/integration

pdb: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} -x --ff --pdb --ignore ${PYTHON_MODULES}/tests/integration

ci:
ifeq "true" "${TRAVIS}"
	CI=1 py.test ${PYTHON_MODULES} --durations=10 --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report=xml --junitxml=pytest-report.xml
else
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} --durations=10 --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report=xml --junitxml=pytest-report.xml
endif

coverage: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report term-missing --cov-report html:cov_html --cov-report xml:cov.xml --cov-report annotate:cov_annotate

codestyle: ${REQUIREMENTS_TEST}
	${VIRTUALENV} pycodestyle --statistics -qq ${PYTHON_MODULES} | sort -rn || echo ''

todo: ${REQUIREMENTS_TEST}
	${VIRTUALENV} {{cookiecutter.pyrunner}} -m flake8 ${PYTHON_MODULES}
	${VIRTUALENV} {{cookiecutter.pyrunner}} -m pycodestyle --first ${PYTHON_MODULES}
	find ${PYTHON_MODULES} -type f | xargs -I [] grep -H TODO []

search:
	find ${PYTHON_MODULES} -regex .*\.py$ | xargs -I [] egrep -H -n 'print|ipdb' [] || echo ''

report:
	coverage run --source=${PYTHON_MODULES} setup.py test

tdd: ${REQUIREMENTS_TEST}
	${VIRTUALENV} {{cookiecutter.pyrunner}} -m ptw --ignore ${VIRTUALENV_DIR} --ignore ${PYTHON_MODULES}/tests/integration/

tox: ${REQUIREMENTS_TEST}
	${VIRTUALENV} {{cookiecutter.pyrunner}} -m tox

docs/plantuml-jar-lgpl-1.2019.5.zip:
	cd docs && ${WGET} https://ufpr.dl.sourceforge.net/project/plantuml/1.2019.5/plantuml-jar-lgpl-1.2019.5.zip

docs/plantuml.jar: docs/plantuml-jar-lgpl-1.2019.5.zip
	cd docs && unzip -o plantuml-jar-lgpl-1.2019.5.zip plantuml.jar
	touch $@

docs: ${REQUIREMENTS_TEST} docs/plantuml.jar
	@${VIRTUALENV} $(MAKE) -C docs html

docs/_build/latex/cat-web.tex: ${REQUIREMENTS_TEST} ${PYTHON_SOURCES} ${DOCS_RST} docs/plantuml.jar
	rm -rf docs/_build/latex
	${VIRTUALENV} $(MAKE) -C docs latex

pdf: docs/_build/latex/{{cookiecutter.directory_name}}.tex
	$(MAKE) -C docs/_build/latex

docs_ci: docs/plantuml.jar
	${MAKE} -C docs html

dist: python_egg python_wheel

deploy: ${REQUIREMENTS_TEST} dist
ifeq "true" "${TRAVIS}"
	twine upload dist/*.whl
else
	${VIRTUALENV} twine upload dist/*.whl -r local
endif

.PHONY: clean purge dist docs create_db
