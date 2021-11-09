from .entries.entry import Entry

class Column:
    def __init__(self, name: str) -> None:
        self.name = name
        self.entryType = None
        self.entries = []

    def __str__(self):
        return f"Column {self.name} with {len(self.entries)} entries"

    def __len__(self) -> int:
        return len(self.entries)

    def Push(self, value):
        self.entries.append(value)

    def Pop(self, pos: int = -1):
        return self.entries.pop(pos)

    def Get(self) -> list:
        return self.entries