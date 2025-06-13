# Intro

This is a devcontainer for easy collaboration within a development team. The setup makes it easy to share the code by avoiding the "it works on my machine" issue.
Feel free to clone and use the Project. No guarantees provided, use at your own risk.

## Add Python packages
use "uv" to add and install python packages for your pyproject.toml
https://docs.astral.sh/uv/

e.g. add and install pandas:
```
uv add pandas
```
install all packages from the loc file (done by default when the container is created)
```
uv sync --all-groups --frozen
```

## Use Pre-commit hooks
Ruff is used as a linter and as a formatter for every commit. See more:
https://docs.astral.sh/ruff/

This ensures code quality like Type hints, Docstrings, and much more.
Ruff configuration is found in ruff.toml

## Write tests
In the pyproject.toml you find a strict 90% code coverage target. If you fail to test your code, the CI will fail.
To change the 90% see: pyproject.toml
```
[tool.coverage.report]
fail_under = 90
```
It is recomended to write test, run them regualary local with the UI or with
```
uv run pytest tests --cov=src --cov-report term-missing
```
Tests are located in the folder "tests". Consider setting up a conftest.py where you use fixtures for your local session, where you can setup data that is consumed in multiple tests.

## Write Documentation
This Project has a basic MKDocs setup. See
https://www.mkdocs.org/

A Preview of the choses setup is found here:
https://oprypin.github.io/mkdocs-gen-files/index.html

The Mkdocs config is found in "mkdocs.yml". Write your documentation in the folder "docs". If you want to add new Tabs to the page, add them in the config file:
```
nav:
  - Intro: index.md
  - Code Reference: reference/
```

To preview the docs locally:
```
uv run mkdocs serve
```
To build for production:
```
uv run mkdocs build
```
To deploy (e.g., to GitHub Pages):
```
uv run mkdocs gh-deploy
```

To run it automatically with each push to main and a test build with each push, uncomment the file /.github/workflows/mkdocs_not_active.yaml
