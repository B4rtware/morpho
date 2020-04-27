from typing import Any, Dict, List, Tuple
import regex

# TODO: complete the example
def flatten_dict(dictionary: Dict[str, Any], prefix: str = ""):
    """Transforms a given dictionary into a flattened key value dictionary.

    Example:

        >>> from pprint import pprint
        >>> options = {
            "debug": True,
            "user": {
                "first_name": "Jon",
                "last_name": "Doe"
            },
            "offset": 7
        }
        >>> pprint(explode_dict(options))
    """
    exploded_options = {}
    stack: List[Tuple[str, List[Any]]] = [(prefix, list(dictionary.items()))]
    while stack[0][1] != []:
        prefix, value = stack[0][1].pop(0)

        if isinstance(value, dict):
            stack.insert(0, (prefix, list(value.items())))
        else:
            prefixes = [elem[0] for elem in reversed(stack) if elem[0]]
            prefixes.append(prefix)
            prefix_str = ".".join(prefixes)
            exploded_options[prefix_str] = value

    return exploded_options

# TODO: remove any its everything except another dict
def unflatten_dict(dictionary: Dict[str, Any]):
    keys = list(dictionary.keys())
    # get prefix
    prefix = None

    index = 0
    for char in zip(*keys):
        if (char[0] * len(char) == "".join(char)):
            index += 1

    if index != 0:
        prefix = keys[0][:index-1]

    # get dict
    unflatten_dict = {}
    for key in keys:
        # TODO: optimize this
        # remove prefix from key
        value = dictionary[key]
        if prefix:
            key = key.split(prefix)[1][1:]
        prefixes = key.split(".")

        cur_dict = unflatten_dict
        cur_prefix = prefixes.pop()
        # proceed to the nested dictionary
        for pkey in prefixes:
            if cur_dict.get(pkey) is None:
                cur_dict[pkey] = {}
            cur_dict = cur_dict[pkey]

        cur_dict[cur_prefix] = value
    return prefix, unflatten_dict
        