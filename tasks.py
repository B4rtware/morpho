from invoke import task

from grpc_tools import protoc
from pathlib import Path

PROTO_PATH = Path("./service/proto/")
PROTO_OUT_PATH = PROTO_PATH
GRPC_PROTO_OUT_PATH = PROTO_PATH / Path("./grpc/")
PROTO_FILE = PROTO_PATH / Path("./dtaservice.proto")


@task
def build(c):
    """Run this if new modules where added"""
    c.run("poetry run sphinx-apidoc -o docs/sphinx/api ./service/")

@task
def docs(c):
    """Run if docstrings have changed"""
    c.run("poetry run sphinx-build -M html ./docs/sphinx ./docs/sphinx/_build -v")

@task
def check(c):
    c.run("poetry run sphinx-build -M spelling ./docs/sphinx ./docs/sphinx/_build -v -W")

@task
def lint(c):
    c.run("poetry run python -m pylint --rcfile=.pylintrc service")


@task
def tests(c):
    c.run("python -m pytest --color=yes tests/unit")
    c.run("python -m pytest --color=yes tests/integration")

@task
def format(c):
    c.run("poetry run python -m black --config=pyproject.toml --check .")


@task
def proto(c):
    if not GRPC_PROTO_OUT_PATH.exists():
        GRPC_PROTO_OUT_PATH.mkdir()
    protoc.main(
        (
            "",
            f"-I{PROTO_PATH.absolute()}",
            f"--python_out={PROTO_OUT_PATH.absolute()}",
            f"--grpc_python_out={GRPC_PROTO_OUT_PATH.absolute()}",
            str(PROTO_FILE.name),
        )
    )
