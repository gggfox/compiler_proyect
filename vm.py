import json
import statistics
import matplotlib.pyplot as plt
from scipy import stats


class VM:
    def __init__(self):
        self.gosub = []
        self.curr_func = None
        self.era = 0
        # RAM
        self.glob = {}
        self.local = [{}]
        self.temp = [{}]
        self.const = {}
        self.pointer = {}


    def add_const_var_to_ram(self, json_object):
        """adds consts to the constant dictionary

        Args:
            json_object: procedure directory, quadruples and constant table
        """
        for datatype in json_object['const_table']:
            for const, addr in json_object['const_table'][datatype].items():
                if datatype == 'int':
                    const = int(const)
                elif datatype == 'float':
                    const = float(const)
                elif datatype == 'bool':
                    if const in ['false','False']:
                        const = False
                    const = bool(const)

                self.const[addr] = const
       

    def add_global_var_to_ram(self, json_object):
        """adds global variables to memory with None value
        this is so it can be assigned a value later though the save function

        Args:
            json_object: dictionary with procedure directory, quadruples and constant table
        """
        global_variables = json_object['proc_dir']['program'].get('var_table')
        for key, value in enumerate(global_variables):
            self.glob[global_variables[value]['address']] = None
            

    def input_type(self, addr: int):
        """handles the READ operation

        Args:
            addr (int): address

        Raises:
            ValueError: in case a string is in the char section

        Returns:
            [type]: the input value, its type depends on the address
        """
        try:
            base = addr - (addr % 1000)
            value = input('>')
            if base == 6000:
                value = int(value)
            elif base == 7000:
                value = float(value)
            elif base == 8000:
                value = bool(value)
            elif value == 9000:
                value = str(value)
                if len(value) > 1:
                    raise ValueError('CHAR datatypes can`t be longer than 1 character')
            else:
                value = str(value)
            return value
        except:
            datatype = self.get_addr_type(addr=addr)
            msg = "Can't assign {0} to datatype {1}".format(value,datatype)
            raise TypeError(msg)

    def get_addr_type(self, addr:int) -> str:
        """returns datatype of a given address

        Args:
            addr (int): address

        Returns:
            str: datatype
        """
        base = addr - (addr % 1000)
        if base in [1000,6000,11000,16000]:
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
            return 'ptr'

    def is_glob(self, addr: int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 1000 and addr < 6000:
            return True

    def is_local(self, addr: int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 6000 and addr < 11000:
            return True

    def is_temp(self, addr: int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 11000 and addr < 16000:
            return True

    def is_const(self, addr: int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 16000 and addr < 21000:
            return True

    def is_pointer(self, addr: int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 21000:
            return True

    def verify_array(self, left: int, right: int, res: int) -> None:
        """verifies that the index is inside the array range 

        Args:
            left (int): index
            right (int): lower bound
            res (int): upper bound

        Raises:
            ValueError: in case index of the array is out of bounds
        """
        if (left < right) or (left > res):
            msg = 'index "{0}" of array is out of bounds'.format(left)
            raise ValueError(msg)

    def check_datatype(self, datatype:str ,value) -> None:
        """verifies that datatypes int, float and bool 
        aren't reciving chars or strings

        Args:
            datatype (str): datatype
            value ([type]): value that should be of the given datatype

        Raises:
            TypeError: If a string/char is assiged to a bool/int/float
        """
        dt = type(value)
        if datatype in ['int','float','bool'] and dt == str:
            msg = "char and string values can't be assigned to {0}".format(datatype)
            raise TypeError(msg)

    def is_None(self,oper, left,right):
        lvalue = self.get_mem(left)
        rvalue = self.get_mem(right)
        if lvalue == None or rvalue == None:
            print(oper,lvalue,rvalue)
            raise ValueError("A variable is missing a value")
                    
    def clean_datatype(self, addr:int, value):
        
        if addr >= 21000 or value == None:
            return value
        datatype = self.get_addr_type(addr)
        self.check_datatype(datatype, value)
        try:
            if datatype == 'int' and type(value) in [int,float,bool]:
                value = int(value)
                datatype = int
            elif datatype == 'float':
                value = float(value)
                datatype = float
            elif datatype == 'bool':
                value = bool(value)
                datatype = bool
            elif datatype == 'char':
                value = str(value)
                if len(value) > 1:
                    value = value[0]
                datatype = str
            elif datatype == 'string':
                value = str(value)
                datatype = str
            else:
                msg = f"Could not assign {value} to datatype {datatype}"
                raise TypeError("cant be assigned")
            if type(value) != datatype:
                msg = f"Value '{0}' isn't of type {1}".format(value,str(datatype))
                raise TypeError(msg)
            return value
        except:
            msg = "value '{0}' can't be assigned to a {1}".format(value,datatype)
            ValueError(msg)
    
    def save(self, addr: int, value) -> None:
        """saves a value in a memory address

        Args:
            addr (int): memory address
            sol ([type]): value
        """
        if type(addr) != int or addr < 1000:
            return addr

        value = self.clean_datatype(addr,value)
      
        if self.is_glob(addr):
            self.glob[addr] = value
        elif self.is_local(addr):
            self.local[self.era][addr] = value
        elif self.is_temp(addr):
            self.temp[self.era][addr] = value
        elif self.is_pointer(addr):
            self.pointer[addr] = value

    def get_mem(self, addr: int):
        """returns the value of a memory address

        Args:
            addr (int): memory address

        Returns:
            [type]: value 
        """
        if addr == None or type(addr) != int:
            return addr
        elif self.is_glob(addr):
            return self.glob.get(addr)
        elif self.is_temp(addr):
            return self.temp[self.era].get(addr)
        elif self.is_local(addr):
            # expression is param
            if self.era != len(self.gosub):
                return self.local[self.era - 1].get(addr)
            # default
            else:
                return self.local[self.era].get(addr)
        elif self.is_const(addr):
            return self.const.get(addr)
        elif self.is_pointer(addr):
            return self.pointer.get(addr)

    def get_array(self, baseAddr: int, size: int) -> [int]:
        """gets an address and dimesnion of array and generates a
        python list from it

        Args:
            baseAddr (int): base address of the array
            size (int): size/dim of the array

        Returns:
            [int]: returns an array of numbers  
        """
        arr = []
        i = 0
        while(i < size):
            if self.get_mem(baseAddr+i):
                arr.append(self.get_mem(baseAddr+i))
            i += 1
        return arr

    def run_quads(self, json_object) -> None:
        """Execures the quadruples

        Args:
            json_object ([type]): sructure containing the 
            procedure directroy, quadruples and constant table

        Raises:
            TypeError: [description]
            TypeError: [description]
        """
        
        proc_dir = json_object['proc_dir']

        quad_length = len(json_object['quads'])
        ip = 0  # instruction pointer
        while ip < quad_length:
            quad = json_object['quads'][str(ip)]
            left = quad['left']
            right = quad['right']
            res = quad['res']
            oper = quad['oper']

            #print(oper, left, right, res)
            # Convert pointer to real address
            if self.is_pointer(res):
                res = self.get_mem(res)
            if self.is_pointer(left):
                left = self.get_mem(left)
            if self.is_pointer(right):
                right = self.get_mem(right)

            #print(oper, left, right, res)
            #print(self.pointer)
            # print(self.get_mem(left))
            #print(self.glob)
            #print(self.local)
            if oper == 'GOTO':
                ip = int(res)
                continue
            elif oper == 'GOTOF':
                if self.get_mem(left) == False:
                    ip = int(res)
                    continue
            elif oper == 'WRITE':
                disp = self.get_mem(res)
                if disp == '\\n':
                    print()
                elif disp == '\\t':
                    print(end='\t')
                else:
                    print(disp,end='')
            
            elif oper == 'READ':
                addr = quad['res']
                solution = self.input_type(addr)
                self.save(res, solution)
            elif oper == 'VER':
                self.verify_array(
                    self.get_mem(left), self.get_mem(right), self.get_mem(res))
                ip += 1
                quad = json_object['quads'][str(ip)]
                left, right, res = quad['left'], quad['right'], quad['res']
                solution = self.get_mem(right) + left
                self.save(res, solution)

            elif oper == 'ERA':
                self.curr_func = res
                self.era += 1
                self.local.append({})
                self.temp.append({})

            elif oper == 'PARAM':
                func_datatype = proc_dir[self.curr_func]['datatype']
                [is_void] = [-1 if func_datatype == 'void' else 0]
                param_datatype = proc_dir[self.curr_func]['param_vector'][res-1]
                real_datatype = list(proc_dir[self.curr_func]['var_table'].items())[
                    res+is_void][1]['datatype']
                if param_datatype != real_datatype:
                    raise TypeError('function param datatype mismatch')

                addr = list(proc_dir[self.curr_func]['var_table'].items())[
                    res+is_void][1]['address']

                self.save(addr, self.get_mem(left))

            elif oper == 'GOSUB':
                if self.era == len(self.gosub)+1:
                    ip = proc_dir[left]['quad_start']
                    self.gosub.append(res)
                    continue

            elif oper == 'RET':
                func_datatype = proc_dir[self.curr_func]['datatype']
                if func_datatype == 'void':
                    raise TypeError('void functions dont return a value')

                self.glob[res] = self.get_mem(left)
                self.era -= 1
                del self.local[-1]
                del self.temp[-1]
                ip = self.gosub.pop()
                continue
            elif oper == 'ENDFUNC':
                ip = self.gosub.pop()
                del self.local[-1]
                del self.temp[-1]
                self.era -= 1
                continue
            elif oper == 'MAX':
                arr = self.get_array(baseAddr=left, size=right)
                solution = float(max(arr))
                self.save(res, solution)
            elif oper == 'MIN':
                arr = self.get_array(baseAddr=left, size=right)
                solution = float(min(arr))
                self.save(res, solution)
            elif oper == 'MEAN':
                arr = self.get_array(baseAddr=left, size=right)
                solution = round(statistics.mean(arr), 4)
                self.save(res, solution)
            elif oper == 'MEDIAN':
                arr = self.get_array(baseAddr=left, size=right)
                solution = float(statistics.median(arr))
                self.save(res, solution)
            elif oper == 'MODE':
                arr = self.get_array(baseAddr=left, size=right)
                solution = float(statistics.mode(arr))
                self.save(res, solution)
            elif oper == 'VARIANCE':
                arr = self.get_array(baseAddr=left, size=right)
                solution = float(round(statistics.variance(arr), 4))
                self.save(res, solution)
            elif oper == 'PLOTXY':
                arr1 = self.get_array(baseAddr=left, size=right)
                ip += 1
                quad = json_object['quads'][str(ip)]
                left, right, res = quad['left'], quad['right'], quad['res']
                arr2 = self.get_array(baseAddr=left, size=right)
                plt.scatter(arr1, arr2)
                plt.show()
            elif oper == 'REGRESSION':
                x = self.get_array(baseAddr=left, size=right)
                ip += 1
                quad = json_object['quads'][str(ip)]
                left, right, res  = quad['left'], quad['right'], quad['res']
                y = self.get_array(baseAddr=left, size=right)

                slope, intercept, _, _, _ = stats.linregress(x, y)

                def myfunc(x):
                    return slope * x + intercept

                mymodel = list(map(myfunc, x))

                plt.scatter(x, y)
                plt.plot(x, mymodel)
                plt.show()
                pass
            elif oper == '==':
                self.is_None(oper,left,right)
                solution = self.get_mem(left) == self.get_mem(right)
                self.save(res, solution)
            elif oper == '!=':
                self.is_None(oper,left,right)
                solution = self.get_mem(left) != self.get_mem(right)
                self.save(res, solution)
            elif oper == '>=':
                self.is_None(oper,left,right)
                solution = self.get_mem(left) >= self.get_mem(right)
                self.save(res, solution)
            elif oper == '<=':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) <= self.get_mem(right)
                self.save(res, solution)
            elif oper == '>':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) > self.get_mem(right)
                self.save(res, solution)
            elif oper == '<':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) < self.get_mem(right)
                self.save(res, solution)
            elif oper == 'and':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) and self.get_mem(right)
                self.save(res, solution)
            elif oper == 'or':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) or self.get_mem(right)
                self.save(res, solution)
            elif oper == '%':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) % self.get_mem(right)
                self.save(res, solution)
            elif oper == '^':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) ** self.get_mem(right)
                self.save(res, solution)
            elif oper == '*':                
                self.is_None(oper,left,right)
                solution = self.get_mem(left) * self.get_mem(right)
                self.save(res, solution)
            elif oper == '/':                
                self.is_None(oper,left,right)
                if self.get_mem(right) == 0:
                    raise ValueError("Can't divide by zero")
                solution = self.get_mem(left) / self.get_mem(right)
                self.save(res, solution)
            elif oper == '+':                
                self.is_None(oper,left,right)
                try:
                    solution = self.get_mem(left) + self.get_mem(right)
                    self.save(res, solution)
                except:
                    msg = f"Can't + {self.get_mem(left)} and {self.get_mem(right)}"
                    raise ValueError(msg)
            elif oper == '-':                
                self.is_None(oper,left,right)
                try:
                    solution = self.get_mem(left) - self.get_mem(right)
                    self.save(res, solution)
                except:
                    msg = f"Can't - {self.get_mem(left)} and {self.get_mem(right)}"
                    raise ValueError(msg)
            elif oper == '=':
                solution = self.get_mem(left)
                self.save(res, solution)
            elif oper == 'ENDPROG':
                print()

            ip += 1
    

    def execute(self, file_name: str = 'code.json'):
        with open(file_name, 'r') as openfile:
            json_object = json.load(openfile)

        self.add_const_var_to_ram(json_object)
        self.add_global_var_to_ram(json_object)
        self.run_quads(json_object)

        # print()
        # print(self.glob)
        # print(self.local)
        # print(self.temp)
        # print(self.const)


if __name__ == '__main__':
    vm = VM()
    vm.execute()
