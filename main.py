import textwrap

from tokens import *


class char(str):
    def __new__(cls, s):
        if len(s) > 1:
            raise ValueError("Only one character")
        return super(char, cls).__new__(cls, s)


class Lexer:
    def __init__(self, text: str):
        self._text = text
        self._position = 0
        # TODO optimize get line to actually check if new line on inc

    def current(self) -> char:
        if self._position >= len(self._text):
            return char('\0')

        return char(self._text[self._position])

    def inc(self):
        self._position += 1

    def dec(self):
        self._position -= 1

    def get_line(self, position: int):
        return self._text[:position].count("\n") + 1

    def next_token(self) -> Token:
        if self.current() == "\0":
            return EndOfFileToken(len(self._text), self.get_line(len(self._text)))
        elif self.current().isspace():
            white_space = WhiteSpaceToken(self._position, self.get_line(self._position), self._text[self._position])
            self.inc()
            return white_space
        elif self.current().isdigit():
            start = self._position
            line = self.get_line(start)

            while self.current().isdigit() or self.current() == ".":
                self.inc()

            is_float = self.current().lower() == "f"
            if is_float:
                self.inc()

            value = self._text[start:self._position]

            self.inc()
            if is_float:
                return FloatToken(start, line, value, float(value[:-1]))
            elif "." in value:
                # TODO handle the d
                return DoubleToken(start, line, value, float(value))
            else:
                return IntToken(start, line, value, int(value))
        elif self.current() == "/":
            start = self._position
            line = self.get_line(start)

            self.inc()
            if self.current() == "/":
                while self.current() != "\n" and self._position < len(self._text):
                    self.inc()
                value = self._text[start:self._position]
                self.inc()
                return CommentToken(start, line, value[2:])
            elif self.current() == "*":
                current_t = self.current()
                next_t = self._text[self._position + 1] if self._position + 1 < len(self._text) else ''
                while not (current_t == "*" and next_t == "/") and self._position < len(self._text) - 1:
                    self.inc()
                    current_t = self.current()
                    next_t = self._text[self._position + 1] if self._position + 1 < len(self._text) else ''

                if current_t == "*" and next_t == "/":
                    self.inc()
                    self.inc()

                value = self._text[start:self._position]
                self.inc()
                return MultiLineCommentToken(start, line, value, value[2:-2].split("\n"))
        elif self.current().isalpha():
            start = self._position
            while self.current().isalnum() or self.current() in "_.":
                self.inc()

            value = self._text[start:self._position]
            return IdentifierToken(start, self.get_line(start), value)
        elif self.current() in "[](){}":
            start = self._position
            line = self.get_line(start)
            cur = self.current()
            self.inc()
            if cur in "[]":
                return SquareBracketToken(start, line, cur)
            elif cur in "()":
                return RoundBracketToken(start, line, cur)
            elif cur in "{}":
                return CurlyBracketToken(start, line, cur)
        elif self.current() == ";":
            start = self._position
            line = self.get_line(start)
            self.inc()
            return SemiColonToken(start, line)
        elif self.current() == ",":
            start = self._position
            line = self.get_line(start)
            self.inc()
            return CommaToken(start, line)
        elif self.current() == "'" or self.current() == '"':
            str_type = self.current()
            start = self._position
            line = self.get_line(start)
            self.inc()

            value = []
            while self.current() != str_type and self._position < len(self._text):
                if self.current() == '\\':
                    self.inc()
                    if self.current() in ['"', "'", '\\']:
                        value.append(self.current())
                    elif self.current() == 'n':
                        value.append('\n')
                    elif self.current() == 't':
                        value.append('\t')
                else:
                    value.append(self.current())
                self.inc()

            if self.current() == str_type:
                self.inc()

            value = ''.join(value)
            return StringToken(start, line, value, str_type, value[1:-1])
        else:
            self.inc()


def transpiler(tokens: [Token]):
    source = ""
    for token in tokens:
        if isinstance(token, MultiLineCommentToken):
            for line in token.lines:
                if line.startswith("*"):
                    source += f"#{line[1:]}\n"
                elif line.startswith(" *"):
                    source += f"#{line[2:]}\n"
                else:
                    source += f"#{line}\n"
        if isinstance(token, CommentToken):
            source += f"#{token.value}\n"

        # TODO trans javadoc to pydoc
    return source

if __name__ == "__main__":
    example_code = textwrap.dedent(
        """
        /**
         * The Person class represents a person with a name and age.
         * It includes basic functionality to get and set these fields,
         * as well as a method to display the person as a string.
         * 
         * Example usage:
         * - Creating a new Person object
         * - Accessing and modifying the fields
         * - Printing the object's representation
         */
        public class Person {
            // Fields
            private String name;
            private int age;
        
            // Constructor
            public Person(String name, int age) {
                this.name = name;
                this.age = age;
            }
        
            // Getter for name
            public String getName() {
                return name;
            }
        
            // Setter for name
            public void setName(String name) {
                this.name = name;
            }
        
            // Getter for age
            public int getAge() {
                return age;
            }
        
            // Setter for age
            public void setAge(int age) {
                this.age = age;
            }
        
            // Method to return a string representation of the object
            @Override
            public String toString() {
                return "Person{name='" + name + "', age=" + age + "}";
            }
        
            // Main method for testing
            public static void main(String[] args) {
                // Create a new Person object
                Person person = new Person("Alice", 30);
        
                // Access the object's fields
                System.out.println("Name: " + person.getName());
                System.out.println("Age: " + person.getAge());
        
                // Modify the object's fields
                person.setName("Bob");
                person.setAge(25);
        
                // Print the modified object
                System.out.println(person);
            }
        }"""
    ).removeprefix("\n")


    def nth_occurrence(s, char, n):
        start = -1
        for _ in range(n):
            start = s.find(char, start + 1)
            if start == -1:
                return -1
        return start


    def getLine(line):
        line_start = nth_occurrence(example_code, "\n", line - 1)
        line_end = nth_occurrence(example_code, '\n', line)
        return example_code[line_start:line_end]


    lexer = Lexer(example_code)
    tokens = []
    token = None
    while not isinstance(token, EndOfFileToken):
        token = lexer.next_token()
        print(token)
        tokens.append(token)

    print(transpiler(tokens))