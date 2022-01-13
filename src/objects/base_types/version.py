# Project-Management.objects.base_types.version - Class for easy to use version control
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

class Version:
    class Errors:
        class InvalidInitializationArgs(Exception):
            def __init__(self, message: str = "Invalid initalization arguments provided"):
                super().__init__(message)
        class InvalidVersionString(Exception):
            def __init__(self, message: str = "Invalid version string provided"):
                super().__init__(message)
        class UnsupportedOperator(Exception):
            def __init__(self, message: str = "Unsupported operation"):
                super().__init__(message)

    def __init__(self, *args): # Takes int, int, int or str
        if len(args) == 3:
            for arg in args:
                if not type(arg) == int:
                    self.Errors.InvalidVersionString(f"Invalid initalization argument provided: {str(arg)}")
            self.FromInts(args[0], args[1], args[2])
        elif len(args) == 1:
            if not type(args[0]) == str:
                self.Errors.InvalidInitializationArgs(f"Invalid initalization arguments provided: {str(args)}")
            self.FromStr(args[0])
        else:
            self.FromInts(0, 0, 0)

    def FromInts(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def FromStr(self, version: str) -> None:
        vlist = version.split('.')
        if len(vlist) > 3:
            raise self.Errors.InvalidVersionString(f"Invalid version string provided: {version}")
        while len(vlist) < 3:
            vlist.append("0")

        try:
            self.major = int(vlist[0])
            self.minor = int(vlist[1])
            self.patch = int(vlist[2])
        except ValueError:
            raise self.Errors.InvalidVersionString(f"Invalid version string provided: {version}")

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self):
        return not(self.major == None or self.minor == None or self.patch == None)

    def __int__(self):
        return self.major, self.minor, self.patch

    def __and__(self, other):
        return self.__bool__() and other.__bool__()

    def __or__(self, other):
        return self.__bool__() or other.__bool__()

    def __add__(self, other):
        return Version(self.major + other.major, self.minor + other.minor, self.patch + other.patch)

    def __IADD__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Version(self.major - other.major, self.minor - other.minor, self.patch - other.patch)

    def __ISUB__(self, other):
        self.__sub__(other)

    def __lt__(self, other):
        if self.major < other.major:
            return self.major < other.major
        elif self.minor < other.minor:
            return self.minor < other.minor
        elif self.patch < other.patch:
            return self.patch < other.patch

    def __le__(self, other):
        if self.major <= other.major:
            return self.major <= other.major
        elif self.minor <= other.minor:
            return self.minor < other.minor
        elif self.patch <= other.patch:
            return self.patch <= other.patch

    def __gt__(self, other):
        if self.major > other.major:
            return self.major > other.major
        elif self.minor > other.minor:
            return self.minor > other.minor
        elif self.patch > other.patch:
            return self.patch > other.patch

    def __ge__(self, other):
        if self.major >= other.major:
            return self.major >= other.major
        elif self.minor >= other.minor:
            return self.minor >= other.minor
        elif self.patch >= other.patch:
            return self.patch >= other.patch

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __ne__(self, other):
        return not self.__eq__(other)

    # Unsupported operations
    def __mul__(self, other):
        return NotImplemented
    def __matmul__(self, other):
        return NotImplemented
    def __truediv__(self, other):
        return NotImplemented
    def __floordiv__(self, other):
        return NotImplemented
    def __mod__(self, other):
        return NotImplemented
    def __divmod__(self, other):
        return NotImplemented
    def __pow__(self, other):
        return NotImplemented
    def __xor__(self, other):
        return NotImplemented
    def __neg__(self):
        return NotImplemented
    def __pos__(self):
        return NotImplemented
    def __abs__(self):
        return NotImplemented
    def __invert__(self):
        return NotImplemented
    def __complex__(self):
        return NotImplemented
    def __float__(self):
        return NotImplemented

    # ---============================================================---
    #               Version Getters/Setters
    # ---============================================================---
    def GetMajor(self) -> int:
        return self.major

    def GetMinor(self) -> int:
        return self.minor

    def GetPatch(self) -> int:
        return self.patch

    def SetMajor(self, major: int) -> None:
        self.major = major

    def SetMinor(self, minor: int) -> None:
        self.minor = minor

    def SetPatch(self, patch: int) -> None:
        self.patch = patch