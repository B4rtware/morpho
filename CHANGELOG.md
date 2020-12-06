# v1.0.0b8 - (06.12.2020)

## 🔨 Fixed
- (ae7d6ff8066cf2fe23b8f49758d2b62a516f5248) **cli**: working dir not available for module import

# v1.0.0b7 - (04.12.2020)

## 💌 Added
- (a941545bff360cf87211f821c85ba055d06f4378) **examples**: add echo example service
- (66c6022d34b10aac9459c4e4cff48baa302bc205) **server**: expose multiple config parameters to the `Server.run(...)` function
- (fc09853a843a8a7b812c1e7dc38cc961a6a430b9) **cli**: add a `morpho` cli command (is being used to start services from the comman line) and replaces `argparse` with `click`. Use `morpho --help`for a list of commands.
- (7d96dea6e0053b7ad3109c95a542751e2cb5962f) : add health endpoint for services `/health`
- (412c00f144a14eb9be156c4c3c7c9e2bf8b558b9) : a default config is now printable through `morpho config`

## ♻️ Changes
- (bd0471524a262c0e5bb459fd235f1ade99c4987f) **server**: remove argparse argument parsing
- (c8fe9dbb7651e9b5319d2675f4120a007b46406b) **config**: rename protocols parameter to consumers

# v1.0.0b6 - (20.09.2020)

## 🔨 Fixed
- (7e8a4a4e422a3a277f700e896f563c2f8dedaef9) **consumer**: always compare to upper instance name to prevent request deadlock

# v1.0.0b5 - (20.09.2020)

## 🔨 Fixed
- (d8bb5a7ca58ac7b466ea0cda54745d6776735658) **server**: custom config is not being used

# v1.0.0b4 - (20.09.2020)

## 💌 Added
- (96ee82a2e0cb87fa9ebf8caec301c6cf25ec395b) **consumer**: add overridable `_get_applications` function on WorkConsumer
- (2f4384331bd0815bb178b0fc870738ace37dfa2d) **consumer**: add RestGatewayServiceConfig class

## ♻️ Changes
- (9457b144d62c383ea5c1a7074d0498fe7951450f) **consumer**: expose work, config, options_type parameters on RestWorkConsumer
- (7689df06340010c13f03a30663e84145f3f8a354) **consumer**: expose optional client parameter on WorkCosumer constructor
- (c8403aedcd6baf6c14f3a456b4ecb924f8ae8156) **consumer**: _major rewrite_ of `WorkConsumer.list_services`. It now fully respects gateways.

# v1.0.0b3 - (18.09.2020)

## 💌 Added
- (ff3c757fa3f2576a49cd869655e0622b80b7ea21): new error type NoWorkerFunctionError
- (81cad627cc9847327523428802eec57324eed1c5) **consumer**: list services will resolve a gateway and return options for each service
- (ce9cbb34133432e22315ae331db518eb69ca4d22) **work_consumer**: add tests for WorkConsumer abstract class

## ♻️ Changes
- (f986549f8a3fb9a97076dcd981a68d76fb73a796): expose register parameter to Service class constructor

## 🔨 Fixed
- (e1da287eec8f5792978ad8da22095714b3189fd2): dtaType not visible in eureka's metadata

# v1.0.0b2 - (17.09.2020)

## 💌 Added
- (71e495cbdbe7317378bd329bc4aba939c74dd56f) **consumer**: new gateway rest consumer
- (f2cdc10d2f4b15ea264a29ffc568c771c482e720) **unit**: add unit tests for the client
- (d08ede25ed548868c8ad03e3525f56543f06c611) **client**: every client function has an optional `instance_address` parameter
- (1352bbdf501ba9dd313d2731b842e010999d45e6): implement Document Transformation Application Types (DtaType)

## ♻️ Changes
- (1f1ad176317090b8e098abbba4300337751351e4) **examples**: remove deprecated `worker` decorator
- (84e1a8eb71a87209aa9b8f3ead220a9cd7b18346) **server**: make worker function optional

# v1.0.0b1 - (08.09.2020)

## 🔥 BREAKING CHANGES
- removed proto dependencies and files
- removed worker decorator

## 💌 Added
- (d5d217a4b735ddbbb96d07b2f5be08bd71e974fc): information section about how to create a new release (closes: #24)
- (d111c810b2f784dad568afed8ab92020eaa6f571) **consumer**: implement options rest endpoint (closes: #23)
- (a44721ab171fe2c78cc54ed59cf91e44f62fcdb6) **consumer**: improved documentation of functions
- (5104a8bac5dc3b408f3968dcc012c755ebc43c42) **openapi**: new openapi specification
- (d7552cc7f355f1ee47fd226608b5aaf5883c59a3) **sphinx**: sphinx documentation

## ♻️ Changes
- (9dac3a61f2748bca7843c6f69b8a84f77cd5962b) **examples**: all examples now uses the public morpho repository
- (d996ec6bf1b0a5e24a55262831fd078281cd6cfb): remove unused dependencies (closes: #7)
- (84fe09f9e13b78cf01657ae1a89c128a17805267) **proto**: remove proto files 
- (6bd16587b568e14869d949ba9e8c2c0e444bb74d) **tasks**: remove grpc relavant tasks
- (8c32d5fdcb93dff7964b55d4bf04c49c37ade69a): remove proto from docs
- (15a0cd9a8153c23808e001be9676d6b5754ca732) **server**: remove worker decorator

## 🔨 Fixed
- (c5cd08546a5cfc9e4cdd3b8a3cfb7d95cfa43daf) **consumer**: missing Dict type import
- (8693688233f2f0f4799197198a7108c549858607) **circleci**: codecov uses the wrong package directory


# v1.0.0a5 - (16.07.2020)

## 🔨 Fixed
- (593377e57c2f3d447fa826c53c32d41b15fed3bb) **types**: make callable's worker BaseModel not optional 

# v1.0.0a4 - (16.07.2020)

## 💌 Added
- (67da16e8d199df69bb95dda6c9b0d0de513b0a28) **examples**: gateway example to crypto 

## 🔨 Fixed
- (5c96cab81c9c16c0584006e45bcf54ef80a7d595) **consumer**: wrong dict convert function was used in transform pipe 
- (a3e77a982cc9db1fb4551b174ae8fd327c189b39) **client**: wrong json convert function was used in transform pipe

# v1.0.0a3 - (10.06.2020)

## 🔨 Fixed
- (de07dde9c9670732b64db656dfe0956b98087209): worker signature allowing optional BaseModel
- (309e20e5c35a984de2aa972f1f2327bc268a440d): supressed error which was raised by not converting the options dict to the options BaseModel
- (d4498f37e2711cb588afcf6c83b945249b4283bd): is_byte64_encoded variable still being used and caused crashes

# v1.0.0a2 - (07.06.2020)

## 💌 Added
- (70a86dc113f79d0e7a040b866a372a67b49fe659): changelog

## ♻️ Changed
- (caec7a7c2cc8a17149cb43738b824ce50dae91c3): temporarily remove grpcio depencdency until it is fully integrated
- (0462b568838be04a855ee18de04785c892c3a60d) **examples**: remove client examples which where based on grpcio

## 🔨 Fixed
- (d5b34e18467dbb14e0c54ad4a5e36fa1e2a908d9) **client**: pydantic conversion functions not being used
- (cef3b8ddce6a6755624cc709030c0805d684477d) **models**: wrong type for options property

# v1.0.0a1 - (03.06.2020)

## Initial Release