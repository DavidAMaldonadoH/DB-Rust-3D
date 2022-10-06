from enum import Enum


class Type(Enum):
    Int = 0, "integer"
    I64 = 1, "i64"
    F64 = 2, "f64"
    Bool = 3, "bool"
    Char = 4, "char"
    Str = 5, "&str"
    String = 6, "String"
    Usize = 7, "usize"
    Array = 8, "Array"
    Vector = 9, "Vector"
    Struct = 10, "Struct"
    Null = 11, "Null"
    Void = 12, "void"

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return self.value
