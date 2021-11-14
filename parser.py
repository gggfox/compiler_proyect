'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   alebrije_parser.py      #
#   Created_at 2021-09-25   #
#                           #
#############################
'''
import sys
import json
import procedure_dir
import ply.yacc as yacc
from lexer import tokens, lexer
from stack import Stack
from vm import VM

proc_dir = procedure_dir.procedure_dir()
stack = Stack()

def p_program(p):
    '''
    program : PROGRAM np_set_curr_proc ID np_GOTO SEMICOLON programB np_prog_end
    '''

def p_programB(p):
    '''
    programB : vars  programC 
        | programC
    '''

def p_programC(p):
    '''
    programC : function programC
             | main
    '''

def p_vars(p):
    '''
    vars : VARS L_BRACE varsB R_BRACE 
    '''

def p_varsB(p):
    '''
    varsB : type np_set_curr_datatype COLON varsC SEMICOLON
          | type np_set_curr_datatype COLON varsC SEMICOLON varsB
    '''

def p_varsC(p):
    '''
    varsC : varsD 
          | varsD COMMA varsC
    '''

def p_varsD(p):
    '''
    varsD : ID np_add_var
          | ID L_BRACKET  CTE_INT R_BRACKET np_add_arr 
    '''

def p_function(p):
    '''
    function : FUNCTION func_type ID np_set_curr_proc L_PAR params R_PAR np_set_quad_start vblock np_ENDFunc 
    '''

def p_main(p):
    '''
    main : MAIN np_set_curr_proc np_GOTO_END L_PAR R_PAR vblock 
    '''

def p_type(p):
    '''
    type : INT np_add_datatype
          | FLOAT np_add_datatype
          | BOOL np_add_datatype
          | CHAR np_add_datatype
          | STRING np_add_datatype
    '''
    p[0] = p[1]

def p_var(p):
    '''
    var : ID L_BRACKET np_arr_start exp np_end np_arr_end R_BRACKET
        | ID np_push_operand
    '''
    p[0] = p[1]

def p_vector(p):
    '''
    vector : ID L_BRACKET R_BRACKET
    '''

def p_func_type(p):
    '''
    func_type : VOID np_add_datatype 
              | type
    '''
    p[0] = p[1]

def p_block(p):
    '''
    block : L_BRACE blockB R_BRACE 

    blockB : statement blockB
           | empty
    '''

def p_vblock(p):
    '''
    vblock : L_BRACE vars vblockB R_BRACE 
           | block

    vblockB : statement vblockB
            | empty
    '''

def p_params(p):
    '''
    params : type COLON ID np_add_param
           | type COLON ID np_add_param COMMA params
           | empty
    '''

def p_statement(p):
    '''
    statement : assign 
           | condicional 
           | read 
           | write 
           | loop_cond 
           | loop_range 
           | return 
           | void_func
    '''

def p_void_func(p):
    '''
    void_func : func_call SEMICOLON
    '''

def p_assign(p):
    '''
    assign : var oper_assign np_push_operator expression np_end SEMICOLON
    '''

def p_predef_func(p):
    '''
    predef_func : MIN L_PAR vector R_PAR
            | MAX L_PAR vector R_PAR
            | MEAN L_PAR vector R_PAR
            | MEDIAN L_PAR vector R_PAR
            | MODE L_PAR vector R_PAR
            | PLOT_XY L_PAR vector COMMA vector R_PAR
            | REGRESSION L_PAR vector COMMA vector R_PAR
            | VARIANCE L_PAR vector R_PAR
            | SUM L_PAR vector R_PAR
    '''

def p_condicional(p):
    '''
    condicional : IF L_PAR expression np_end np_GOTOF R_PAR block cond2 np_GOTO_END

    cond2 : np_GOTO_ELSE ELSE block 
          | empty 
    '''

def p_read(p):
    '''
    read : READ L_PAR read2 R_PAR SEMICOLON

    read2 : var np_read
          | var np_read COMMA read2
    '''

def p_write(p):
    '''
    write : WRITE L_PAR writeB R_PAR SEMICOLON
    '''

def p_writeB(p):
    '''
    writeB : expression np_end np_write writeC
           | CTE_STRING np_push_cte_str np_write writeC
    '''

def p_writeC(p):
    '''
    writeC : COMMA writeB
           | empty
    '''

def p_loop_cond(p):
    '''
    loop_cond : WHILE L_PAR np_CHECKPOINT expression R_PAR  np_end np_GOTOF block np_GOTO_WHILE
    '''

def p_loop_range(p):
    '''
    loop_range : FOR var EQUAL np_push_operator exp np_set_VC TO exp np_end np_comp_VC_VF block np_GOTO_FOR
    '''

def p_return(p):
    '''
    return : RETURN L_PAR np_stop exp np_end np_set_return R_PAR SEMICOLON
    '''

def p_func_call(p):
    '''
    func_call : ID np_ERA L_PAR func_call_arguments R_PAR np_GOSUB
    '''

def p_func_call_arguments(p):
    '''
    func_call_arguments : np_stop exp np_end np_param
                        | np_stop exp np_end np_param COMMA func_call_arguments
                        | empty
    '''

def p_expression(p):
    '''
    expression : logic expressionB 
    '''

def p_expressionB(p):
    '''    
    expressionB : OR np_push_operator expression 
          | AND np_push_operator expression
          | empty
    '''

def p_oper_assign(p):
    '''
    oper_assign : EQUAL 
        | MULT_EQ 
        | DIV_EQ 
        | PLUS_EQ 
        | MINUS_EQ 
    '''
    p[0] = p[1]

def p_logic(p):
    '''
    logic : exp logic2 

    logic2 : LESS np_push_operator exp
         | GREATER np_push_operator exp
         | LESS_EQ np_push_operator exp
         | GREATER_EQ np_push_operator exp
         | EQUIVALENT np_push_operator exp
         | DIFFERENT np_push_operator exp
         | empty
    '''

def p_exp(p):
    '''
    exp : term exp2 

    exp2 : PLUS np_push_operator exp 
         | MINUS np_push_operator exp
         | empty
    '''

def p_term(p):
    '''
    term : factor term2

    term2 : MULT np_push_operator term 
          | DIV np_push_operator term
          | REMAINDER np_push_operator term 
          | empty
    '''

def p_factor(p):
    '''
    factor : exponent factorB 
    '''

def p_factorB(p):
    '''
    factorB : EXP factor
            | empty
    '''

def p_exponent(p):
    '''
    exponent : L_PAR np_push_operator expression R_PAR np_rpar
        | exponentB 
    '''

def p_exponentB(p):
    ''' 
    exponentB : MINUS var_cte 
        | var_cte 
    '''
    p[0] = p[-1]

def p_var_cte(p):
    '''
    var_cte : var 
         | predef_func
         | func_call
         | CTE_INT np_push_cte_int
         | CTE_FLOAT np_push_cte_float
         | CTE_CHAR np_push_cte_char
         | CTE_STRING np_push_cte_str
         | CTE_BOOL np_push_cte_bool
    '''
    p[0] = p[1]


'''
displays syntax errors on the console
'''
def p_error(p):
    msg = ('Syntax error found at line {0}'.format(lexer.lineno))
    raise SyntaxError(msg)


'''
Acts as an epsilon on the GRAMMAR
'''
def p_empty(p):
    '''
    empty :
    '''

quadruples = []

def gen_assign(vc: bool = False) -> None:
    (operand1, operand2) = stack.get_RL_operands()
    quadruples.append(('=', operand1, None, operand2))
    if vc:
        stack.operands.append(operand2)


def gen_quad(oper: str) -> None:
    (right, left) = stack.get_RL_operands()
    temp = proc_dir.gen_temp(oper, right, left)
    quadruples.append((oper, left, right, temp))
    stack.operands.append(temp)

#######################
# NEURALOGIC POINTS
#######################


'''
neural point that changes the current procedure to either 
program, main or a function/module
'''
def p_np_set_curr_proc(p):
    'np_set_curr_proc : '
    func_name = p[-1]
    if(func_name in ['main', 'program']):
        proc_dir.set_curr_proc(func_name, 'void')
    elif(proc_dir.curr_proc != func_name):
        proc_dir.set_curr_proc(func_name, proc_datatype=p[-2])
    else:
        raise TypeError('Missing type for function: ', func_name)


'''
adds operator to operator stack, and creates quadruple in case the current
operator has less or equal priority to the last operator in the operator stack
'''
def p_np_push_operator(p):
    'np_push_operator : '
    
    while len(stack.operators) > 0 and stack.top(stack.operators) != '(' and stack.priority(stack.operators[-1]) > stack.priority(p[-1]):
        oper = stack.operators.pop()
        if oper == '=':
            gen_assign()
        else:
            gen_quad(oper)
    stack.operators.append(p[-1])

'''
pushes operand to stack and adds it to the variable table
'''
def p_np_push_operand(p):
    'np_push_operand : '
    addr = proc_dir.get_var_addr(p[-1])
    stack.operands.append(addr)

'''
pushes constant int to the operand stack and adds it to the constant table
'''
def p_np_push_cte_int(p):
    'np_push_cte_int : '
    addr = proc_dir.add_const(int(p[-1]), 'int')
    stack.operands.append(addr)

'''
pushes constant float to the operand stack and adds it to the constant table
'''
def p_np_push_cte_float(p):
    'np_push_cte_float : '
    addr = proc_dir.add_const(float(p[-1]), 'float')
    stack.operands.append(addr)

'''
pushes constant char to the operand stack and adds it to the constant table
'''
def p_np_push_cte_char(p):
    'np_push_cte_char : '
    addr = proc_dir.add_const(p[-1], 'char')
    stack.operands.append(addr)

'''
pushes constant string to the operand stack and adds it to the constant table
'''
def p_np_push_cte_str(p):
    'np_push_cte_str : '
    addr = proc_dir.add_const(p[-1], 'string')
    stack.operands.append(addr)

'''
pushes constant bool to the operand stack and adds it to the constant table
'''
def p_np_push_cte_bool(p):
    'np_push_cte_bool : '
    addr = proc_dir.add_const(p[-1], 'bool')
    stack.operands.append(addr)

'''
saves last datatype used, in case of multiple in declarations in a single line
example: 'int: a, b, c;'
'''
def p_np_set_curr_datatype(p):
    'np_set_curr_datatype : '
    proc_dir.curr_datatype = p[-1]

'''
appends datatype to stack
'''
def p_np_add_datatype(p):
    'np_add_datatype : '
    # If the datatype is a comma this means it has
    #  the same datatype as the previous option
    if p[-1] == ',':
        stack.datatypes.append(stack.datatypes[len(stack.datatypes) - 1])
    else:
        stack.datatypes.append(p[-1])

'''
adds variable to the varibale table of the current function
'''
def p_np_add_var(p):
    'np_add_var : '
    proc_dir.add_variable(var_name=p[-1], datatype=proc_dir.curr_datatype, dim=None)

'''
'''
def p_np_add_arr(p):
    'np_add_arr : '
    proc_dir.add_variable(
        var_name=p[-4], datatype=proc_dir.curr_datatype, dim=p[-2])

'''
updates the current function.
example: program, func_name, main
'''
# def p_np_set_curr_scope(p):
#     'np_set_curr_scope : '
#     proc_dir.curr_scope = p[-1]

'''
creates quadruples unitl it finds a left parenthesis on the operator stack
'''


def p_np_rpar(p):
    'np_rpar : '
    oper = stack.operators.pop()
    while oper != '(':
        gen_quad(oper)
        oper = stack.operators.pop()


'''
'''


def p_np_set_return(p):
    'np_set_return : '
    operand = stack.operands.pop()
    datatype = proc_dir.get_curr_proc_datatype
    addr = proc_dir.get_func_return_addr()
    quadruples.append(('RET', operand, None, addr))


'''
creates quadruples until the operator stack is empty
'''
def p_np_end(p):
    'np_end : '
    while len(stack.operators) > 0:
        oper = stack.operators.pop()
        if oper == 'stop':
            break
        if oper == '=':
            gen_assign()
        elif oper in ['+=', '-=', '*=', '/=']:
            (right, left) = stack.get_RL_operands()
            temp = proc_dir.gen_temp(oper[0], right, left)
            quadruples.append((oper[0], left, right, temp))
            quadruples.append(('=', temp, None, left))
        else:
            gen_quad(oper)

'''

'''
def p_np_read(p):
    'np_read : '
    addr = stack.operands.pop()
    quadruples.append(('READ', None, None, addr))


'''

'''
def p_np_write(p):
    'np_write : '
    operand = stack.operands.pop()
    quadruples.append(('WRITE', None, None, operand))


'''

'''
def p_np_set_VC(p):
    'np_set_VC : '
    while len(stack.operators) > 0:
        oper = stack.operators.pop()
        if oper == '=':
            gen_assign(vc=True)
        else:
            gen_quad(oper)

'''

'''
def p_np_comp_VC_VF(p):
    'np_comp_VC_VF : '
    (vf, vc) = stack.get_RL_operands()
    temp = proc_dir.gen_temp('<', vf, vc)
    quadruples.append(('<', vc, vf, temp))
    stack.operands.append(vc)
    stack.jumps.append(len(quadruples)-1)
    quadruples.append(('GOTOF', temp, None, None))
    stack.jumps.append(len(quadruples)-1)

# GOTO's
'''
Add's a GOTO to the quadruples and the number of the quadruple 
to the jump stack
'''
def p_np_GOTO(p):
    'np_GOTO : '
    stack.jumps.append(len(quadruples))
    quadruples.append(('GOTO', None, None, None))


'''
creates gotoF quadruple, it jumps to the position in case
'''
def p_np_GOTOF(p):
    'np_GOTOF : '
    cond = stack.operands.pop()
    stack.jumps.append(len(quadruples))
    quadruples.append(('GOTOF', cond, None, None))


'''
settle the IF GOTOF, add GOTOF quad and position to jump stack
'''
def p_np_GOTO_ELSE(p):
    'np_GOTO_ELSE : '
    goto_index = stack.jumps.pop()
    stack.jumps.append(len(quadruples))
    (a, b, c, d) = quadruples[goto_index]
    quadruples.append(('GOTO', None, None, None))
    quadruples[goto_index] = (a, b, c, len(quadruples))


'''
Add's a the number of the quadruple a GOTO
must got to
'''
def p_np_GOTO_END(p):
    'np_GOTO_END : '
    goto_index = stack.jumps.pop()
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


'''
adds GOTO to the comparison quad before the GOTOF of the while cycle
and sets where the GOTOF ends
'''
def p_np_GOTO_WHILE(p):
    'np_GOTO_WHILE : '
    goto_index = stack.jumps.pop()
    pre_expression = stack.jumps.pop()
    quadruples.append(('GOTO', None, None, pre_expression))
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


'''
'''
def p_np_GOTO_FOR(p):
    'np_GOTO_FOR : '
    var = stack.operands.pop()
    addr = proc_dir.add_const(var_name=1, datatype='int')
    temp = proc_dir.gen_temp('+', addr, var)
    proc_dir.add_temp('int')
    quadruples.append(('+', addr, var, temp))
    quadruples.append(('=', temp, None, var))

    goto_index = stack.jumps.pop()
    comp_vc_vf = stack.jumps.pop()
    quadruples.append(('GOTO', None, None, comp_vc_vf))
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


'''
adds a checkpoint in the jump stack for the expression in a while loop
'''
def p_np_CHECKPOINT(p):
    'np_CHECKPOINT : '
    stack.jumps.append(len(quadruples))

# FUNCTION CONTROL
# function calls must validate function name,
# of arguments and their datatypes
# function must create a space in local memory (variables, )


'''
'''
def p_np_add_param(p):
    'np_add_param : '
    proc_dir.add_param(param_name=p[-1], datatype=p[-3])


'''
'''
def p_np_set_quad_start(p):
    'np_set_quad_start : '
    proc_dir.set_quad_start(len(quadruples))

'''
'''
def p_np_GOSUB(p):
    'np_GOSUB : '
    # jump that changes instruction pointer to a specific line of code
    func_name = p[-5]
    argk = proc_dir.get_curr_arg_k() - 1
    if argk != proc_dir.get_param_num(func_name=p[-5]):
        print('ERROR the number of arguments don`t match the number of params')

    init_address = len(quadruples)
    quadruples.append(('GOSUB', func_name, None, init_address))

    # generate temporal and assign it the value of the
    # return of the function unless function is void

    datatype = proc_dir.get_proc_datatype(func_name)
    if(datatype != 'void'):
        temp = proc_dir.memory['temp']['curr_addr'][datatype]
        proc_dir.memory['temp']['curr_addr'][datatype] += 1
        addr = proc_dir.get_func_return_addr()
        quadruples.append(('=', addr, None, temp))
        #proc_dir.add_variable(temp, datatype)
        proc_dir.add_temp(datatype)
        stack.operands.append(temp)

'''
adds ERA quadruple, for calculating function memory size at run time
'''
def p_np_ERA(p):
    'np_ERA : '
    if proc_dir.exist_proc(proc_name=p[-1]):
        func_name = p[-1]
        proc_dir.func_call = func_name
        quadruples.append(('ERA', None, None, func_name))
        proc_dir.reset_curr_arg_k()
    else:
        msg = 'ERROR undefined Function: "{0}"'.format(p[-1])
        raise ValueError(msg)
        p_error(p)

'''
creates param quadruple
'''
def p_np_param(p):
    'np_param : '
    arg = stack.operands.pop()
    argk = proc_dir.get_curr_arg_k()
    quadruples.append(('PARAM', arg, None, argk))

'''
borra memoria temporal que se uso para ejecutar la funcion
'''
def p_np_ENDFunc(p):
    'np_ENDFunc : '
    quadruples.append(('ENDFUNC', None, None, None))
    proc_dir.set_quad_end(len(quadruples) - 1)
    #proc_dir.reset_local_and_temp()

'''
adds a stop in the operator stack, to stop evaluating the expression
'''
def p_np_arr_start(p):
    'np_arr_start : '
    stack.operators.append('stop')

def p_np_arr_end(p):
    'np_arr_end : '
    index = stack.operands.pop()
    dirB = proc_dir.get_var_addr(var_name=p[-5])
    var_dim = proc_dir.get_var_dim(var_name=p[-5])
    linf = proc_dir.add_const(0, datatype='int')
    lsup = proc_dir.add_const(var_dim, datatype='int')
    datatype = proc_dir.get_var_datatype(var_name=p[-5])

    # necesito generar una direcion que sea
    # igual a la suma de la direcion base y el indice
    # y ponerla en mi stack te operadores
    #print(dirB,var_dim, linf, index,datatype)
    quadruples.append(('VER', index, linf, lsup))
    ptr = proc_dir.gen_ptr()

    quadruples.append(('[+]', dirB, index, ptr))
    print('index', index, var_dim)
    stack.operands.append(ptr)
    # print(p[-5],dirB,index)

    # gen_quad(oper='+')

'''
'''
def p_np_stop(p):
    'np_stop : '
    stack.operators.append('stop')

'''
'''
def p_np_prog_end(p):
    'np_prog_end : '
    proc_dir.procedures['program']['quad_range'] = [0, len(quadruples)]
    quadruples.append(('ENDPROG', None, None, None))

# Build the parser
parser = yacc.yacc()

def print_quadruples() -> None:
    for index, quad in enumerate(quadruples):
        (a, b, c, d) = quad
        [a] = ['_' if a == None else a]
        [b] = ['_' if b == None else b]
        [c] = ['_' if c == None else c]
        [d] = ['_' if d == None else d]
        print('{0}:\t({1},{2},{3},{4})'.format(index, a, b, c, d))


def quad_to_json(quadruples):
    obj = {'proc_dir': {}, 'quads': {}, 'const_table': {}}
    for index, quad in enumerate(quadruples):
        (a, b, c, d) = quad
        obj['quads'][index] = {'oper': a, 'left': b, 'right': c, 'res': d}
    obj['proc_dir'] = proc_dir.procedures
    obj['const_table'] = proc_dir.const_table
    return json.dumps(obj, indent=4)


def gen_obj_code(quadruples) -> None:
    json_object = quad_to_json(quadruples)
    with open('code.json', 'w') as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError('No file name was provided')
        file = open(sys.argv[1], 'r')
        code = ''
        for line in file:
            code += line
        parser.parse(code)
        gen_obj_code(quadruples)
        proc_dir.print_procedure_directory()
        proc_dir.print_var_tables()
        print_quadruples()
        # stack.print_all_stacks()
        print(proc_dir.const_table)

        v = VM()
        v.execute()
    except EOFError:
        raise SyntaxError('Error')