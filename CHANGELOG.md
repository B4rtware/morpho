# v1.0.0a4 - (16.07.2020)

## 💌 Added
- added(**examples**): gateway example to crypto (67da16e8d199df69bb95dda6c9b0d0de513b0a28)

## 🔨 Fixed
- fixed(**consumer**): wrong dict convert function was used in transform pipe
- fixed(**client**): wrong json convert function was used in transform pipe (a3e77a982cc9db1fb4551b174ae8fd327c189b39)

# v1.0.0a3 - (10.06.2020)

## 🔨 Fixed
- fixed: worker signature allowing optional BaseModel (de07dde9c9670732b64db656dfe0956b98087209)
- fixed: supressed error which was raised by not converting the options dict to the options BaseModel (309e20e5c35a984de2aa972f1f2327bc268a440d)
- fixed: is_byte64_encoded variable still being used and caused crashes (d4498f37e2711cb588afcf6c83b945249b4283bd)

# v1.0.0a2 - (07.06.2020)

## 💌 Added
- added: changelog

## ♻️ Changed
- changed: temporarily remove grpcio depencdency until it is fully integrated
- changed(**examples**): remove client examples which where based on grpcio

## 🔨 Fixed
- fixed(**client**): pydantic conversion functions not being used
- fixed(**models**): wrong type for options property

# v1.0.0a1 - (03.06.2020)

## Initial Release