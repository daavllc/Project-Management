from cui.utils import Pause

class Command:
    def __init__(self, keys: list[list[type]], help: str, callback):
        self.keys = keys
        self.help = help
        self.callback = callback
        
    def __str__(self):
        return self.help

    def Check(self, cmd) -> bool:
        for key in self.keys:
            if cmd == key:
                self.callback()
                return True
            else:
                if '**' in key:
                    index = key.index('**')
                    if [val for val in cmd[:index]] == [val for val in key[:index]]:
                        self.callback([val for val in cmd[index:]])
                        return True
                elif '*' in key:
                    anyIndexes = [i for i in range(len(key)) if key[i] == '*']
                    setIndexes = [i for i in range(len(key)) if i not in anyIndexes]
                    if len(key) == len(cmd):
                        if [cmd[x] for x in setIndexes] == [key[x] for x in setIndexes]:
                            self.callback([cmd[x] for x in anyIndexes])
                            return True
        return False
        
    def GetKeysAsStr(self) -> str:
        keys = ""
        for i, key in enumerate(self.keys):
            for j, value in enumerate(key):
                keys += value
                if j < len(key) - 1:
                    keys += " "
            if i < len(self.keys) - 1:
                keys += " | "
        return keys

class Group:
    def __init__(self, name: str, description: str, fallback: str = None):
        self.name = name
        self.description = description
        self.commands = []
        self.fallback = fallback

    def Add(self, keys: list[list[type]], help: str, callback):
        self.commands.append(Command(keys, help, callback))

    def Check(self, ui: str) -> bool:
        for cmd in self.commands:
            if cmd.Check(ui):
                return True
        if not self.fallback is None:
            print(f"{self.fallback}")
        return False

    def PrintHelp(self, indent: str = "\t"):
        print(f"{indent}{self.name}")
        print(f"{indent * 2} {self.description}")
        for cmd in self.commands:
            print(f"{indent}{cmd.GetKeysAsStr()}")
            print(f"{indent * 2}{cmd.help}")

class CommandParse:
    def __init__(self, name: str, description: str, fallback: str = None):
        self.name = name
        self.description = description
        self.groups = {}
        self.fallback = fallback

    def AddGroup(self, name: str, description: str) -> Group:
        self.groups[name] = Group(name, description)
        return self.groups[name]

    def Check(self, message: str = "Enter a command > ", splitter: str = " ") -> bool:
        ui = input(message).split(" ")
        for group in self.groups.values():
            if group.Check(ui):
                return True
        if not self.fallback is None:
            print(f"{self.fallback}")
        return False

    def PrintHelp(self, indent: str = "  "):
        print(f"{indent}{self.name}")
        print(f"{indent * 2} {self.description}")
        print(f"{indent}-------------------------")
        for group in self.groups.values():
            group.PrintHelp(indent)
            print(f"{indent}----")
        Pause()