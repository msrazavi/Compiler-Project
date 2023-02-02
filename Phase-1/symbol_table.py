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

    def __str__(self):
        return f"{self.name}, " \
               f"{self.type}, " \
               f"{'func' if self.is_func else ('arr' if self.is_arr else 'var')}, " \
               f"scope={self.scope}, " \
               f"size={self.size}"


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

    def index_of(self, name: str, scope: int) -> Optional[int]:
        for i, e in enumerate(self.elements):
            if e.name == name and e.scope == scope:
                return i
        return None

    def __str__(self):
        return str([str(e) for e in self.elements])
