## References
- **Docker Morpho File**: [Github repository](https://github.com/B4rtware/morpho/blob/master/docker/docker-morpho/Dockerfile)
- **Morpho Framework**: [Github repository](https://github.com/B4rtware/morpho)

## About

This docker image is considered to be used as a base image for a morpho service.

Currently it installs the following python package managers:
- [Poetry](https://python-poetry.org/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

## Build
- `docker build . --tag b4rtware/morpho`