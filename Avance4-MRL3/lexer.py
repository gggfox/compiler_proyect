'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   alebrije_lexer.py       #
#   Created_at 2021-09-25   #
#   Updated_at 2021-09-25   #
#############################
''' 

import ply.lex as lex

reserved = {
    'program' : 'PROGRAM',
    'main' : 'MAIN',
    'vars' : 'VARS',
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'char': 'CHAR',
    'string' : 'STRING',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'read' : 'READ',
    'write' : 'WRITE',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'to' : 'TO',
    'void' : 'VOID',
    'median' : 'MEDIAN',
    'mode' : 'MODE',
    'mean' : 'MEAN',
    'variance' : 'VARIANCE',
    'regression' : 'REGRESSION',
    'plotXY' : 'PLOT_XY',
    'max' : 'MAX',
    'min' : 'MIN',
    'length' : 'LENGTH',
    'dot' : 'DOT',
    'abs' : 'ABS',
    'sum' : 'SUM',
    'roof' : 'ROOF',
    'floor' : 'FLOOR'
}


tokens = list(reserved.values()) + [
    "AND",
    "OR",
    "NOT",
    "LESS",
    "GREATER",
    "LESS_EQ",
    "GREATER_EQ",
    "EQUIVALENT",
    "DIFFERENT",
    "EQUAL",
    "MULT",
    "DIV",
    "PLUS",
    "MINUS",
    "REMAINDER",
    "EXP",
    "MULT_EQ",
    "DIV_EQ",
    "PLUS_EQ",
    "MINUS_EQ",
    "L_BRACE",
    "R_BRACE",
    "L_BRACKET",
    "R_BRACKET",
    "L_PAR",
    "R_PAR",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "ID",
    "CTE_INT",
    "CTE_FLOAT",
    "CTE_BOOL",
    "CTE_CHAR",
    "CTE_STRING"
] 

# Simple tokens
t_LESS = r'\<'
t_GREATER = r'\>'
t_LESS_EQ = r'\<\='
t_GREATER_EQ = r'\>\=' 
t_EQUAL = r'\='
t_MULT = r'\*'
t_DIV = r'\/'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_REMAINDER = r'\%'
t_EXP = r'\*\*'
t_MULT_EQ = r'\*\='
t_DIV_EQ = r'\/\='
t_PLUS_EQ = r'\+\='
t_MINUS_EQ = r'\-\='
t_L_BRACE = r'\{'
t_R_BRACE = r'\}'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_L_PAR = r'\('
t_R_PAR = r'\)'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# complex tokens
def t_EQUIVALENT(t):
    r'((\=\=)|(is\b))'
    t.value = 'EQUIVALENT'
    return t

def t_DIFFERENT(t):
    r'((\!\=)|(isnt\b))'
    t.value = 'DIFFERENT'
    return t

def t_AND(t):
    r'((\&\&)|(and\b))'
    t.value = 'AND'
    return t

def t_OR(t):
    r'((\|\|)|(or\b))'
    t.value = 'OR'
    return t

def t_NOT(t):
    r'((\!)|(not\b))'
    t.value = 'NOT'
    return t

def t_CTE_BOOL(t):
    r'(True|true|False|false)'
    t.type = 'CTE_BOOL'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    reserved_type  = reserved.get(t.value, False)
    if reserved_type:
        t.type = reserved_type
        return t
    else:
        t.type = 'ID'
        return t

def t_CTE_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_CTE_CHAR(t):
    r'(\'((?!\').)\')|(\"((?!\").)\")'
    t.type = 'CTE_CHAR'
    return t

'''
the regex does a negative look ahead(?!) for ' or " depending
on the case, so \'\'\' is invalid and so is """
'''
def t_CTE_STRING(t):
    r'(\'((?!\').)*\')|(\"((?!\").)*\")'
    t.type = 'CTE_STRING'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# build the lexer
lexer = lex.lex()

# Tokenize
if __name__ == "__main__":
    code = ""
    file = open("Test/test_func.alebrije", "r")
    for line in file:
        code += line

    # Give the lexer some input
    lexer.input(code)

    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

