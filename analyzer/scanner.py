import ply.lex as lex
import re

# Lista de tokens
tokens = [
    "ID",
    "INT",
    "FLOAT",
    "STRING",
    "CHAR",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULE",
    "OR",
    "AND",
    "NOT",
    "LTHAN",
    "LORE",
    "GTHAN",
    "GORE",
    "EQUALS",
    "NEQUALS",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "DOT",
    "COLON",
    "SEMICOLON",
    "EQUAL",
    "AMPERSAND",
    "LCBRACKET",
    "RCBRACKET",
    "PIPE",
    "ARROW",
    "ARROW2",
    "DCOLON",
]

reserved = {
    "true": "RTRUE",
    "false": "RFALSE",
    "to_string": "RTOSTRING",
    "to_owned": "RTOOWNED",
    "i64": "RINT",
    "f64": "RFLOAT",
    "bool": "RBOOL",
    "char": "RCHAR",
    "str": "RSTR",
    "String": "RSTRING",
    "usize": "RUSIZE",
    "let": "RLET",
    "mut": "RMUT",
    "as": "RAS",
    "if": "RIF",
    "else": "RELSE",
    "match": "RMATCH",
    "_": "UNDERSCORE",
    "while": "RWHILE",
    "loop": "RLOOP",
    "for": "RFOR",
    "in": "RIN",
    "break": "RBREAK",
    "continue": "RCONTINUE",
    "return": "RRETURN",
    "fn": "RFN",
    "println": "RPRINTLN",
    "abs": "RABS",
    "sqrt": "RSQRT",
    "pow": "RPOW",
    "powf": "RPOWF",
    "len": "RLEN",
}

tokens += list(reserved.values())

# Tokens

# Aritmeticos
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MODULE = r"\%"

# Logicos
t_OR = r"\|\|"
t_AND = r"\&\&"
t_NOT = r"\!"

# Relacionales
t_LTHAN = r"<"
t_LORE = r"<="
t_GTHAN = r">"
t_GORE = r">="
t_EQUALS = r"=="
t_NEQUALS = r"\!\="

# Signos
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMMA = r"\,"
t_DOT = r"\."
t_EQUAL = r"="
t_COLON = r"\:"
t_SEMICOLON = r"\;"
t_LCBRACKET = r"\{"
t_RCBRACKET = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_DCOLON = r"\:\:"
t_AMPERSAND = r"\&"
t_ARROW = r"=>"
t_ARROW2 = r"->"
t_PIPE = r"\|"


def t_FLOAT(t):
    r"\d+\.\d+"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_INT(t):
    r"\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# fmt:off
def t_STRING(t):
    r"\".*?\""
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


def t_CHAR(t):
    r"\'((\\)?(.{1}?))\'"
    return t
# fmt:on


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t


def t_multiline_comment(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")


def t_simple_comment(t):
    r"//.*\n"
    t.lexer.lineno += 1


# Ignored characters
t_ignore = " \t\r"

# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind("\n", 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
lexer = lex.lex()
