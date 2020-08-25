from invoke import task


# from grpc_tools import protoc
from pathlib import Path
import requests
import regex as re

VERSION_CHECK_REGEX = re.compile(r"^\d+\.\d+\.\d+(-(b|a)\.\d+)?$")

# PROTO_PATH = Path("./morpho/proto/")
# PROTO_OUT_PATH = PROTO_PATH
# GRPC_PROTO_OUT_PATH = PROTO_PATH / Path("./grpc/")
# PROTO_FILE = PROTO_PATH / Path("./morpho.proto")

# PROTO_VENDOR_PATH = PROTO_OUT_PATH / Path("vendor/")

# REQUIRED_PROTO_FILES = {
#     "google/protobuf/": [
#         "https://raw.githubusercontent.com/protocolbuffers/protobuf/master/src/google/protobuf/descriptor.proto",
#         "https://raw.githubusercontent.com/protocolbuffers/protobuf/master/src/google/protobuf/empty.proto",
#         "https://raw.githubusercontent.com/protocolbuffers/protobuf/master/src/google/protobuf/struct.proto"
#     ],
#     "google/api/": [
#         "https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/http.proto",
#         "https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/annotations.proto"
#     ]
# }

# TODO: submodule?
# @task
# def deps(c):
#     """Pull dependencies (proto files) from git"""
#     for path, files in REQUIRED_PROTO_FILES.items():
#         for proto in files:
#             file_path = Path(PROTO_VENDOR_PATH / Path(path + proto.split("/")[-1])).resolve()
#             file_path.parent.mkdir(exist_ok=True, parents=True)
#             with (file_path / Path()) .open("wb") as protofile:
#                 response = requests.get(proto)
#                 if response.status_code == 200:
#                     protofile.write(response.content)
#                 else:
#                     print("error while downloading: {}".format(proto))


@task
def build(c):
    """Run this if new modules where added"""
    c.run("poetry run sphinx-apidoc -o docs/sphinx/api ./morpho/")

@task
def docs(c):
    """Run if docstrings have changed"""
    c.run("poetry run sphinx-build -M html ./docs/sphinx ./docs/dist -v")

@task
def check(c):
    c.run("poetry run sphinx-build -M spelling ./docs/sphinx ./docs/dist -v -W")

@task
def lint(c):
    c.run("poetry run python -m pylint --rcfile=.pylintrc service")

# @task
# def deps(c):
#     c.run("")


@task
def tests(c):
    c.run("python -m pytest --color=yes tests/unit")
    c.run("python -m pytest --color=yes tests/integration")

@task
def format(c):
    c.run("poetry run python -m black --config=pyproject.toml --check .")

@task
def export(c):
    c.run("poetry export -f requirements.txt > requirements.txt")

# @task
# def bump(c, version: str = ""):
#     if not VERSION_CHECK_REGEX.match(version):
#         print("The version <{}> you have specified does not match semver style!".format(version))
#         exit(1)


# @task
# def proto(c):
#     if not GRPC_PROTO_OUT_PATH.exists():
#         GRPC_PROTO_OUT_PATH.mkdir()
#     protoc.main(
#         (
#             "",
#             f"-I{PROTO_VENDOR_PATH.absolute()}",
#             f"--python_out={PROTO_OUT_PATH.absolute()}",
#             f"--grpc_python_out={GRPC_PROTO_OUT_PATH.absolute()}",
#             f"--proto_path={PROTO_PATH}",
#             str(PROTO_FILE.name),
#         )
#     )
