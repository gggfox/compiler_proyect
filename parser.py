'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   alebrije_parser.py      #
#   Created_at 2021-09-25   #
#   Updated_at 2021-10-09   #
#############################
''' 

import procedure_dir 
import ply.yacc as yacc
from lexer import tokens, lexer

proc_dir = procedure_dir.procedure_dir()

def p_program(p):
    """
    program : PROGRAM np_set_curr_proc ID np_GOTO SEMICOLON programB
    """

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
             | main
    """
    p[0] = None

def p_vars(p):
    """
    vars : VARS L_BRACE varsB R_BRACE 
    """
    p[0] = None

def p_varsB(p):
    """
    varsB : type np_set_curr_datatype COLON varsC SEMICOLON
          | type np_set_curr_datatype COLON varsC SEMICOLON varsB
    """
    p[0] = p[1]

def p_varsC(p):
    """
    varsC : var np_add_var
          | var np_add_var COMMA varsC
    """


def p_function(p):
    """
    function : FUNCTION func_type ID  np_set_curr_proc L_PAR functionB R_PAR  block
    """
    p[0] = None

def p_functionB(p):
    """
    functionB : params 
          | empty
    """
    p[0] = None

def p_main(p):
    """
    main : MAIN np_set_curr_proc np_GOTO_END L_PAR R_PAR block
    """

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
    assign : var np_add_operand oper_assign np_add_operator expression SEMICOLON
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
    condicional : IF L_PAR expression np_GOTOF R_PAR THEN block cond2 np_GOTO_END
    
    cond2 : np_GOTO ELSE block 
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
    p[0] = p[1]

def p_not(p):
    """
    not : NOT np_add_operator
         | empty
    """

def p_logic(p):
    """
    logic : exp logic2 
    
    logic2 : LESS exp
         | GREATER np_add_operator exp
         | LESS_EQ np_add_operator exp
         | GREATER_EQ np_add_operator exp
         | EQUIVALENT np_add_operator exp
         | DIFFERENT np_add_operator exp
         | empty
    """

def p_exp(p):
    """
    exp : term exp2 
    
    exp2 : PLUS np_add_operator exp 
         | MINUS np_add_operator exp
         | empty
    """

def p_term(p):
    """
    term : factor term2
    
    term2 : MULT np_add_operator term 
          | DIV np_add_operator term
          | REMAINDER np_add_operator term 
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
    exponent : L_PAR np_add_operator expression R_PAR np_rpar
        | exponent2 
    
    exponent2 : PLUS var_cte 
        | MINUS var_cte 
        | var_cte 

    """

def p_var_cte(p):
    """
    var_cte : var np_add_operand
         | func_call
         | predef_func
         | CTE_INT np_add_operand
         | CTE_FLOAT np_add_operand
         | CTE_CHAR np_add_operand
         | CTE_STRING np_add_operand
         | CTE_BOOL np_add_operand
    """

def p_error(p):
    print("Syntax error found at line {0} around '{1}'".format(lexer.lineno, p))


def p_empty(p):
    """
    empty :
    """

#######################
# NEURALOGIC POINTS
#######################

quadruples = []
operand_stack = []
operator_stack = []
datatype_stack = []
jump_stack = []

def p_np_set_curr_proc(p):
    ' np_set_curr_proc : '
    print(p[-1])
    if(p[-1] in ["main","program"]):
        proc_dir.set_curr_proc(p[-1])
    # set curr to function name
    else:
        proc_dir.set_curr_proc(p[-1], p[-2])

def p_np_add_operator(p):
    'np_add_operator : '
    operator_stack.append(p[-1])

def p_np_add_operand(p):
    'np_add_operand : '
    #var_type = proc_dir.get_var_type(curr_scope, p[-1])
    operand_stack.append((p[-1], proc_dir.curr_proc))
    #var_type = proc_dir.get_var_type(curr_scope, p[-1])
    #print(var_type)

def p_np_set_curr_datatype(p):
    'np_set_curr_datatype : '
    proc_dir.curr_datatype = p[-1]
    print(p[-1])
    
def p_np_add_datatype(p):
    'np_add_datatype : '
    # If the datatype is a comma this means its the same datatype as the previous optioin
    if p[-1] == ',':
        datatype_stack.append(datatype_stack[len(datatype_stack) - 1])
    else:
        datatype_stack.append(p[-1])

def p_np_add_var(p):
    'np_add_var : '
    print(p[-1])
    proc_dir.add_variable(p[-1])

def p_np_set_curr_scope(p):
    'np_set_curr_scope : '
    proc_dir.curr_scope = p[-1]

def p_np_rpar(p):
    'np_rpar : '
    oper = operator_stack.pop()
    while oper != '(':
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        print("({0},{1},{2},{3})".format(oper, left_operand, right_operand, "temp"))
        oper = operator_stack.pop()

## GOTO's
def p_np_GOTO(p):
    'np_GOTO : '
    print("GOTO","__")
    jump_stack.append(proc_dir.get_curr_quadruple())

def p_np_GOTOF(p):
    'np_GOTOF : '
    print("GOTOF")

def p_np_GOTOV(p):
    'np_GOTOV : '
    print('GOTOV')

def p_np_GOTO_END(p):
    'np_GOTO_END : '
    print(jump_stack.pop())

# Build the parser
parser = yacc.yacc()


def priority(op):
    if op in ["=", "+=", "-=", "*=", "/="]:
        return 1
    elif op in ["+","-"]:
        return 2
    elif op in ["*","/"]:
        return 3
    elif op == "**":
        return 4
    elif op == "(":
        return 5




if __name__ == "__main__":
    try:
        file = open("Test/test_pemdas.alebrije", "r")
        code = ""
        for line in file:
            code += line
        parser.parse(code)
        proc_dir.print_procedure_directory()
        proc_dir.print_var_tables()
        print(operator_stack)
        print(operand_stack)
        print(datatype_stack)


            

        print("Done")
    except EOFError:
        print("Error")