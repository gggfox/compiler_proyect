'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   procedure_dir.py        #
#   Created_at 2021-09-28   #
#                           #
#############################
''' 

from tabulate import tabulate
from semanticCube import SemanticCube
from memory_architecture import memory
'''
    PROCEDURE DIRECTORY
    -------------------
    name      -> name of the procedure
    datatype  -> datatype of the procedure 
    size      -> memory size of the procedure
    params    -> a vector of the datatypes expected by the params
    var_table -> a table of all the variables in the procedure.

    VARIABLE TABLE
    --------------

'''
class procedure_dir():
    def __init__(self):
        self.curr_proc = ''
        self.curr_quadruple = 0
        self.curr_temp = 0
        self.curr_datatype = ''
        self.procedures = {}
        self.variable_stack = []
        self.curr_arg_k = 0
        self.memory = memory
        self.const_table = {
            'int':{},
            'float':{},
            'char':{},
            'string':{},
            'bool':{}
        }

    '''
    '''
    def get_curr_temp(self) -> int:
        """updates the current temporal counter,
        increases the total number of temporals in the 
        current procedure and returns the temporal

        Returns:
            int: temporal counter
        """
        self.curr_temp += 1
        self.procedures[self.curr_proc]['temps'] += 1
        return self.curr_temp

    '''
    '''
    def add_temp(self, datatype:str) -> None:
        self.procedures[self.curr_proc]['size']['temp'][datatype] += 1

    '''
    '''
    def gen_temp(self, operator:str, operand1:str, operand2:str) -> str:
        var1 = self.get_var_datatype(operand1)
        var2 = self.get_var_datatype(operand2)


        # Catch cte ints and floats
        if var1 == 'ERROR':
            [_,var1,_] = str(type(operand1)).split('\'')
        if var2 == 'ERROR':
            [_,var2,_] = str(type(operand2)).split('\'')


        # print(operand1,operand2)
        # print(operator,var1,var2)
        #self.print_var_tables()
        #print(operator,var1,var2,operand1,operand2)
        temp_datatype = SemanticCube[operator][var1][var2]
        self.add_temp(temp_datatype)    
        temp = 'temp'+str(self.get_curr_temp())   
        addr = self.memory['temp']['curr_addr'][temp_datatype]
        self.memory['temp']['curr_addr'][temp_datatype] += 1
        self.add_variable(addr, temp_datatype, addr, 'temp')
        #print(addr)
        return addr

    '''
    '''
    def reset_curr_temp(self) -> None:
        self.curr_temp = 0

    '''
    '''    
    def get_curr_quadruple(self) -> int:
        
        self.curr_quadruple += 1
        return self.curr_quadruple


    def set_curr_proc(self, proc_name: str, proc_datatype:str = 'void') -> None:
        """changes the current procedure and adds it to the procedure directory

        Args:
            proc_name (str): name of the procedure 
            proc_datatype (str, optional): the datatype of the procedure it is
                void in case its main or the program. Defaults to 'void'.
        """
        self.curr_proc = proc_name
        self.add_procedure(proc_name, proc_datatype)
    
    def get_curr_proc_datatype(self) -> str:
        """returns the type of the current procedure

        Returns:
           datatype [str]: string that indicates datatype 
        """
        proc_name = self.curr_proc
        datatype = self.get_proc_datatype(proc_name)
        return datatype

    def get_proc_datatype(self, proc_name:str)->str:
        datatype = self.procedures[proc_name]['datatype']
        return datatype

    def print_procedure_directory(self) -> None:
        """Prints the procedure directory in console"""
        header = ['name', 'datatype','quad range','#params','#vars','#temps','li','lf','lb','lc','ls','ti','tf','tb','tc','ts']
        data = []
        
        for proc in self.procedures:
            datatype = self.procedures[proc]['datatype']
            quad_range = self.procedures[proc]['quad_range']
            params = len(self.procedures[proc]['param_vector'])
            variables = len(self.procedures[proc]['var_table']) - params
            temps = self.procedures[proc]['temps']

            # local ints, floats, bools, chars, strings
            li = self.procedures[proc]['size']['local']['int']
            lf = self.procedures[proc]['size']['local']['float']
            lb = self.procedures[proc]['size']['local']['bool']
            lc = self.procedures[proc]['size']['local']['char']
            ls = self.procedures[proc]['size']['local']['string']
            
            # temporal ints, floats, bools, chars, strings
            ti = self.procedures[proc]['size']['temp']['int']
            tf = self.procedures[proc]['size']['temp']['float']
            tb = self.procedures[proc]['size']['temp']['bool']
            tc = self.procedures[proc]['size']['temp']['char']
            ts = self.procedures[proc]['size']['temp']['string']

            res = [proc, datatype, quad_range, params, variables, temps]
            res += [li, lf, lb, lc, ls, ti, tf, tb, tc, ts] #size 
            data.append(res)
        print('\n',' '*16,'PROCEDURE DIRECTORY')
        print(tabulate(data, headers=header, tablefmt='fancy_grid'),'\n')

    def print_var_tables(self) -> None:
        """Prints the varaible table in console"""
        header = ['Name', 'Datatype', 'Scope','Belongs to','Address','Dim']
        data = []
        procs = self.procedures
        for proc_name in procs:
            for var_name in procs[proc_name]['var_table']:
                datatype = procs[proc_name]['var_table'][var_name]['datatype']
                scope = procs[proc_name]['var_table'][var_name]['scope']
                address = procs[proc_name]['var_table'][var_name]['address']
                dim = procs[proc_name]['var_table'][var_name]['dim']
                data.append([var_name, datatype, scope, proc_name, address,dim])
        for datatype in self.const_table:
            for const in self.const_table[datatype]:
                data.append([const, datatype, 'const', 'const',self.const_table[datatype][const]])
                #print(const)
        print(' '*15,'VARIABLE TABLE')
        print(tabulate(data, headers=header, tablefmt='fancy_grid'),'\n')

    def get_dim(self, var_name:str) -> int:
        dim = self.procedures[self.curr_proc]['var_table'][var_name].get('dim')
        if dim != None:
            return dim
        # dim = self.procedures['global']['var_table'][var_name].get('dim')
        # if dim != None:
        #     return dim
        
    # def get_arr_dim(self, var):
    #     if self.procedures[self.curr_proc]['var_table'][var]['dim'] != None:
    #         return self.procedures[self.curr_proc]['var_table'][var]['dim']
    #     elif self.procedures['global']['var_table'][var]['dim'] != None:
    #         return self.procedures['global']['var_table'][var]['dim']
    #     else:
    #         return None

    '''
    This function is used to collect varibales(name, datatype, scope) in a
    stack that gets emptied when a new procedure is added to the object

    '''    
    def add_variable(self, var_name:str, datatype:str = '', addr:int = -1, scope:str = 'local', dim:int = None):
        if datatype == '':
            datatype = self.curr_datatype
        if self.exist_global_var(var_name):
            raise ValueError('Error a global variable with that name alredy exists')
        if self.procedures[self.curr_proc]['var_table'].get(var_name) != None:
            msg = f'Error repeated variable name:{var_name} in {self.curr_proc}'
            raise ValueError(msg)
        [scope] = ['global' if self.curr_proc == 'program' else scope]
        if addr == -1:
            addr = self.memory['local']['curr_addr'][datatype]
            self.memory['local']['curr_addr'][datatype] += 1
        data = {
            'datatype':datatype, 
            'scope': scope,
            'address': addr,
            'dim': dim
        }
        self.procedures[self.curr_proc]['var_table'][var_name] = data
        if scope != 'global':
            self.procedures[self.curr_proc]['size'][scope][datatype] += 1

    def add_const(self, var_name:str, datatype:str) -> int:
        if datatype == 'string' or datatype == 'char':
            var_name = var_name[1:-1]
        if self.const_table[datatype].get(var_name) == None:
            addr = self.memory['const']['curr_addr'][datatype]
            self.memory['const']['curr_addr'][datatype] += 1
            self.const_table[datatype].update({var_name:addr})
            #self.const_table[datatype].update({addr:var_name})
            return int(addr)
        else:
            return self.const_table[datatype].get(var_name)

    '''
    This function adds a new procedure to the procedure directory
    the size is # of vars per type and temporals per type (temp i, temp f)
    '''
    def add_procedure(self, proc_name:str, proc_datatype:str):
        # Test for existing procedures
        if self.exist_proc(proc_name):
            raise ValueError('Error that procedure with that name already exists')
        self.procedures[proc_name] = {
            'datatype':proc_datatype,
            'size': {
                'local':{
                    'int': 0,
                    'float':0,
                    'bool':0,
                    'char':0,
                    'string':0
                },
                'temp':{
                    'int': 0,
                    'float':0,
                    'bool':0,
                    'char':0,
                    'string':0
                }
            },
            'quad_range':(None,None),
            'param_vector':[],
            'var_table':{},
            'temps':0
        }
        if proc_datatype != 'void':
            addr = self.memory['global']['curr_addr'][proc_datatype]
            self.memory['global']['curr_addr'][proc_datatype] += 1
            self.add_variable(addr, proc_datatype, addr,'global' )

    def reset_curr_arg_k(self) -> None:
        """sets the counter of current arguments to 0"""
        self.curr_arg_k = 0
    
    def get_curr_arg_k(self) -> int:
        """returns the updated argument number

        Returns:
            int: number of current argument 
        """
        self.curr_arg_k += 1
        return self.curr_arg_k

    def get_param_num(self, func_name:str) -> int:
        """returns the lenght of the parameter vector of a function

        Args:
            func_name (str): name of a function/module

        Returns:
            int: the number of parameters of a given function
        """
        return len(self.procedures[func_name]['param_vector'])
    
    '''
    Adds a param datatype to the current procedure
    '''
    def add_param(self, param_name:str, datatype:str) -> None:
        """ Adds a parameter to the parameter vector of a function
        and to its variable table

        Args:
            param_name (str): name of the parameter to be added
            datatype (str): datatype of the parameter to be added
        """
        self.procedures[self.curr_proc]['param_vector'].append(datatype)
        self.add_variable(param_name, datatype)


    '''
    Sets the start of a quadruple to a given integer
    '''
    def set_quad_start(self, quad_start:int) -> None:
        self.procedures[self.curr_proc]['quad_range'] = (quad_start,None)

    '''
    Sets the start of a quadruple to a given integer
    '''
    def set_quad_end(self, quad_end:int) -> None:
        (start,_) = self.procedures[self.curr_proc]['quad_range'] 
        self.procedures[self.curr_proc]['quad_range'] = (start, quad_end)

    '''
    '''
    def exist_proc(self, proc_name):
        try:
            return self.procedures[proc_name]
        except:
            return False

    '''
    '''
    def exist_local_var(self, proc_name, var_name):
        try:
            if self.procedures[proc_name]['var_table'][var_name]:
                return True 
        except:
            return False

    '''
    '''
    def is_cte(self, var) -> (bool,str):
        res = 'int'
        for x in range(len(var)):
            if var[x] == '.' and res != 'float':
                res = 'float'
            if not var[x] in ['0','1','2','3','4','5','6','7','8','9']:
                return False,_
        return True, res

        
    '''
    '''
    def get_var_datatype(self, var_name:str, proc_name:str = '') -> str:
        try:
            [proc_name] = [self.curr_proc if proc_name == '' else proc_name]
            procs = self.procedures
            dt = procs[proc_name]['var_table'][var_name]['datatype']
            return dt    
        except:
            return 'ERROR'

    def get_var_addr(self, var_name:str) -> int:
        try:
            res = self.procedures[self.curr_proc]['var_table'][var_name]['address']
            if res == None:
                res = self.curr_proc['global']['var_table'][var_name]['address']
            return res
        except:
            return -1
            msg = f'A variable with the name "{var_name}" does not exist'
            raise NameError(msg)
        
    '''
    '''
    def exist_global_var(self, var_name):
        try:
            if self.procedure['program']['var_table'][var_name]:
                return True
        except:
            return False

    '''
    '''
    def search_var(self, proc_name:str, var_name:str):
        if not self.search_proc(proc_name):
            return 'Error there is no procedure with that name'
        if self.exist_local_var(proc_name, var_name):
            return self.procedures[proc_name]['var_table'][var_name]
        elif self.exist_global_var(var_name):
            return self.procedures['program']['var_table'][var_name]
        else:
            msg = "Error variable '{0}' isn't associated with procedure '{1}'"
            return msg.format(var_name,proc_name)

    '''
    '''
    def search_proc(self, proc_name:str):
        if self.exist_proc(proc_name):
            return self.procedures[proc_name]
        else:
            msg = "Error there is no procedure with the name:{0}"
            return msg.format(proc_name)


if __name__ == '__main__':
    pass