
# TODO: test on false parameter types?


# class TestBaseConfig():
#     def test_as_json(self):
#         config = BaseConfig(config_file="./dts/config.json")
#         string = config.as_json()
#         assert string == '{"config_file": "./dts/config.json"}'

#     def test_as_dict(self):
#         config = BaseConfig(config_file="./path/to/config.json")
#         assert config.as_dict() == {"config_file": "./path/to/config.json"}

#     def test_save(self):
#         buffer = io.StringIO()
#         config = BaseConfig(config_file="")
#         config.save(buffer)
#         assert buffer.getvalue() == '{\n    "config_file": ""\n}'