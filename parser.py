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
import procedure_dir
import ply.yacc as yacc
from lexer import tokens, lexer
from stack import Stack
from obj import OBJ
from vm import VM

proc_dir = procedure_dir.procedure_dir()
stack = Stack()
obj = OBJ()


def p_program(p):
    '''
    program : PROGRAM np_set_curr_proc ID np_GOTO SEMICOLON programB np_prog_end

    programB : vars  programC 
             | programC

    programC : function programC
             | main      
    '''

def p_vars(p):
    '''
    vars : VARS L_BRACE varsB R_BRACE 

    varsB : type np_set_curr_datatype COLON varsC SEMICOLON
          | type np_set_curr_datatype COLON varsC SEMICOLON varsB

    varsC : varsD 
          | varsD COMMA varsC

    varsD : ID np_add_var
          | ID L_BRACKET  CTE_INT R_BRACKET np_add_arr 
    '''


def p_function(p):
    '''
    function : FUNCTION func_type ID np_set_curr_proc L_PAR functionB R_PAR np_set_quad_start vblock np_ENDFunc 

    functionB : params
              | empty
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
    var : ID L_BRACKET np_stop exp np_end np_arr_end R_BRACKET
        | ID np_push_operand
    '''
    p[0] = p[1]


def p_func_type(p):
    '''
    func_type : VOID np_add_datatype 
              | type
    '''
    p[0] = p[1]

def p_params(p):
    '''
    params : type COLON ID np_add_param
           | type COLON ID np_add_param COMMA params
           | empty
    '''

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
              | PLOTXY L_PAR ID  COMMA ID  R_PAR np_def_func_2param SEMICOLON
              | REGRESSION L_PAR ID  COMMA ID  R_PAR np_def_func_2param SEMICOLON
    '''


def p_assign(p):
    '''
    assign : var oper_assign np_push_operator expression np_end SEMICOLON
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

    writeB : expression np_end np_write writeC
           | CTE_STRING np_push_cte_str np_write writeC

    writeC : COMMA writeB
           | empty      
    '''

def p_loop_cond(p):
    '''
    loop_cond : WHILE L_PAR np_CHECKPOINT expression R_PAR  np_end np_GOTOF block np_GOTO_WHILE
    '''


def p_loop_range(p):
    '''
    loop_range : FOR var EQUAL np_push_operator exp np_set_CV TO exp np_end np_comp_CV_FV block np_GOTO_FOR
    '''


def p_return(p):
    '''
    return : RETURN L_PAR np_stop exp np_end np_set_return R_PAR SEMICOLON
    '''


def p_func_call(p):
    '''
    func_call : ID np_ERA L_PAR func_callB R_PAR np_GOSUB

    func_callB : func_call_arguments
                | empty
    '''
    
def p_func_call_arguments(p):
    '''
    func_call_arguments : np_stop exp np_end np_param func_call_argumentsB

    func_call_argumentsB : COMMA func_call_arguments
                         | empty
    '''

def p_def_func(p):
    '''
    def_func : def_funcB L_PAR ID  R_PAR np_def_func_1param
    
    def_funcB : MIN
              | MAX
              | MEAN
              | MEDIAN
              | MODE
              | VARIANCE
    '''
    p[0] = p[1]

def p_oper_assign(p):
    '''
    oper_assign : EQUAL 
        | MULT_EQ 
        | DIV_EQ 
        | PLUS_EQ 
        | MINUS_EQ 
    '''
    p[0] = p[1]

def p_expression(p):
    '''
    expression : logic expressionB 

    expressionB : OR np_push_operator expression 
          | AND np_push_operator expression
          | empty
    '''

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
    term : exponent term2

    term2 : MULT np_push_operator term 
          | DIV np_push_operator term
          | REMAINDER np_push_operator term 
          | empty
    '''

def p_exponent(p):
    '''
    exponent : factor exponentB 

    exponentB : EXP np_push_operator exponent
              | empty   
    '''

def p_factor(p):
    '''
    factor : L_PAR np_push_operator expression R_PAR np_rpar
        | var_cte
        
    '''

def p_var_cte(p):
    '''
    var_cte : var 
         | func_call
         | def_func
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
    """displays syntax errors

    Raises:
        SyntaxError: outputs the line number where the error was found
    """
    msg = ('Syntax error found at line {0}'.format(lexer.lineno))
    raise SyntaxError(msg)


def p_empty(p):
    '''
    empty :
    '''
    """
    acts a s epsilon inside the GRAMMAR
    """

quadruples = []


def gen_assign(cv: bool = False) -> None:
    """generates an assign quadruple

    Args:
        vc (bool, optional): indicates if its a control variable in a for loop.
            Defaults to False.
    """
    (operand1, operand2) = stack.get_RL_operands()
    quadruples.append(('=', operand1, None, operand2))
    if cv:
        stack.operands.append(operand2)


def gen_quad(oper: str) -> None:
    """generates a quadruple 

    Args:
        oper (str): operator
    """
    (right, left) = stack.get_RL_operands()
    temp = proc_dir.gen_temp(oper, right, left)
    quadruples.append((oper, left, right, temp))
    stack.operands.append(temp)

#######################
# NEURALOGIC POINTS
#######################


def p_np_set_curr_proc(p):
    'np_set_curr_proc : '
    """changes current procedure

    Raises:
        TypeError: [description]
    """
    func_name = p[-1]
    if(func_name in ['main', 'program']):
        proc_dir.set_curr_proc(func_name, 'void')
    elif(proc_dir.curr_proc != func_name):
        proc_dir.set_curr_proc(func_name, proc_datatype=p[-2])
    else:
        msg = 'Missing type for function: "{0}"'.format(func_name)
        raise TypeError(msg)


def p_np_push_operator(p):
    'np_push_operator : '
    """adds operator to operator stack, and creates quadruple if the current
    operator has less or equal priority to the last operator in the operator stack
    """
    while len(stack.operators) > 0 and stack.top(stack.operators) != '(' and stack.priority(stack.operators[-1]) > stack.priority(p[-1]):
        oper = stack.operators.pop()
        if oper == '=':
            gen_assign()
        else:
            gen_quad(oper)
    stack.operators.append(p[-1])


def p_np_push_operand(p):
    'np_push_operand : '
    """pushes operand to the operand stack and adds 
    it to the variable table of the current procedure
    """
    addr = proc_dir.get_var_addr(p[-1])
    stack.operands.append(addr)


def p_np_push_cte_int(p):
    'np_push_cte_int : '
    """pushes constant int to the operand 
    stack and adds it to the constant table
    """
    addr = proc_dir.add_const(int(p[-1]), 'int')
    stack.operands.append(addr)


def p_np_push_cte_float(p):
    'np_push_cte_float : '
    """pushes constant float to the operand 
    stack and adds it to the constant table
    """
    addr = proc_dir.add_const(float(p[-1]), 'float')
    stack.operands.append(addr)


def p_np_push_cte_char(p):
    'np_push_cte_char : '
    """pushes constant char to the operand 
    stack and adds it to the constant table
    """
    addr = proc_dir.add_const(p[-1], 'char')
    stack.operands.append(addr)


def p_np_push_cte_str(p):
    'np_push_cte_str : '
    """pushes constant string to the operand 
    stack and adds it to the constant table
    """
    addr = proc_dir.add_const(p[-1], 'string')
    stack.operands.append(addr)


def p_np_push_cte_bool(p):
    'np_push_cte_bool : '
    """pushes constant bool to the operand 
    stack and adds it to the constant table
    """
    addr = proc_dir.add_const(p[-1], 'bool')
    stack.operands.append(addr)


def p_np_set_curr_datatype(p):
    'np_set_curr_datatype : '
    """Saves last datatype used, in case of multiple 
    in declarations in a single line, example: 'int: a, b, c;'
    """
    proc_dir.curr_datatype = p[-1]


def p_np_add_datatype(p):
    'np_add_datatype : '
    """appends datatype to datatype stack. In the datatype is a 
    comma the last datatype used will be pushed instead.
    """
    if p[-1] == ',':
        stack.datatypes.append(stack.datatypes[len(stack.datatypes) - 1])
    else:
        stack.datatypes.append(p[-1])


def p_np_add_var(p):
    'np_add_var : '
    """adds variable to the varibale table of the current function
    """
    datatype=proc_dir.curr_datatype
    proc_dir.add_variable(var_name=p[-1], datatype=datatype, dim=None)


def p_np_add_arr(p):
    'np_add_arr : '
    """Adds an array to the varaible table of the current procedure
    """
    datatype=proc_dir.curr_datatype
    proc_dir.add_variable(var_name=p[-4], datatype=datatype, dim=p[-2])


def p_np_rpar(p):
    'np_rpar : '
    """will generates quadruples until it finds a left parenthesis
    """
    oper = stack.operators.pop()
    while oper != '(':
        gen_quad(oper)
        oper = stack.operators.pop()


def p_np_set_return(p):
    'np_set_return : '
    """Generats a RETURN quadruple
    """
    if proc_dir.curr_proc in ["main","program"]:
        raise SyntaxError("Procedures main or program can't have a return statement")
    operand = stack.operands.pop()
    datatype = proc_dir.get_curr_proc_datatype
    func_name = proc_dir.curr_proc
    addr = proc_dir.get_func_return_addr(func_name)

    if operand == None:
        msg = f"function {func_name} returns a non existant value"
        raise ValueError(msg)
    quadruples.append(('RET', operand, None, addr))


def p_np_end(p):
    'np_end : '
    """Generates quadruples until the operator stack is empty or finds a stop
    """
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


def p_np_read(p):
    'np_read : '
    """generates a READ quadruple
    """
    addr = stack.operands.pop()
    if addr == None:
        raise ValueError("Trying to read non existant variable")
    quadruples.append(('READ', None, None, addr))


def p_np_write(p):
    'np_write : '
    """generates a WRITE quadruple
    """
    operand = stack.operands.pop()
    if operand == None:
        raise ValueError("Trying to write non existant value")
    quadruples.append(('WRITE', None, None, operand))


def p_np_set_CV(p):
    'np_set_CV : '
    """sets the control variable of a for loop
    """
    while len(stack.operators) > 0:
        oper = stack.operators.pop()
        if oper == '=':
            gen_assign(cv=True)
        else:
            gen_quad(oper)


def p_np_comp_CV_FV(p):
    'np_comp_CV_FV : '
    """creates quadruples to compare the control variable to the final value
    """
    (fv, cv) = stack.get_RL_operands()
    temp = proc_dir.gen_temp('<', fv, cv)
    quadruples.append(('<', cv, fv, temp))
    stack.operands.append(cv)
    stack.jumps.append(len(quadruples)-1)
    quadruples.append(('GOTOF', temp, None, None))
    stack.jumps.append(len(quadruples)-1)


def p_np_GOTO(p):
    'np_GOTO : '
    """Add's a GOTO quadruple to the quadruple list and
    the number of the current quadruple to the jump stack
    """
    stack.jumps.append(len(quadruples))
    quadruples.append(('GOTO', None, None, None))



def p_np_GOTOF(p):
    'np_GOTOF : '
    """ pushes GOTOF quadruple to the quadrule list,
    and pushes current quadruple number to the jump stack
    """
    cond = stack.operands.pop()
    stack.jumps.append(len(quadruples))
    quadruples.append(('GOTOF', cond, None, None))


def p_np_GOTO_ELSE(p):
    'np_GOTO_ELSE : '
    """close the IF GOTOF, add GOTO quadruple 
    and current cuadruple number to jump stack
    """
    goto_index = stack.jumps.pop()
    stack.jumps.append(len(quadruples))
    (a, b, c, d) = quadruples[goto_index]
    quadruples.append(('GOTO', None, None, None))
    quadruples[goto_index] = (a, b, c, len(quadruples))


def p_np_GOTO_END(p):
    'np_GOTO_END : '
    """Add's a the number of the quadruple a GOTO must lead to
    """
    goto_index = stack.jumps.pop()
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


def p_np_GOTO_WHILE(p):
    'np_GOTO_WHILE : '
    """adds GOTO to the comparison quad before the GOTOF of the while cycle
    and sets where the GOTOF ends
    """
    goto_index = stack.jumps.pop()
    pre_expression = stack.jumps.pop()
    quadruples.append(('GOTO', None, None, pre_expression))
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


def p_np_GOTO_FOR(p):
    'np_GOTO_FOR : '
    """Generates a SUM and ASSIGN quadruples to increase the value of the 
    control varaible at the end of the for loop, then it generates a GOTO 
    to the expression that compares the control variable to the final value
    """
    var = stack.operands.pop()
    addr = proc_dir.add_const(var_name=1, datatype='int')
    temp = proc_dir.gen_temp('+', addr, var)
    quadruples.append(('+', addr, var, temp))
    quadruples.append(('=', temp, None, var))

    goto_index = stack.jumps.pop()
    comp_cv_fv = stack.jumps.pop()
    quadruples.append(('GOTO', None, None, comp_cv_fv))
    (a, b, c, d) = quadruples[goto_index]
    quadruples[goto_index] = (a, b, c, len(quadruples))


def p_np_CHECKPOINT(p):
    'np_CHECKPOINT : '
    """adds a checkpoint in the jump stack, so that the while 
    loop can return to the expression at the end of the loop
    """
    stack.jumps.append(len(quadruples))


def p_np_add_param(p):
    'np_add_param : '
    """Adds a param and a datatype to the current function
    """

    proc_dir.add_param(param_name=p[-1], datatype=p[-3])


def p_np_set_quad_start(p):
    'np_set_quad_start : '
    """sets the quadruple where the current function starts
    """
    proc_dir.set_quad_start(len(quadruples))


def p_np_GOSUB(p):
    'np_GOSUB : '
    """Adds a GOSUB of a given function quadruple to the quadruple list.
    In case the function isn't void it assigns a temporal var the value of
    the global variable belonging to the function

    Raises:
        ValueError: in case the number of parameters and argk dont match
    """
    func_name = p[-5]
    argk = proc_dir.get_curr_arg_k() - 1
    if argk != proc_dir.get_param_len(func_name):
        msg = 'The number of arguments doesn`t match the number of parameters'
        raise ValueError(msg)

    current_address = len(quadruples)
    quadruples.append(('GOSUB', func_name, None, current_address))

    datatype = proc_dir.get_proc_datatype(func_name)
    if(datatype != 'void'):
        temp = proc_dir.memory['temp']['curr_addr'][datatype]
        proc_dir.memory['temp']['curr_addr'][datatype] += 1
        addr = proc_dir.get_func_return_addr(func_name)
        quadruples.append(('=', addr, None, temp))
        stack.operands.append(temp)


def p_np_ERA(p):
    'np_ERA : '
    """adds ERA quadruple, for calculating function memory size at run time

    Raises:
        ValueError: In case the function is undefined
    """
    func_name = p[-1]
    if proc_dir.procedures.get(func_name) != None:
        proc_dir.func_call = func_name
        quadruples.append(('ERA', None, None, func_name))
        proc_dir.reset_curr_arg_k()
    else:
        msg = 'Undefined function: "{0}"'.format(func_name)
        raise ValueError(msg)
        p_error(p)


def p_np_param(p):
    'np_param : '
    """generates a PARAM quadruple 
    """
    argument = stack.operands.pop()
    if argument == None:
        raise ValueError("Function argument doesn't exist")
    argk = proc_dir.get_curr_arg_k()
    quadruples.append(('PARAM', argument, None, argk))


def p_np_ENDFunc(p):
    'np_ENDFunc : '
    """pushes a ENDFUNC quadruple to the quadruple list
    """
    quadruples.append(('ENDFUNC', None, None, None))
    proc_dir.reset_local_and_temp()


def p_np_arr_end(p):
    'np_arr_end : '
    """neural point for the end of arrays it generates a Verify index 
    quadruple (VER, index, upper_lim, lower_lim). Then it generates a 
    quadruple that generates a pointer that points to the base address + index
    """
    index = stack.operands.pop()
    dirB = proc_dir.get_var_addr(var_name=p[-5])
    var_dim = proc_dir.get_var_dim(var_name=p[-5])
    llim = proc_dir.add_const(0, datatype='int')
    ulim = proc_dir.add_const(var_dim, datatype='int')
    addr = proc_dir.get_var_addr(var_name=p[-5])
    
    index_datatype = proc_dir.get_addr_datatype(index)
    if index_datatype != 'int':
        raise ValueError('Array index must be a integer value')
    quadruples.append(('VER', index, llim, ulim))
    ptr = proc_dir.gen_ptr()
    quadruples.append(('[+]', dirB, index, ptr))
    stack.operands.append(ptr)


def p_np_stop(p):
    'np_stop : '    
    """Adds a 'stop' operator to the operator stack,
    this is for stoping the evaluation of an expression
    """
    stack.operators.append('stop')


def p_np_prog_end(p):
    'np_prog_end : '
    """Adds a quadruple that indicates the end
    of the program
    """
    quadruples.append(('ENDPROG', None, None, None))

def p_np_def_func_1param(p):
    'np_def_func_1param : ' 
    """
    neural point for working with predefined functions that have exactly
    1 parameter
    """
    oper = p[-4].upper()
    addr = proc_dir.get_var_addr(p[-2])
    dim = proc_dir.get_var_dim(var_name=p[-2])
    datatype = proc_dir.get_addr_datatype(addr)
    temp = proc_dir.memory['temp']['curr_addr'][datatype]
    quadruples.append((oper,addr,dim,temp))
    stack.operands.append(temp)


def p_np_def_func_2param(p):
    'np_def_func_2param : '
    """neural point for predefined functions that have exactly 
    2 parameters
    """
    func_name = p[-6]
    oper = func_name.upper()
    addr1 = proc_dir.get_var_addr(var_name=p[-4])
    addr2 = proc_dir.get_var_addr(var_name=p[-2])
    dim1 = proc_dir.get_var_dim(var_name=p[-4])
    dim2 = proc_dir.get_var_dim(var_name=p[-2])
    datatype1 = proc_dir.get_addr_datatype(addr1)
    datatype2 = proc_dir.get_addr_datatype(addr2)
    invalid_types = ['bool','char','string']
    if datatype1 in invalid_types or datatype2 in invalid_types:
        msg = f"function {func_name} only accepts arrays of int's or float's"
        raise TypeError(msg)
    quadruples.append((oper,addr1,dim1,None))
    quadruples.append((oper,addr2,dim2,None))
   

# Build the parser
parser = yacc.yacc()


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError('No file name was provided')
        file = open(sys.argv[1], 'r')
        code = ''
        for line in file:
            code += line
        parser.parse(code)
        obj.gen_obj_code(quadruples,proc_dir.procedures,proc_dir.const_table)
        #proc_dir.print_procedure_directory()
        #proc_dir.print_var_tables()
        # obj.print_quadruples(quadruples)
        # stack.print_all_stacks()
        # print(proc_dir.const_table)

        v = VM()
        v.execute()
    except EOFError:
        raise SyntaxError('EOF Error')