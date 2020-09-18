from base64 import b64decode, b64encode
from typing import Any, Dict, List, Tuple


def encode_base64(string: str, encoding: str = "utf-8") -> str:
    return b64encode(string.encode(encoding)).decode(encoding)


def decode_base64(string: str, encoding: str = "utf-8") -> str:
    return b64decode(string.encode(encoding)).decode(encoding)


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
        if char[0] * len(char) == "".join(char):
            index += 1

    if index != 0:
        prefix = keys[0][: index - 1]

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


# from threading import Thread

# import asyncio

# def run_until_timeout(func, timeout):
#     result_queue = Queue()
#     worker_process = Process(target=worker, args=(func, result_queue), daemon=True)
#     worker_process.start()
#     worker_process.join(timeout)
#     if worker_process.is_alive():
#         worker_process.terminate()
#         worker_process.join()
#         # if worker_process.is_alive():
#         #     raise Exception("worker is still alive")
#         raise ServerTimeout()
#     if not result_queue.empty():
#         print(result_queue.get())


# def test():
#     for i in range(10):
#         print("sleeping")
#         time.sleep(1)
#     return "result"

# def run_func(func):
#     with ThreadPoolExecutor(max_workers=2) as pool:
#         result = pool.submit(func)
#         result.result(5)
#         pool.shutdown(False)
#         pool.shutdown()
#         print("shuedown")
#         # print(result.cancel())
#         # print(result.set_exception(Exception("Timeout")))


# def run_until_timeout(func, timeout):
#     run_func(func)
#     print("DONE")


# def worker(func, queue):
#     result = func()
#     queue.put(result)

# if __name__ == "__main__":
#     run_until_timeout(test, 10)
# worker_process = Process(target=test, daemon=True)
# worker_process.start()
# worker_process.join(5)
# if worker_process.is_alive():
#     worker_process.terminate()
#     if worker_process.is_alive():
#         raise Exception("worker is still alive")
#     raise ServerTimeout()

