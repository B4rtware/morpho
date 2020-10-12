## References
- **Echo Example**: [Github repository](https://github.com/B4rtware/morpho/blob/master/examples/services/de/tuberlin/qds/echo)
- **Morpho Framework**: [Github repository](https://github.com/B4rtware/morpho)

## About
This docker image implements a morpho echo service.

## Build
- `docker build . --tag b4rtware/morpho-service-echo`

## Create a container
- `docker run -d -p 50000:50000 b4rtware/morpho-service-echo`
