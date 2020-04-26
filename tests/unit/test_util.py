from morpho.util import flatten_dict, unflatten_dict


class TestFlattenDict():
    
    def test_flat_no_prefix(self):
        # fmt: off
        options = {
            "debug": True,
            "offset": 12,
            "type": "service",
            "array": [1,2,3,4]
        }

        f_dict = flatten_dict(options)
        assert f_dict == {
            "debug": True,
            "offset": 12,
            "type": "service",
            "array": [1,2,3,4]
        }
        # fmt: on

    def test_flat_with_prefix(self):
        # fmt: off
        options = {
            "debug": True,
            "offset": 12,
            "type": "service",
            "array": [1,2,3,4]
        }

        f_dict = flatten_dict(options, "morpho")
        assert f_dict == {
            "morpho.debug": True,
            "morpho.offset": 12,
            "morpho.type": "service",
            "morpho.array": [1,2,3,4]
        }
        # fmt: on

    def test_nested_no_prefix(self):
        options = {
            "debug": False,
            "credentials": {
                "username": "klaus",
                "password": "2321"
            }
        }

        f_dict = flatten_dict(options)
        assert f_dict == {
            "debug": False,
            "credentials.username": "klaus",
            "credentials.password": "2321"
        }

    def test_nested_with_prefix(self):
        options = {
            "length": 34,
            "aws": {
                "version": "1.10",
                "message": "Hello World!",
                "output": {
                    "lines": 20
                }
            }
        }

        f_dict = flatten_dict(options, "morpho")
        assert f_dict == {
            "morpho.length": 34,
            "morpho.aws.version": "1.10",
            "morpho.aws.message": "Hello World!",
            "morpho.aws.output.lines": 20
        }

class TestUnflattenDict():
    def test_flat_no_prefix(self):
        options = {
            "username": "Peter",
            "password": "secret",
            "length": 12
        }

        prefix, uf_dict = unflatten_dict(options)
        assert prefix == None
        assert uf_dict == options

    def test_flat_prefix(self):
        options = {
            "morpho.username": "Peter",
            "morpho.password": "secret",
            "morpho.length": 13
        }
        prefix, uf_dict = unflatten_dict(options)
        assert prefix == "morpho"
        assert uf_dict == {
            "username": "Peter",
            "password": "secret",
            "length": 13
        }

    def test_flat_multi_prefix(self):
        options = {
            "morpho.options.username": "Hans",
            "morpho.options.password": "secret",
            "morpho.options.length": 23
        }
        prefix, uf_dict = unflatten_dict(options)
        assert prefix == "morpho.options"
        assert uf_dict == {
            "username": "Hans",
            "password": "secret",
            "length": 23
        }

    def test_nested_no_prefix(self):
        options = {
            "debug": False,
            "credentials.username": "klaus",
            "credentials.password": "2321"
        }
        prefix, dictionary = unflatten_dict(options)
        assert prefix == None
        assert dictionary == {
            "debug": False,
            "credentials": {
                "username": "klaus",
                "password": "2321"
            }
        }

    def test_nested_multi_prefix(self):
        options = {
            "morpho.debug": True,
            "morpho.credentials.account.username": "Niem",
            "morpho.credentials.type": "hash",
            "morpho.not": True
        }
        prefix, dictionary = unflatten_dict(options)
        assert prefix == "morpho"
        assert dictionary == {
            "debug": True,
            "credentials": {
                "account": {
                    "username": "Niem"
                },
                "type": "hash"
            },
            "not": True
        }

