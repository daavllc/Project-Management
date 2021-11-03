class Entry:
    def __init__(self, data):
        self.Data = data

    def __str__(self) -> str:
        return str(self.Data)

    def Get(self):
        return self.Data

    def Set(self, data):
        self.Data = data