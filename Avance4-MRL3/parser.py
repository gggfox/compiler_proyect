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
import sys
import procedure_dir 
import ply.yacc as yacc
from lexer import tokens, lexer

proc_dir = procedure_dir.procedure_dir()

def p_program(p):
    """
    program : PROGRAM np_set_curr_proc ID np_GOTO SEMICOLON programB np_prog_end
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
    function : FUNCTION func_type ID np_set_curr_proc L_PAR params R_PAR  np_set_quad_start vblock np_ENDFunc 
    """
    p[0] = None

def p_main(p):
    """
    main : MAIN np_set_curr_proc np_GOTO_END L_PAR R_PAR vblock 
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
    block : L_BRACE blockB R_BRACE 

    blockB : statement blockB
           | empty
    """
def p_vblock(p):
    """
    vblock : L_BRACE vars blockB R_BRACE 
    
    vblockB : statement vblockB
            | empty
    """

def p_params(p):
    """
    params : type COLON ID np_add_param
           | type COLON ID np_add_param COMMA params
           | empty
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
           | void_func
    """
def p_void_func(p):
    '''
    void_func : func_call SEMICOLON
    '''
def p_assign(p):
    """
    assign : var np_add_operand oper_assign np_add_operator expression np_end SEMICOLON
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
    condicional : IF L_PAR expression np_end np_GOTOF R_PAR block cond2 np_GOTO_END
    
    cond2 : np_GOTO_ELSE ELSE block 
          | empty 
    """

def p_read(p):
    """
    read : READ L_PAR read2 R_PAR SEMICOLON
    
    read2 : var np_read
          | var np_read COMMA read2
    """

def p_write(p):
    """
    write : WRITE L_PAR writeB R_PAR SEMICOLON
    """

def p_writeB(p):
        """
    writeB : expression np_end np_write writeC
           | CTE_STRING np_add_cte_string np_write writeC
    """

def p_writeC(p):
    """
    writeC : COMMA writeB
           | empty
    """

def p_loop_cond(p):
    """
    loop_cond : WHILE L_PAR np_GOTO_BEGIN expression R_PAR  np_end np_GOTOF block np_GOTO_WHILE
    """

def p_loop_range(p):
    """
    loop_range : FOR var np_add_operand EQUAL np_add_operator exp np_set_VC TO exp np_end np_comp_VC_VF block np_GOTO_FOR
    """

def p_return(p):
    """
    return : RETURN L_PAR exp np_end R_PAR SEMICOLON
    """

def p_func_call(p):
    """
    func_call : ID np_ERA L_PAR func_call_arguments R_PAR np_GOSUB
    """


def p_func_call_arguments(p):
    """
    func_call_arguments : exp np_end np_param
                        | exp np_end np_param COMMA func_call_arguments
                        | empty
    """

def p_expression(p):
    """
    expression : not logic expressionB 
    """

def p_expressionB(p):
    """    
    expressionB : OR np_add_operator expression 
          | AND np_add_operator expression
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
        | exponentB 
    """

def p_exponentB(p):
    """ 
    exponentB : MINUS var_cte 
        | var_cte 

    """
    p[0] = p[-1]

def p_var_cte(p):
    """
    var_cte : var np_add_operand
         | predef_func
         | func_call
         | CTE_INT np_add_operand
         | CTE_FLOAT np_add_operand
         | CTE_CHAR np_add_operand
         | CTE_STRING np_add_operand
         | CTE_BOOL np_add_operand
    """
    p[0] = p[1]

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
'''
returns the item on top of the stack, 
aka the last operator to be added into the stack
'''
def top(stack:list):
    if len(stack) > 0:
        return stack[len(stack) - 1]
    return 

def p_np_set_curr_proc(p):
    'np_set_curr_proc : '
    
    if(p[-1] in ["main","program"]):
        proc_dir.set_curr_proc(p[-1],"void")
    # set curr to function name
    elif(proc_dir.curr_proc != p[-1]):
        print(p[-1],p[-2])
        proc_dir.set_curr_proc(p[-1], p[-2])

'''
adds operator to operator stack, and creates quadruple in case the current operator
has less or equal priority to the last operator added to the operator stack
'''
def p_np_add_operator(p):
    'np_add_operator : '
    #print(p[-1],priority(p[-1]),top(operator_stack),priority(top(operator_stack)))
    if len(operator_stack) >= 1 and priority(p[-1]) <= priority(top(operator_stack)) and top(operator_stack) != '(':
        
        oper = operator_stack.pop()
        
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        temp = "temp"+str(proc_dir.get_curr_temp())
        quadruples.append("({0},{1},{2},{3})".format(oper, left_operand, right_operand, temp))
        operand_stack.append(temp)
    
    operator_stack.append(p[-1])

'''
adds operand to the operand stack
'''
def p_np_add_operand(p):
    'np_add_operand : '
    #var_type = proc_dir.get_var_type(curr_scope, p[-1])
    operand_stack.append(p[-1])
    #var_type = proc_dir.get_var_type(curr_scope, p[-1])
    #print(var_type)

def p_np_set_curr_datatype(p):
    'np_set_curr_datatype : '
    proc_dir.curr_datatype = p[-1]
    #print(p[-1])
    
def p_np_add_datatype(p):
    'np_add_datatype : '
    # If the datatype is a comma this means its the same datatype as the previous optioin
    if p[-1] == ',':
        datatype_stack.append(datatype_stack[len(datatype_stack) - 1])
    else:
        datatype_stack.append(p[-1])

'''
adds variable to the varibale table of the current function
'''
def p_np_add_var(p):
    'np_add_var : '
    #print(p[-1])
    proc_dir.add_variable(p[-1])

'''
updates the current function.
example: program, func_name, main
'''
def p_np_set_curr_scope(p):
    'np_set_curr_scope : '
    proc_dir.curr_scope = p[-1]

'''
creates quadruples unitl it finds a left parenthesis on the operator stack
'''
def p_np_rpar(p):
    'np_rpar : '
    #print(operator_stack)
    oper = operator_stack.pop()
    while oper != '(':
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        temp = "temp"+str(proc_dir.get_curr_temp())
        quadruples.append("({0},{1},{2},{3})".format(oper, left_operand, right_operand, temp))
        operand_stack.append(temp)
        oper = operator_stack.pop()

'''
creates quadruples until the operator stack is empty
'''
def p_np_end(p):
    'np_end : '
    #print(operator_stack)
    while len(operator_stack) > 0:
        oper = operator_stack.pop()
        if oper == 'stop':
            break

        if oper == '=':
            operand1 = operand_stack.pop()
            operand2 = operand_stack.pop()
            quadruples.append('({0},{1},{2},{3})'.format(oper, operand1, '', operand2))
        else:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            temp = 'temp'+str(proc_dir.get_curr_temp())
            quadruples.append('({0},{1},{2},{3})'.format(oper, left_operand, right_operand, temp))
            operand_stack.append(temp)

def p_np_read(p):
    'np_read : '
    quadruples.append(("READ",p[-1]))

def p_np_write(p):
    'np_write : '
    operand = operand_stack.pop()
    quadruples.append(("WRITE",operand))

def p_np_add_cte_string(p):
    'np_add_cte_string : '
    operand_stack.append(p[-1])

def p_np_set_VC(p):
    'np_set_VC : '
    while len(operator_stack) > 0:
        oper = operator_stack.pop()
        #print(oper)
        if oper == "=":    
            operand1 = operand_stack.pop()
            operand2 = operand_stack.pop()
            quadruples.append("({0},{1},{2},{3})".format(oper, operand1, "", operand2))
            operand_stack.append(operand2)
        else:
            right_operand = operand_stack.pop()
            left_operand = operand_stack.pop()
            temp = "temp"+str(proc_dir.get_curr_temp())
            quadruples.append("({0},{1},{2},{3})".format(oper, left_operand, right_operand, temp))
            operand_stack.append(temp)



def p_np_comp_VC_VF(p):
    'np_comp_VC_VF : '
    temp = "temp"+str(proc_dir.get_curr_temp())
    vf = operand_stack.pop()
    vc = operand_stack.pop()
    quadruples.append("({0},{1},{2},{3})".format("<", vc, vf, temp))
    operand_stack.append(vc)
    jump_stack.append(len(quadruples)-1)
    quadruples.append(("GOTOF",str(temp),None,None))
    jump_stack.append(len(quadruples)-1)

## GOTO's
def p_np_GOTO(p):
    'np_GOTO : '
    quadruples.append(("GOTO",None,None,None))
    jump_stack.append(len(quadruples)-1)

'''
creates gotoF quadruple, it jumps to the position in case
'''
def p_np_GOTOF(p):
    'np_GOTOF : '
    cond = operand_stack.pop()
    quadruples.append(("GOTOF",str(cond),None,None))
    jump_stack.append(len(quadruples)-1)

def p_np_GOTOV(p):
    'np_GOTOV : '
    quadruples.append(('GOTOV',None,None,None))

def p_np_GOTO_ELSE(p):
    'np_GOTO_ELSE : '
    goto_index = jump_stack.pop()
    (a,b,c,d) = quadruples[goto_index]
    quadruples[goto_index] = (a,b,len(quadruples)+1,d)
    quadruples.append(("GOTO",None,None,None))
    jump_stack.append(len(quadruples)-1)

def p_np_GOTO_END(p):
    'np_GOTO_END : '
    print(jump_stack)
    print(proc_dir.curr_proc)
    goto_index = jump_stack.pop()
    (a,b,c,d) = quadruples[goto_index]
    quadruples[goto_index] = (a,b,len(quadruples),d)
    #quadruples.append("end goto "+str())

def p_np_GOTO_WHILE(p):
    'np_GOTO_WHILE : '
    goto_index = jump_stack.pop()
    pre_expression = jump_stack.pop()
    quadruples.append(("GOTO",None,pre_expression,None))
    (a,b,c,d) = quadruples[goto_index]
    quadruples[goto_index] = (a,b,len(quadruples),d)
    
def p_np_GOTO_FOR(p):
    'np_GOTO_FOR : '
    temp = "temp"+str(proc_dir.get_curr_temp())
    var = operand_stack.pop()
    quadruples.append('(+,1,{0},{1})'.format(var,temp))
    quadruples.append('(=,{0},None,{1})'.format(temp,var))

    goto_index = jump_stack.pop()
    comp_vc_vf = jump_stack.pop()
    quadruples.append('(GOTO,{0},None,None)'.format(comp_vc_vf))
    (a,b,c,d) = quadruples[goto_index]
    quadruples[goto_index] = (a,b,len(quadruples),d)

def p_np_GOTO_BEGIN(p):
    'np_GOTO_BEGIN : '
    jump_stack.append(len(quadruples))

## FUNCTION CONTROL

def p_np_add_param(p):
    'np_add_param : '
    proc_dir.add_param(param_name=p[-1],datatype=p[-3])
    #(PARAM,Argument, Argument#k,_)
    

def p_np_set_quad_start(p):
    'np_set_quad_start : '
    proc_dir.set_quad_start(len(quadruples))
    

def p_np_GOSUB(p):
    'np_GOSUB : '
    # jump that changes instruction pointer to a specific line of code
    argk = proc_dir.get_curr_arg_k() - 1
    if argk != proc_dir.get_param_num(func_name=p[-5]):
        print("ERROR the number of arguments does not match the number of params")
    quadruples.append('(GOSUB,{proc_name},{init_address},_)'.format(proc_name=p[-5],init_address=0))

def p_np_ERA(p):
    'np_ERA : '
    # indicates the size of the local memory to be created in run time
    # verify that the function exists
    if proc_dir.exist_proc(p[-1]):
        # Generate ERA
        quadruples.append('(ERA,{0},_,_)'.format(p[-1]))
        proc_dir.reset_curr_arg_k()
    else:
        print('ERROR Function "{0}" is not defined'.format(p[-1]))
        p_error(p)

def p_np_param(p):
    'np_param : '
    arg = operand_stack.pop()
    argk = proc_dir.get_curr_arg_k()
    quadruples.append('(PARAM,{arg},{argk},_)'.format(arg=arg,argk=argk))

"""
borra memoria temporal que se uso para jecutar la funcion
"""
def p_np_ENDFunc(p):
    'np_ENDFunc : '
    # erase local memory 
    quadruples.append('(ENDFUNC,_,_,_)')
    proc_dir.set_quad_end(len(quadruples) - 1)
    proc_dir.reset_curr_temp()

def p_np_break_point(p):
    'np_break_point : '
    operator_stack.append('stop')

def p_np_prog_end(p):
    'np_prog_end : '
    quadruples.append('(PROG_END,None,None,None)')
# Build the parser
parser = yacc.yacc()

'''
returns the priority of a given operator
'''
def priority(op:str) -> int:
    val = 0
    if op in ['and', 'or', '&&', '||', 'not', '!']:
        val = 1
    if op in ['>','<','>=','<=','==','!=','is','isnt', 'DIFFERENT']:
        val = 2
    elif op in ['=', '+=', '-=', '*=', '/=']:
        val = 3
    elif op in ['+','-']:
        val = 4
    elif op in ['*','/','%']:
        val = 5
    elif op == '**':
        val = 6
    elif op == '(':
        val = 7
    else:
        val = 0
    lvl = operator_stack.count('(') + 1
    return val * lvl

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            test = 'Test/{0}'.format(sys.argv[1])
        else:
            test = 'Test/test_func_recursion.alebrije'
        file = open(test, "r")
        code = ""
        for line in file:
            code += line
        parser.parse(code)
        proc_dir.print_procedure_directory()
        proc_dir.print_var_tables()
        for index, value in enumerate(quadruples):
            print(index, value)

        print(jump_stack)
        print(operator_stack)
        print(operand_stack)
        print(datatype_stack)

            

        print("Done")
    except EOFError:
        print("Error")