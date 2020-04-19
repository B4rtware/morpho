from invoke import task

from grpc_tools import protoc
from pathlib import Path

PROTO_PATH = Path("./service/proto/")
PROTO_OUT_PATH = PROTO_PATH
GRPC_PROTO_OUT_PATH = PROTO_PATH / Path("./grpc/")
PROTO_FILE = PROTO_PATH / Path("./dtaservice.proto")

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

@task
def deps(c)


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
