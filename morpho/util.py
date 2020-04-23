from typing import Any, Dict, List, Tuple

# TODO: complete the example
def explode_dict(dictionary: Dict[str, Any]):
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
    stack: List[Tuple[str, List[Any]]] = [("morpho.option", list(dictionary.items()))]
    while stack:
        cur = stack[0][1].pop(0)

        if isinstance(cur[1], dict):
            stack.insert(0, (cur[0], list(cur[1].items())))
        else:
            prefix = ".".join([elem[0] for elem in reversed(stack)]) + "." + cur[0]
            exploded_options[prefix] = cur[1]

        if stack[0][1] == []:
            stack.pop(0)
    return exploded_options