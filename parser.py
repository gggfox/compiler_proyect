'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   alebrije_parser.py      #
#   Created_at 2021-09-25   #
#   Updated_at 2021-09-25   #
#############################
''' 

import ply.yacc as yacc
from lexer import tokens, lexer

def p_program(p):
    """
    program : PROGRAM ID SEMICOLON prog2
    
    prog2 : vars  prog3 
          | prog3 
    
    prog3 : function prog3 
          | main empty
    """
    p[0] = None

def p_vars(p):
    """
    vars : VARS L_BRACE vars2 R_BRACE 
    
    vars2 : vars3
          | vars3 vars2
    
    vars3 : type COLON vars4 SEMICOLON
    
    vars4 : var 
          | var COMMA vars4
    """

def p_function(p):
    """
    function : FUNCTION func_type ID L_PAR func2 R_PAR vars block
    
    func2 : params 
          | empty
    """
    p[0] = None

def p_main(p):
    """
    main : MAIN L_PAR R_PAR block
    """

def p_type(p):
    """
    type : INT 
          | FLOAT 
          | BOOL 
          | CHAR 
          | STRING
    """

def p_var(p):
    """
    var : ID L_BRACKET CTE_INT R_BRACKET
         | ID
    """

def p_vector(p):
    """
    vector : ID L_BRACKET R_BRACKET
    """

def p_func_type(p):
    """
    func_type : VOID 
              | type
    """

def p_block(p):
    """
    block : L_BRACE statement R_BRACE 
    """

def p_params(p):
    """
    params : param2
           | param2 COMMA params
    
    param2 : type COLON var
    """

def p_statement(p):
    """
    statement : assign 
           | condicional 
           | read 
           | write 
           | loop_cond 
           | loop_range 
           | return 
           | func
    """

def p_assign(p):
    """
    assign : var assign2 assign3
    
    assign2 : EQUAL 
         | oper_assign

    assign3 : expression
            | func
            | LENGTH L_PAR vector R_PAR
            | MIN L_PAR vector R_PAR
            | MAX L_PAR vector R_PAR
            | MEAN L_PAR vector R_PAR
            | MEDIAN L_PAR vector R_PAR
            | MODE L_PAR vector R_PAR
            | PLOT_XY L_PAR vector COMMA vector R_PAR
            | REGRESSION L_PAR vector COMMA vector R_PAR
            | VARIANCE L_PAR vector R_PAR
            | DOT L_PAR vector COMMA vector R_PAR
            | SUM L_PAR vector R_PAR
            | ABS L_PAR CTE_INT R_PAR
            | ROOF L_PAR CTE_FLOAT R_PAR
            | FLOOR L_PAR CTE_FLOAT R_PAR

    """

def p_condicional(p):
    """
    condicional : IF L_PAR expression R_PAR THEN block cond2 SEMICOLON
    
    cond2 : ELSE block 
          | empty 
    """

def p_read(p):
    """
    read : READ L_PAR read2 R_PAR SEMICOLON
    
    read2 : var 
          | var COMMA read2
    """

def p_write(p):
    """
    write : WRITE L_PAR write2 R_PAR SEMICOLON
    
    write2 : expression write3
           | CTE_STRING write3
    
    write3 : COMMA write2 
           | empty
    """

def p_loop_cond(p):
    """
    loop_cond : WHILE L_PAR expression R_PAR DO block
    """

def p_loop_range(p):
    """
    loop_range : FOR var EQUAL exp TO exp DO block
    """

def p_return(p):
    """
    return : RETURN L_PAR exp R_PAR SEMICOLON
    """

def p_func(p):
    """
    func : ID L_PAR expression fun2 R_PAR SEMICOLON
    
    fun2 : COMMA expression fun2 
         | empty
    """

def p_expression(p):
    """
    expression : not logic expr2
    
    expr2 : expr3 expression 
         | empty
    
    expr3 : OR 
          | AND
    """

def p_oper_assign(p):
    """
    oper_assign : MULT_EQ 
        | DIV_EQ 
        | PLUS_EQ 
        | MINUS_EQ
    """

def p_not(p):
    """
    not : NOT 
         | empty
    """

def p_logic(p):
    """
    logic : exp log2
    
    log2 : log3 exp 
         | empty
    
    log3 : LESS 
         | GREATER 
         | LESS_EQ 
         | GREATER_EQ 
         | EQUIVALENT 
         | DIFFERENT
    """

def p_exp(p):
    """
    exp : term exp2
    
    exp2 : PLUS exp 
         | MINUS exp
         | empty
    """

def p_term(p):
    """
    term : factor term2
    
    term2 : MULT term 
          | DIV term
          | REMAINDER term 
          | empty
    """

def p_factor(p):
    """
    factor : exponent fact2 
    
    fact2 : EXP factor 
          | empty 
    """

def p_exponent(p):
    """
    exponent : L_PAR expression R_PAR 
        | ex2 var_cte
    
    ex2 : PLUS 
        | MINUS 
        | empty
    """

def p_var_cte(p):
    """
    var_cte : ID 
         | CTE_INT 
         | CTE_FLOAT 
         | CTE_CHAR 
         | CTE_STRING 
         | CTE_BOOL
    """

def p_error(p):
    print("Syntax error found at line {0} in token {1}".format(lexer.lineno, p.type))


def p_empty(p):
    """
    empty :
    """

# Build the parser
parser = yacc.yacc()


if __name__ == "__main__":
    try:
        file = open("test.alebrije", "r")
        for s in file:
            parser.parse(s)
        print("Done")
    except EOFError:
        print("Error")