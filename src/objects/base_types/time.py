class Time:
    class Errors:
        class InvalidInitializationArgs(Exception):
            def __init__(self, message: str = "Invalid initalization arguments provided"):
                super().__init__(message)
        class InvalidTimeString(Exception):
            def __init__(self, message: str = "Invalid time string provided"):
                super().__init__(message)
        class UnsupportedOperator(Exception):
            def __init__(self, message: str = "Unsupported operation"):
                super().__init__(message)

    def __init__(self, *args):
        if type(args[0]) == int:
            for arg in args:
                if not type(arg) == int:
                    self.Errors.InvalidInitializationArgs(f"Invalid initalization argument provided: {str(arg)}")
            while len(args) < 3:
                args.append[0]
            self.FromInts(args[0], args[1], args[2])
        elif type(args[0]) == str and len(args) == 1:
            self.FromStr(args[0])
        else:
            self.Errors.InvalidInitializationArgs(f"Invalid initalization argument provided: {str(arg)}")

    def FromInts(self, hour: int, minute: int, second: int):
        self.hour = hour
        self.minute = minute
        self.second = second

    def FromStr(self, time: str):
        tlist = time.split('.')
        if len(tlist) > 3:
            raise self.Errors.InvalidTimeString(f"Invalid time string provided: {time}")
        while len(tlist) < 3:
            tlist.append("0")

        try:
            self.hour = int(tlist[0])
            self.minute = int(tlist[1])
            self.second = int(tlist[2])
        except ValueError:
            raise self.Errors.InvalidTimeString(f"Invalid time string provided: {time}")

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self):
        return f"{self.hour}.{self.minute}.{self.second}"

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return self.hour and self.minute and self.second

    def __int__(self):
        return self.hour, self.minute, self.second

    def __and__(self, other):
        return self.__bool__() and other.__bool__()

    def __or__(self, other):
        return self.__bool__() or other.__bool__()

    def __add__(self, other):
        return Time(self.hour + other.hour, self.minute + other.minute, self.second + other.second)

    def __IADD__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Time(self.hour - other.hour, self.minute - other.minute, self.second - other.second)

    def __ISUB__(self, other):
        self.__sub__(other)

    def __lt__(self, other):
        if self.hour < other.hour:
            return self.hour < other.hour
        elif self.minute < other.minute:
            return self.minute < other.minute
        elif self.second < other.second:
            return self.second < other.second

    def __le__(self, other):
        if self.hour <= other.hour:
            return self.hour <= other.hour
        elif self.minute <= other.minute:
            return self.minute < other.minute
        elif self.second <= other.second:
            return self.second <= other.second

    def __gt__(self, other):
        if self.hour > other.hour:
            return self.hour > other.hour
        elif self.minute > other.minute:
            return self.minute > other.minute
        elif self.second > other.second:
            return self.second > other.second

    def __ge__(self, other):
        if self.hour >= other.hour:
            return self.hour >= other.hour
        elif self.minute >= other.minute:
            return self.minute >= other.minute
        elif self.second >= other.second:
            return self.second >= other.second

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute and self.second == other.second

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
    #               Time Getters/Setters
    # ---============================================================---
    def GetHour(self) -> int:
        return self.hour

    def GetMinute(self) -> int:
        return self.minute

    def GetSecond(self) -> int:
        return self.second

    def SetHour(self, hour: int) -> None:
        self.hour = hour

    def SetMinute(self, minute: int) -> None:
        self.minute = minute

    def SetSecond(self, second: int) -> None:
        self.second = second