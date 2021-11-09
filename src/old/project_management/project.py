from .column import Column

class Project:
    def __init__(self, name: str) -> None:
        self.name = name
        self.columns = []

    def __str__(self) -> str:
        return f"Project {self.name} with {len(self.columns)} columns"

    def __len__(self) -> int:
        return len(self.columns)

    def Push(self, name: str) -> None:
        self.columns.append(Column(name))

    def Pop(self, pos: int = -1):
        self.columns.pop(pos)

    def GetLargestColumn(self) -> int:
        size = 0
        for column in self.columns:
            if len(column) > size:
                size = len(column)
        return size

    def Get(self, column: int, entry: int):
        if entry > len(self.columns[column]) - 1:
            return ""
        else:
            return self.columns[column].entries[entry]