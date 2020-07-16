<img src="docs/images/morpho.png" width="100%" alt="Morpho Logo">

> Python port for the go written [doctrans](https://github.com/theovassiliou/doctrans)

<div align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square">
</a>
<a href=""><img alt="license: MIT" src="https://img.shields.io/badge/license%3A-MIT-green?style=flat-square">
</a>
<a href=""><img src="https://img.shields.io/badge/python%3A-%5E3.8-blue?style=flat-square"></a><br>
<a href=""><img src="https://circleci.com/gh/B4rtware/morpho.svg?style=shield&circle-token=5cd58aa7f458d098a3b9a82e861d87d64ec4a181"></a>
<a href="https://codecov.io/gh/B4rtware/morpho">
  <img src="https://codecov.io/gh/B4rtware/morpho/branch/master/graph/badge.svg?token=14BJUE5PY5" />
</a>
</div>

Morpho is a framework for microservice based web services. It offers the ability to transform a given document with a provided function.

In the first place this framework was created to use it for research purposes.

## 💡 Installation

`pip install morpho`

⚠️ currently in alpha: public api may change with breaking changes ⚠️

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

## 📝 License
MIT
