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

class procedure_dir():
    def __init__(self):
        self.curr_proc = ''
        self.curr_quadruple = 0
        self.curr_temp = 0
        self.curr_datatype = ''
        self.func_call = ''
        self.procedures = {}
        self.curr_arg_k = 0
        self.memory = memory
        self.const_table = {
            'int':{},
            'float':{},
            'char':{},
            'string':{},
            'bool':{}
        }


    def get_curr_temp(self) -> int:
        """updates the current temporal counter, increases the total 
        number of temporals in the current procedure and returns the temporal

        Returns:
            int: temporal counter
        """
        self.curr_temp += 1
        self.procedures[self.curr_proc]['temps'] += 1
        return self.curr_temp

  
    def add_temp(self, datatype:str) -> None:
        """increments the temporal variable counter for a given fucntion

        Args:
            datatype (str): temporal datatype
        """
        self.procedures[self.curr_proc]['size']['temp'][datatype] += 1


    def gen_temp(self, operator:str, operand1:str, operand2:str) -> int:
        """generates a temporal variable

        Args:
            operator (str): operator
            operand1 (str): left operand
            operand2 (str): right operand

        Raises:
            TypeError: Value mismatch

        Returns:
            int: address
        """
        try:
            var1 = self.get_addr_datatype(operand1)
            var2 = self.get_addr_datatype(operand2)


            # Catch cte ints and floats
            if var1 == 'ERROR':
                [_,var1,_] = str(type(operand1)).split('\'')
            if var2 == 'ERROR':
                [_,var2,_] = str(type(operand2)).split('\'')

            if var1 in ["string","char"] and var2 in ["int","float","bool"]:
                operand2 = str(operand2)
                var2 = var1

            if var2 in ["string","char"] and var1 in ["int","float","bool"]:
                operand1 = str(operand1)
                var1 = var2

            # print(operand1,operand2)
            # print(operator,var1,var2)
            #self.print_var_tables()
            #print(operator,var1,var2,operand1,operand2)
            temp_datatype = SemanticCube[operator][var1][var2]
            #print(temp_datatype,var1,var2)
            self.add_temp(temp_datatype)    
            temp = 'temp'+str(self.get_curr_temp())   
            addr = self.memory['temp']['curr_addr'][temp_datatype]
            self.memory['temp']['curr_addr'][temp_datatype] += 1
            self.add_variable(addr, temp_datatype, addr, 'temp')
            return addr
        except:
            #print(operand1,operand2,var1,var2,operator)
            msg = "Error while trying operation: {0} {1} {2}".format(var1,operator,var2)
            raise TypeError(msg)

    def gen_ptr(self) -> int:
        """generates a new pointer

        Returns:
            int: pointer
        """
        addr = self.memory['ptr']['curr_addr']
        self.memory['ptr']['curr_addr'] += 1
        return addr
    

    def reset_local_and_temp(self) -> None:
        """resets local and temporal addresses 
        back to their original starting address
        """
        for datatype in self.memory['temp']['curr_addr']:
            temp_init = self.memory['temp']['init_addr'][datatype]
            local_init = self.memory['local']['init_addr'][datatype]
            self.memory['temp']['curr_addr'][datatype] = temp_init
            self.memory['local']['curr_addr'][datatype] = local_init

 
    def get_curr_quadruple(self) -> int:
        """increments quadruples and returns value

        Returns:
            int: quadruple id
        """
        self.curr_quadruple += 1
        return self.curr_quadruple


    def set_curr_proc(self, proc_name: str, proc_datatype:str = 'void') -> None:
        """changes the current procedure and adds it to the procedure directory

        Args:
            proc_name (str): name of the procedure 
            proc_datatype (str, optional): the datatype of the procedure 
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
        """returns the datatype of a given procedure

        Args:
            proc_name (str): name of procedure

        Returns:
            str: procedure datatype
        """
        datatype = self.procedures[proc_name].get('datatype')
        return datatype

    def get_func_return_addr(self, func_name:str ='') -> int:
        """retursn the global address of a function for handling function returns

        Args:
            func_name (str, optional): name of the function. Defaults to ''.

        Raises:
            TypeError: void function has a return

        Returns:
            int: fucntion return global address
        """
        if func_name == '':
            func_name = self.curr_proc
        else:
            proc = self.procedures.get(func_name)
            var = proc['var_table'].get(func_name)
            if var != None:
                return var['address']
        proc = self.procedures.get(func_name)
        proc_datatype = proc['datatype']

        if proc_datatype == 'void':
            #return None
            raise TypeError('void functions should not return a value')
        func = self.func_call
        if func == '':
            func = self.curr_proc

        res = self.procedures[func]['var_table'][func]['address']
        return res
        

    def print_procedure_directory(self) -> None:
        """Prints the procedure directory in console
        """
        header = ['name', 'datatype','quad start','#param','local+param','#temps','li','lf','lb','lc','ls','ti','tf','tb','tc','ts']
        data = []
        
        for proc in self.procedures:
            global_var = 0
            datatype = self.procedures[proc]['datatype']
            if datatype != 'void':
                global_var = 1
            quad_start = self.procedures[proc]['quad_start']
            params = len(self.procedures[proc]['param_vector'])
            variables = len(self.procedures[proc]['var_table']) - global_var
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

            res = [proc, datatype, quad_start, params, variables, temps]
            res += [li, lf, lb, lc, ls, ti, tf, tb, tc, ts]
            data.append(res)
        print('\n',' '*16,'PROCEDURE DIRECTORY')
        print(tabulate(data, headers=header, tablefmt='fancy_grid'),'\n')

    def print_var_tables(self) -> None:
        """Prints the varaible table in the console
        """
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
        print(' '*15,'VARIABLE TABLE')
        print(tabulate(data, headers=header, tablefmt='fancy_grid'),'\n')

    def get_dim(self, var_name:str) -> int:
        dim = self.procedures[self.curr_proc]['var_table'][var_name].get('dim')
        if dim != None:
            return dim

   
    def add_variable(self, var_name:str, datatype:str = '', addr:int = -1, scope:str = 'local', dim:int = None):
        """adds a variable to the variable table of a function

        Args:
            var_name (str): name of the
            datatype (str, optional): datatype of the varaible. Defaults to ''.
            addr (int, optional): address of the variable. Defaults to -1.
            scope (str, optional): scope of the variable. Defaults to 'local'.
            dim (int, optional): dimension of array. Defaults to None.

        Raises:
            ValueError: a global variable with that same name exists
            ValueError: another variable already has that name
        """
        if datatype == '':
            datatype = self.curr_datatype
        if self.procedures['program']['var_table'].get(var_name) != None:
            raise ValueError('A global variable with that name already exists')
        if self.procedures[self.curr_proc]['var_table'].get(var_name) != None:
            msg = f'Repeated variable name:{var_name} in {self.curr_proc}'
            raise ValueError(msg)
        [scope] = ['global' if self.curr_proc == 'program' else scope]
        if addr == -1:
            if dim == None:
                dim = 0
            self.add_const(dim, datatype='int')
            addr = self.memory[scope]['curr_addr'][datatype]
            self.memory[scope]['curr_addr'][datatype] += 1 + dim
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
        """adds a constant varaible, and returns its address in case a 
        constant already existed its not added and its address is returned

        Args:
            var_name (str): variable name
            datatype (str): datatype

        Returns:
            int: address
        """
        if datatype == 'string' or datatype == 'char':
            var_name = var_name[1:-1]
        if self.const_table[datatype].get(var_name) == None:
            addr = self.memory['const']['curr_addr'][datatype]
            self.memory['const']['curr_addr'][datatype] += 1
            self.const_table[datatype].update({var_name:addr})
            return int(addr)
        else:
            return self.const_table[datatype].get(var_name)


    def add_procedure(self, proc_name:str, proc_datatype:str) -> None:
        """This function adds a new procedure to the procedure directory

        Args:
            proc_name (str): procedure name
            proc_datatype (str): procedure datatype

        Raises:
            ValueError: duplicate procedure
        """
        if self.procedures.get(proc_name) != None:
            msg = f'A procedure with the name "{proc_name}" already exists'
            raise ValueError(msg)
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
            'quad_start':None,
            'param_vector':[],
            'var_table':{},
            'temps':0
        }
        if proc_datatype != 'void':
            addr = self.memory['global']['curr_addr'][proc_datatype]
            self.memory['global']['curr_addr'][proc_datatype] += 1
            self.add_variable(proc_name, proc_datatype, addr,'global' )
            

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

    def get_param_len(self, func_name:str) -> int:
        """returns the lenght of the parameter vector of a function

        Args:
            func_name (str): name of a function/module

        Returns:
            int: the number of parameters of a given function
        """
        return len(self.procedures[func_name]['param_vector'])
    

    def add_param(self, param_name:str, datatype:str) -> None:
        """ Adds a parameter to the parameter vector of a function
        and to its variable table

        Args:
            param_name (str): name of the parameter to be added
            datatype (str): datatype of the parameter to be added
        """
        self.procedures[self.curr_proc]['param_vector'].append(datatype)
        self.add_variable(param_name, datatype)


    def set_quad_start(self, quad_start:int) -> None:
        """Sets the start of a function to a given integer

        Args:
            quad_start (int): the quadruple number where the function starts
        """
        self.procedures[self.curr_proc]['quad_start'] = quad_start


    def get_addr_datatype(self, addr:int) -> str:
        """returns the datatype for a given address

        Args:
            addr (int): address number

        Returns:
            str: datatype
        """
        try:
            base = addr - addr%1000
            if base in [1000,6000,11000,16000,21000]:
                return 'int'
            elif base in [2000,7000,12000,17000]:
                return 'float'
            elif base in [3000,8000,13000,18000]:
                return 'bool'
            elif base in [4000,9000,14000,19000]:
                return 'char'
            elif base in [5000,10000,15000,20000]:
                return 'string'
            else:
                'ptr'
        except:
            raise MemoryError('Address has no datatype')

    def get_var_addr(self, var_name:str) -> int:
        """retuns the address of a given variable

        Args:
            var_name (str): name of the variable

        Raises:
            NameError: non existant variable

        Returns:
            int: address
        """
        proc = self.curr_proc
        try:
            val = self.procedures['program']['var_table'].get(var_name)
            if  val != None:
                return val['address']
            val = self.procedures[proc]['var_table'].get(var_name)
            if  val != None:
                return val['address']

        except:
            msg = f'A variable with the name "{var_name}" doesn`t exist'
            raise NameError(msg)

    def get_var_dim(self, var_name:str) -> int:
        """returns dimension of an array

        Args:
            var_name (str): variable/array name

        Raises:
            MemoryError: No dimensions found for the array

        Returns:
            int: array dimension
        """
        try:
            res = self.procedures['program']['var_table'].get(var_name)
            if res != None:
                return res['dim']
            res = self.procedures[self.curr_proc]['var_table'].get(var_name)
            if res != None:
                return res['dim']
        except:
            msg = f'No dimension was found for the array with name: "{var_name}"'
            raise MemoryError(msg)

if __name__ == '__main__':
    pass