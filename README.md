<img src="https://raw.githubusercontent.com/B4rtware/morpho/master/docs/images/morpho.png" width="100%" alt="Morpho Logo">

> Python port for the go written [doctrans](https://github.com/theovassiliou/doctrans)

<div align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://github.com/B4rtware/morpho/blob/master/LICENSE"><img alt="license: MIT" src="https://img.shields.io/badge/license%3A-MIT-green">
</a>
<a href="https://github.com/B4rtware/morpho"><img src="https://img.shields.io/badge/python%3A-%5E3.8-blue"></a><br>
<a href="https://app.circleci.com/pipelines/github/B4rtware/morpho"><img src="https://circleci.com/gh/B4rtware/morpho.svg?style=shield"></a>
<a href="https://codecov.io/gh/B4rtware/morpho">
  <img src="https://codecov.io/gh/B4rtware/morpho/branch/master/graph/badge.svg" />
</a>
<a href="">
  <img src="https://img.shields.io/pypi/v/morpho?color=dar-green" />
</a>
</div>

Morpho is a framework for microservice based web services. It offers the ability to transform a given document with a provided function.

In the first place this framework was created to be used for research purposes.

## 💡 Installation

`pip install morpho`

### via git

1. make sure to use at least **python 3.8**
2. clone the repo `git clone https://github.com/B4rtware/morpho.git`
3. `cd morpho` and install dependencies via
    - `poetry install` ([Poetry](https://github.com/python-poetry/poetry))
    or
    - use the provided `requirements.txt`

## ⚙️ Server Example

### ... without options

service.py
```python
from morpho.server import Service

def work(document: str) -> str:
    return document

service = Service(name="Echo", version="0.0.1")

if __name__ == "__main__":
    service.run()
```

### ... with options

service.py
```python
from morpho.server import Service
from pydantic import BaseModel

class Options(BaseModel):
    name: str

def work(document: str, options: Options) -> str:
    return document + options.name

service = Service(name="AppendName", version="0.0.1", options_type=Options)

if __name__ == "__main__":
    service.run()
```

## 🖥️ Client Example

client.py
```python
from morpho.client import Client
from morpho.client import ClientConfig

morpho = Client(ClientConfig("http://localhost:8761/eureka/"))

response = morpho.transform_document(
    "This is a Document!",
    service_name="Echo"
)

print(response.document)
```
`>>> This is a Document!`

## 👩🏽‍💻 Development

### Creating a new release

1. Run the following command `poetry version <version>`
<br>*Morpho* uses the following schema: `^\d+\.\d+\.\d+((b|a)\d+)?$`

2. Bump the version within the file: `morpho/__version__.py`
<br>Make sure it's the same version used when bumping with poetry

3. Open `Changelog.md` and write the new changelog:
    - Use the following `#` header: `v<version> - (dd.mm.yyyy)`
    <br>Used `##` headers:
    - 💌 Added
    - 🔨 Fixed
    - ♻️ Changed

4. Stage the modified files and push them with the following commit message:
    > chore: bump to version `<version>`

5. Run the following command `poetry build` to create a tarball and a wheel based on the new version

6. Create a new github release and:
    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox
    2. Use the `#` header style to fill in the *Release title* (copy it from the `Changelog.md`)
    3. Copy the version with the `v`-prefix into the *Tag version*

7. Attach the produced tarball and wheel (`dist/`) to the release

8. Check *This is a pre-release* if it's either an alpha or beta release *(a|b)* - ***optional*** 

9. **Publish release**

## 📝 License
MIT
