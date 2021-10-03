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

stck = []
import procedure_dir 
import ply.yacc as yacc
from lexer import tokens, lexer

proc_dir = procedure_dir.procedure_dir()

def p_program(p):
    """
    program : PROGRAM ID SEMICOLON programB
    """
    print("PROG: ", p[2])
    p[0] = p[2]

def p_programB(p):
    """
    programB : vars  programC 
        | programC
    """
    p[0] = None

def p_programC(p):
    """
    programC : function programC
             | programD
    """
    p[0] = None

def p_programD(p):
    """
    programD : main
    """
    p[0] = None

def p_vars(p):
    """
    vars : VARS L_BRACE varsB R_BRACE 
    """
    
    if proc_dir.curr_scope == "global":
        proc_dir.curr_scope = "local"
        proc_dir.add_procedure("program","void")
    p[0] = None

def p_varsB(p):
    """
    varsB : type COLON varsC SEMICOLON
          | type COLON varsC SEMICOLON varsB
    """
    lst = p[3].split(',')
    for var_name in lst:
        proc_dir.add_variable(var_name=var_name, var_datatype=p[1])
    p[0] = None

def p_varsC(p):
    """
    varsC : var
          | var COMMA varsC
    """
    #print("LENGTH:",len(p))
    if(len(p) > 2):
        p[0] = str(p[1])+","+str(p[3])
    else:
        p[0] = p[1]

def p_function(p):
    """
    function : FUNCTION func_type ID L_PAR functionB R_PAR  block
    """
    proc_dir.add_procedure(proc_name=p[3], proc_datatype=p[2])
    p[0] = None

def p_functionB(p):
    """
    functionB : params 
          | empty
    """
    p[0] = None

def p_main(p):
    """
    main : MAIN L_PAR R_PAR block
    """
    proc_dir.add_procedure(proc_name = "main",proc_datatype="void")

def p_type(p):
    """
    type : INT 
          | FLOAT 
          | BOOL 
          | CHAR 
          | STRING
    """
    p[0] = p[1]

def p_var(p):
    """
    var : ID L_BRACKET CTE_INT R_BRACKET
        | ID L_BRACKET ID R_BRACKET
        | ID
    """
    p[0] = p[1]

def p_vector(p):
    """
    vector : ID L_BRACKET R_BRACKET
    """

def p_func_type(p):
    """
    func_type : VOID 
              | type
    """
    p[0] = p[1]

def p_block(p):
    """
    block : L_BRACE block2 block3 R_BRACE 
    
    block2 : vars
            | empty

    block3 : empty 
           | statement block3
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
           | func_call
    """

def p_assign(p):
    """
    assign : var oper_assign expression SEMICOLON
    """

def p_predef_func(p):
    """
    predef_func : LENGTH L_PAR vector R_PAR
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
    condicional : IF L_PAR expression R_PAR THEN block cond2
    
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

def p_func_call(p):
    """
    func_call : ID L_PAR func_callB R_PAR 
    """


def p_func_callB(p):
    """
    func_callB : exp
          | COMMA exp func_callB
          | empty
    """

def p_expression(p):
    """
    expression : not logic expression2
    
    expression2 : OR expression 
          | AND expression
          | empty
    """

def p_oper_assign(p):
    """
    oper_assign : EQUAL 
        | MULT_EQ 
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
    logic : exp logic2
    
    logic2 : LESS exp
         | GREATER exp
         | LESS_EQ exp
         | GREATER_EQ exp
         | EQUIVALENT exp
         | DIFFERENT exp
         | empty
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
    factor : exponent factorB 
    """

def p_factorB(p):
    """
    factorB : EXP factor
            | empty
    """

def p_exponent(p):
    """
    exponent : L_PAR expression R_PAR 
        | exponent2 
    
    exponent2 : PLUS var_cte 
        | MINUS var_cte 
        | var_cte 

    """

def p_var_cte(p):
    """
    var_cte : var 
         | func_call
         | predef_func
         | CTE_INT 
         | CTE_FLOAT 
         | CTE_CHAR 
         | CTE_STRING 
         | CTE_BOOL 
    """

def p_error(p):
    print("Syntax error found at line {0} around '{1}'".format(lexer.lineno, p))


def p_empty(p):
    """
    empty :
    """

# Build the parser
parser = yacc.yacc()


if __name__ == "__main__":
    try:
        file = open("Test/test1.alebrije", "r")
        code = ""
        for line in file:
            code += line
        parser.parse(code)
        proc_dir.print_procedure_directory()
        proc_dir.print_var_tables()
        print("Done")
    except EOFError:
        print("Error")