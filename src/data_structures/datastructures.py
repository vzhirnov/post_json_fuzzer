class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def pop_all(self):
        r, self.items[:] = self.items[:], []
        return r

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)
