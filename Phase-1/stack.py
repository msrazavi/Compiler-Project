class Stack:
    def __init__(self):
        self.elements = []

    def push(self, x):
        self.elements.append(x)

    def pop(self):
        return self.elements.pop()

    def top(self):
        return self.elements[-1]

    def __str__(self):
        return str([str(e) for e in self.elements])
