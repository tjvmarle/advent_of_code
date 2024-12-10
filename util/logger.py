import inspect


indent_map = {}


def set_log(id: int = 0, indent_str: str = "  "):
    global indent_map
    indent_map[id] = (len(inspect.stack()), indent_str)


def log(txt: str, id: int = 0):
    stack_base, indent = indent_map.get(id, (None, None))

    if stack_base is None:
        print(f"ERROR: id {id} is unknown.")
        raise KeyError

    offset = len(inspect.stack()) - stack_base
    print(f"{indent * offset}{txt}")
