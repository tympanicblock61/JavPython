class Token:
    def __init__(self, position: int, line_num: int, value: str):
        self.position = position
        self.line_num = line_num
        self.value = value

    def __repr__(self):
        attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"


# pseudo tokens

class EndOfFileToken(Token):
    def __init__(self, position: int, line_num: int):
        super().__init__(position, line_num, None)


class WhiteSpaceToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


class SemiColonToken(Token):
    def __init__(self, position: int, line_num: int):
        super().__init__(position, line_num, ";")


class CommaToken(Token):
    def __init__(self, position: int, line_num: int):
        super().__init__(position, line_num, ",")


# String, Numbers

class NumberToken(Token):
    def __init__(self, position: int, line_num: int, value: str, parsed):
        super().__init__(position, line_num, value)
        self.parsed = parsed


class FloatToken(NumberToken):
    def __init__(self, position: int, line_num: int, value: str, parsed: float):
        super().__init__(position, line_num, value, parsed)


class DoubleToken(NumberToken):
    def __init__(self, position: int, line_num: int, value: str, parsed: float):
        super().__init__(position, line_num, value, parsed)


class StringToken(Token):
    def __init__(self, position: int, line_num: int, value: str, str_type:str, parsed: str):
        super().__init__(position, line_num, value)
        self.type = str_type
        self.real = parsed


class IntToken(NumberToken):
    def __init__(self, position: int, line_num: int, value: str, parsed: int):
        super().__init__(position, line_num, value, parsed)


# comments

class MultiLineCommentToken(Token):
    def __init__(self, position: int, line_num: int, value: str, lines: [str]):
        super().__init__(position, line_num, value)
        self.lines = lines


class CommentToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


# brackets, (), {}, []

class RoundBracketToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


class CurlyBracketToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


class SquareBracketToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


# ids, mods, functions, etc

class IdentifierToken(Token):
    def __init__(self, position: int, line_num: int, value: str):
        super().__init__(position, line_num, value)


__all__ = ["Token", "EndOfFileToken", "WhiteSpaceToken", "NumberToken", "FloatToken", "DoubleToken", "IntToken",
           "MultiLineCommentToken", "CommentToken", "RoundBracketToken", "CurlyBracketToken", "SquareBracketToken",
           "IdentifierToken", "SemiColonToken", "CommaToken", "StringToken"]
