from typing import List, Optional


class Element:
    def __init__(self,
                 name: str = '',
                 type: str = '',
                 scope: int = '',
                 is_func: bool = False,
                 is_arr: bool = False,
                 size: int = 1):
        self.name = name
        self.type = type
        self.scope = scope
        self.is_func = is_func
        self.is_arr = is_arr
        self.is_var = not (is_func or is_arr)
        self.size = size


class SymbolTable:
    elements: List[Element] = []

    def declare(self, type: str, scope: int):
        self.elements.append(Element(type=type, scope=scope))

    def declare_name(self, name: str):
        self.elements[-1].name = name

    def declare_size(self, size: int):
        self.elements[-1].size = size

    def declare_func(self):
        self.elements[-1].is_func = True
        self.elements[-1].is_var = False

    def declare_arr(self):
        self.elements[-1].is_arr = True
        self.elements[-1].is_var = False

    def add_var(self, name: str, type: str, scope: int):
        self.elements.append(Element(name, type, scope))

    def add_func(self, name: str, type: str, scope: int, arg_count: int):
        self.elements.append(Element(name, type, scope, is_func=True, size=arg_count))

    def add_arr(self, name: str, type: str, scope: int, size: int):
        self.elements.append(Element(name, type, scope, is_arr=True, size=size))

    def index_of(self, name: str, scope: int) -> Optional[int]:
        for i, e in enumerate(self.elements):
            if e.name == name and e.scope == scope:
                return i
        return None
