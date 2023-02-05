class Node:
    name: str
    children = []
    parent = None

    def __init__(self, name: str = '', children=[], parent=None):
        self.name = name
        self.children = children
        self.parent = parent
