from parse_tree_node import Node


class Stack:
    def __init__(self):
        self.elements = []

    def push(self, x):
        self.elements.append(x)

    def pop(self):
        return self.elements.pop()

    def multipop(self, n: int):
        for i in range(n):
            self.pop()

    def __getitem__(self, item):
        if item <= 0: return self.elements[item - 1]
        return self.elements[item]

    def __setitem__(self, key, value):
        if key <= 0:  self.elements[key - 1] = value
        self.elements[key] = value

    def top(self):
        return self.elements[-1]

    def __str__(self):
        return str(
            [(str(e.name[2]) if isinstance(e.name, tuple) else str(e.name)) if isinstance(e, Node) else str(e) for e in
             self.elements])
