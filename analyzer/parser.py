import ply.yacc as yacc

from analyzer.scanner import tokens
from expression.Abs import Abs
from expression.Cast import Cast
from expression.Logic import Logic
from expression.Operation import Operation
from expression.Literal import Literal
from expression.Pow import Pow
from expression.Reference import Reference
from expression.SimpleAccess import SimpleAccess
from expression.Sqrt import Sqrt
from expression.ToString import ToString
from instruction.Assignation import Assignation
from instruction.Break import Break
from instruction.Case import Case
from instruction.Continue import Continue
from instruction.Declaration import Declaration
from instruction.Default import Default
from instruction.For import For
from instruction.FunctionDeclaration import FunctionDeclaration
from instruction.If import If
from instruction.Loop import Loop
from instruction.Match import Match
from instruction.Println import Println
from instruction.Return import Return
from instruction.Statement import Statement
from instruction.While import While
from util.Types import Type


precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "EQUALS", "NEQUALS"),
    ("left", "LTHAN", "GTHAN", "LORE", "GORE"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MODULE"),
    ("left", "RAS"),
    ("right", "UMINUS", "NOT"),
    ("left", "DOT", "PARENS"),
)


def p_init(p):
    "init : instructions"
    p[0] = p[1]


def p_instructions(p):
    "instructions : instructions instruction"
    p[1].append(p[2])
    p[0] = p[1]


def p_instructions_instr(p):
    "instructions : instruction"
    p[0] = [p[1]]


def p_instruction(p):
    """instruction : declaration SEMICOLON
    | asignation SEMICOLON
    | println SEMICOLON
    | if_st
    | match
    | while
    | loop
    | for
    | break SEMICOLON
    | continue SEMICOLON
    | return SEMICOLON
    | function"""
    p[0] = p[1]


def p_simple_instr(p):
    """simple_instr : println
    | asignation
    | break
    | continue
    | return"""
    p[0] = p[1]


def p_simple_instr_2(p):
    "simple_instr : empty"
    p[0] = None


def p_statement(p):
    "statement : LCBRACKET instructions simple_instr RCBRACKET"
    if p[2] is None:
        p[2] = []
    if p[3] is not None:
        p[2].append(p[3])
    p[0] = Statement(p.lineno(1), p.lexpos(1), p[2])


def p_statement_2(p):
    "statement : LCBRACKET simple_instr RCBRACKET"
    if p[2] is None:
        p[0] = Statement(p.lineno(1), p.lexpos(1), [])
    else:
        p[0] = Statement(p.lineno(1), p.lexpos(1), [p[2]])


def p_primitive_type(p):
    """primitive_type : RINT
    | RFLOAT
    | RBOOL
    | RCHAR
    | AMPERSAND RSTR
    | RSTRING
    | RUSIZE"""
    if p[1] == "i64":
        p[0] = Type.I64
    elif p[1] == "f64":
        p[0] = Type.F64
    elif p[1] == "bool":
        p[0] = Type.Bool
    elif p[1] == "char":
        p[0] = Type.Char
    elif p[1] == "&":
        p[0] = Type.Str
    elif p[1] == "String":
        p[0] = Type.String
    else:
        p[0] = Type.Usize


def p_declaration_mut(p):
    "declaration : RLET RMUT ID COLON primitive_type EQUAL expression"
    p[0] = Declaration(p.lineno(1), p.lexpos(1), True, p[3], p[5], p[7])


def p_declaration(p):
    "declaration : RLET ID COLON primitive_type EQUAL expression"
    p[0] = Declaration(p.lineno(1), p.lexpos(1), False, p[2], p[4], p[6])


def p_asignation(p):
    "asignation : ID EQUAL expression"
    p[0] = Assignation(p.lineno(1), p.lexpos(1), p[1], p[3])


def p_println(p):
    "println : RPRINTLN NOT LPAREN expressions RPAREN"
    p[0] = Println(p.lineno(1), p.lexpos(1), p[4])


def p_ifst(p):
    "if_st : RIF expression statement else_st"
    p[0] = If(p.lineno(1), p.lexpos(1), p[2], p[3], p[4])


def p_else_st(p):
    """else_st : RELSE statement
    | RELSE if_st
    | empty"""
    if p[1] == "else":
        p[0] = p[2]
    else:
        p[0] = None


def p_match(p):
    "match : RMATCH expression LCBRACKET cases default RCBRACKET"
    p[0] = Match(p.lineno(1), p.lexpos(1), p[2], p[4], p[5])


def p_cases(p):
    "cases : cases case"
    p[1].append(p[2])
    p[0] = p[1]


def p_cases_case(p):
    "cases : case"
    p[0] = [p[1]]


def p_case(p):
    """case : expressions_match ARROW statement
    | expressions_match ARROW simple_instr COMMA"""
    p[0] = Case(p.lineno(1), p.lexpos(1), p[1], p[3])


def p_default(p):
    """default : UNDERSCORE ARROW statement
    | UNDERSCORE ARROW simple_instr COMMA
    | empty"""
    if p[1] == "_":
        p[0] = Default(p.lineno(1), p.lexpos(1), p[3])
    else:
        p[0] = None


def p_while(p):
    "while : RWHILE expression statement"
    p[0] = While(p.lineno(1), p.lexpos(1), p[2], p[3])


def p_loop(p):
    "loop : RLOOP statement"
    p[0] = Loop(p.lineno(1), p.lexpos(1), p[2])


def p_for_range(p):
    """for : RFOR ID RIN expression DOT DOT expression statement
    | RFOR ID RIN expression statement"""
    if p[5] == ".":
        p[0] = For(p.lineno(1), p.lexpos(1), p[2], p[4], p[7], p[8])
    else:
        p[0] = For(p.lineno(1), p.lexpos(1), p[2], p[4], None, p[5])


def p_break(p):
    "break : RBREAK"
    p[0] = Break(p.lineno(1), p.lexpos(1), None)


def p_break_2(p):
    "break : RBREAK expression"
    p[0] = Break(p.lineno(1), p.lexpos(1), p[2])


def p_continue(p):
    "continue : RCONTINUE"
    p[0] = Continue(p.lineno(1), p.lexpos(1))


def p_return(p):
    "return : RRETURN"
    p[0] = Return(p.lineno(1), p.lexpos(1), None)


def p_return_2(p):
    """return : RRETURN expression
    | expression"""
    if p[1] == "return":
        p[0] = Return(p.lineno(1), p.lexpos(1), p[2])
    else:
        p[0] = Return(p.lineno(1), p.lexpos(1), p[1])


def p_function(p):
    """function : RFN ID LPAREN RPAREN statement
    | RFN ID LPAREN args RPAREN statement"""
    if p[4] != ")":
        p[0] = FunctionDeclaration(
            p.lineno(1), p.lexpos(1), p[2], p[4], p[6], Type.Void
        )
    else:
        p[0] = FunctionDeclaration(p.lineno(1), p.lexpos(1), p[2], [], p[5], Type.Void)


def p_function_return(p):
    """function : RFN ID LPAREN RPAREN ARROW2 primitive_type statement
    | RFN ID LPAREN args RPAREN ARROW2 primitive_type statement"""
    if p[4] != ")":
        p[0] = FunctionDeclaration(p.lineno(1), p.lexpos(1), p[2], p[4], p[8], p[7])
    else:
        p[0] = FunctionDeclaration(p.lineno(1), p.lexpos(1), p[2], [], p[7], p[6])


def p_args_list(p):
    "args : args COMMA arg"
    p[1].append(p[3])
    p[0] = p[1]


def p_args_item(p):
    "args : arg"
    p[0] = [p[1]]


def p_arg(p):
    """arg : ID COLON primitive_type"""
    p[0] = {"name": p[1], "type": p[3], "mut": False}


# =========== Expresiones ===========


def p_expressions(p):
    "expressions :  expressions COMMA expression"
    p[1].append(p[3])
    p[0] = p[1]


def p_expressions_expression(p):
    "expressions : expression"
    p[0] = [p[1]]


def p_expressions_match(p):
    "expressions_match : expressions_match PIPE expression"
    p[1].append(p[3])
    p[0] = p[1]


def p_expressions_expression_match(p):
    "expressions_match : expression"
    p[0] = [p[1]]


def p_expr_cast(p):
    "expression : expression RAS primitive_type"
    p[0] = Cast(p.lineno(1), p.lexpos(1), p[1], p[3])


def p_expr_abs(p):
    "expression : expression DOT RABS LPAREN RPAREN"
    p[0] = Abs(p.lineno(1), p.lexpos(1), p[1])


def p_expr_sqrt(p):
    "expression : expression DOT RSQRT LPAREN RPAREN"
    p[0] = Sqrt(p.lineno(1), p.lexpos(1), p[1])


def p_expr_pow(p):
    """expression : RPOW LPAREN expression COMMA expression RPAREN
    | RPOWF LPAREN expression COMMA expression RPAREN"""
    if p[1] == "pow":
        p[0] = Pow(p.lineno(1), p.lexpos(1), p[3], p[5], Type.I64)
    else:
        p[0] = Pow(p.lineno(1), p.lexpos(1), p[3], p[5], Type.F64)


def p_expr_reference(p):
    "expression : AMPERSAND expression %prec UMINUS"
    p[0] = Reference(p.lineno(1), p.lexpos(1), p[2])


def p_expr_selection(p):
    """expression : if_st
    | loop
    | match"""
    p[0] = p[1]


def p_expr_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = Operation(p.lineno(1), p.lexpos(1), None, p[2], p[1], True)


def p_expression(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression MODULE expression"""
    p[0] = Operation(p.lineno(1), p.lexpos(1), p[1], p[3], p[2])


def p_expr_relational(p):
    """expression : expression EQUALS expression
    | expression NEQUALS expression
    | expression LTHAN expression
    | expression LORE expression
    | expression GTHAN expression
    | expression GORE expression"""
    p[0] = Operation(p.lineno(1), p.lexpos(1), p[1], p[3], p[2])


def p_expr_logic(p):
    """expression : expression AND expression
    | expression OR expression
    | NOT expression"""
    if p[2] == "||" or p[2] == "&&":
        p[0] = Logic(p.lineno(1), p.lexpos(1), p[1], p[3], p[2])
    else:
        p[0] = Logic(p.lineno(1), p.lexpos(1), None, p[2], p[1], True)


def p_expr_par(p):
    "expression : LPAREN expression RPAREN %prec PARENS"
    p[0] = p[2]


def p_expr_tostr(p):
    """expression : expression DOT RTOSTRING LPAREN RPAREN
    | expression DOT RTOOWNED LPAREN RPAREN"""
    p[0] = ToString(p.lineno(1), p.lexpos(1), p[1])


def p_literal(p):
    """expression : INT
    | FLOAT
    | STRING
    | CHAR"""
    p[0] = Literal(p.lineno(1), p.lexpos(1), p[1])


def p_true(p):
    "expression : RTRUE"
    p[0] = Literal(p.lineno(1), p.lexpos(1), True)


def p_false(p):
    "expression : RFALSE"
    p[0] = Literal(p.lineno(1), p.lexpos(1), False)


def p_access(p):
    "expression : ID"
    p[0] = SimpleAccess(p.lineno(1), p.lexpos(1), p[1])


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    if p:
        print(
            "Syntax error at token", p.type, "at line", p.lineno, "at column", p.lexpos
        )
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
