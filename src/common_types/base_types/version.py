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
            raise self.Errors.InvalidInitializationArgs(f"Invalid initalization arguments provided: {str(args)}")

    def FromInts(self, release: int, major: int, minor: int) -> None:
        self.Release = release
        self.Major = major
        self.Minor = minor

    def FromStr(self, version: str) -> None:
        if version == None or version == "None.None.None":
            self.Release = None
            self.Major = None
            self.Minor = None
            return
        vstr = version.split('.')
        try:
            self.Release = int(vstr[0])
            self.Major = int(vstr[1])
            self.Minor = int(vstr[2])
        except ValueError:
            raise self.Errors.InvalidVersionString(f"Invalid version string provided: {version}")

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        if self.Release == None or self.Major == None or self.Minor == None:
            return "None"
        return f"{self.Release}.{self.Major}.{self.Minor}"

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self):
        return not(self.Release == None or self.Major == None or self.Minor == None)

    def __len__(self) -> int:
        tVal = 0
        if not self.Release == None:
            tVal += 1
        if not self.Major == None:
            tVal += 1
        if not self.Minor == None:
            tVal += 1
        return tVal

    def __int__(self):
        return self.Release, self.Major, self.Minor

    def __and__(self, other):
        return self.__bool__() and other.__bool__()

    def __or__(self, other):
        return self.__bool__() or other.__bool__()

    def __add__(self, other):
        return self.Release + other.Release, self.Major + other.Major, self.Minor + other.Minor

    def __sub__(self, other):
        return self.Release - other.Release, self.Major - other.Major, self.Minor - other.Minor

    def __lt__(self, other):
        if self.Release < other.Release:
            return self.Release < other.Release
        elif self.Major < other.Major:
            return self.Major < other.Major
        elif self.Minor < other.Minor:
            return self.Minor < other.Minor

    def __le__(self, other):
        if self.Release <= other.Release:
            return self.Release <= other.Release
        elif self.Major <= other.Major:
            return self.Major < other.Major
        elif self.Minor <= other.Minor:
            return self.Minor <= other.Minor

    def __gt__(self, other):
        if self.Release > other.Release:
            return self.Release > other.Release
        elif self.Major > other.Major:
            return self.Major > other.Major
        elif self.Minor > other.Minor:
            return self.Minor > other.Minor

    def __ge__(self, other):
        if self.Release >= other.Release:
            return self.Release >= other.Release
        elif self.Major >= other.Major:
            return self.Major >= other.Major
        elif self.Minor >= other.Minor:
            return self.Minor >= other.Minor

    def __eq__(self, other):
        return self.Release == other.Release and self.Major == other.Major and self.Minor == other.Minor

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
    def GetRelease(self) -> int:
        return self.Release

    def GetMajor(self) -> int:
        return self.Major

    def GetMinor(self) -> int:
        return self.Minor

    def SetRelease(self, release: int) -> None:
        self.Release = release

    def SetMajor(self, major: int) -> None:
        self.Major = major

    def SetMinor(self, minor: int) -> None:
        self.Minor = minor


    