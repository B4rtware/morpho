from invoke import task


@task
def build(c):
    c.run("poetry run sphinx-apidoc -o docs/sphinx ./service/")


@task
def lint(c):
    c.run("poetry run python -m pylint --rcfile=.pylintrc service")


@task
def test(c):
    c.run("python -m pytest --color=yes")


@task
def format(c):
    c.run("poetry run python -m black --config=pyproject.toml --check .")
