
import json
from memory_architecture import memory


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
                    const = bool(const)

                self.const[addr] = const


    def add_global_var_to_ram(self,json_object):
        """adds global variables to memory

        Args:
            json_object: dictionary with procedure directory, quadruples and constant table
        """
        variables = json_object['proc_dir']['program'].get('var_table')
        for key,value in enumerate(variables):
            self.glob[variables[value]['address']] = None
      

    def input_type(self, addr: int):
        """handles the READ operation

        Args:
            addr (int): address

        Raises:
            ValueError: in case a string is in the char section

        Returns:
            [type]: the input value, its type depends on the address
        """
        base = addr - (addr % 1000)
        if base == 6000:
            res = int(input())
        elif base == 7000:
            res = float(input())
        elif base == 8000:
            res = bool(input())
        elif res == 9000:
            res = input()
            if len(res) > 1:
                raise ValueError('CHAR datatypes longer than expected')
        else:
            res = input()
        return res

    def is_glob(self,addr:int) -> bool:
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

    def is_const(self, addr:int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 16000 and addr < 21000:
            return True

    def is_pointer(self,addr:int) -> bool:
        if type(addr) != int:
            return False
        if addr >= 21000:
            return True

    def verify_array(self, left: int, right: int, res: int) -> None:
        if (left < right) or (left > res):
            print(left,right,res)
            raise ValueError('index of array is out of bounds')


    def save(self,addr,sol):
        if type(addr) != int or addr < 1000:
            return addr
        if self.is_glob(addr):
            self.glob[addr] = sol
        elif self.is_local(addr):
            self.local[self.era][addr] = sol
        elif self.is_temp(addr):
            self.temp[self.era][addr] = sol
        elif self.is_pointer(addr):
            self.pointer[addr] = sol
  

    def get_mem(self,addr):
        if addr == None or type(addr) != int:
            return addr
        elif self.is_glob(addr):
            return self.glob[addr]
        elif self.is_temp(addr):
            return self.temp[self.era][addr]
        elif self.is_local(addr):
            # expression in param
            #print(self.era,self.gosub)
            if self.era != len(self.gosub):
                return self.local[self.era - 1][addr]
            # default
            else:
                return self.local[self.era][addr]
        elif self.is_const(addr):
            return self.const[addr]
        elif self.is_pointer(addr):
            return self.pointer[addr]

    def run_quads(self, json_object):
        proc_dir = json_object['proc_dir']

        quad_length = len(json_object['quads'])
        ip = 0  # instruction pointer
        while ip < quad_length:
            quad = json_object['quads'][str(ip)]
            left = quad['left']
            right = quad['right']
            res = quad['res']
            oper = quad['oper']

            # Convert pointer to real address
            if self.is_pointer(res):
                res = self.get_mem(res)
            if self.is_pointer(left):
                left = self.get_mem(left)
            if self.is_pointer(right):
                right = self.get_mem(right)
       
            #self.get_mem(left)

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

            # ERA necesia borrar memoria
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
                
                self.save(addr,self.get_mem(left))
             
            elif oper == 'GOSUB':

                
                #print(self.era,self.gosub)
                if self.era == len(self.gosub)+1:
                    ip = proc_dir[left]['quad_range'][0]
                    self.gosub.append(res)
                    continue
                    
                
            elif oper == 'RET':
                func_datatype = proc_dir[self.curr_func]['datatype']
                if func_datatype == 'void':
                    raise TypeError('void functions dont return a value')

                lst = list(proc_dir[self.curr_func]['var_table'].items())
                addr = lst[0][1]['address']
                self.glob[addr] = self.get_mem(left)
                self.era -= 1
                del self.local[-1]
                del self.temp[-1]
                ip = self.gosub.pop()

            elif oper == 'ENDFUNC':
                ip = self.gosub.pop()
                del self.local[-1]
                del self.temp[-1]
                self.era -= 1
                continue
            elif oper == '==':
                solution = self.get_mem(left) == self.get_mem(right)
                self.save(res,solution)
            elif oper == '!=':
                solution = self.get_mem(left) != self.get_mem(right)
                self.save(res,solution)
            elif oper == '>=':
                solution = self.get_mem(left) >= self.get_mem(right)
                self.save(res,solution)
            elif oper == '<=':
                solution = self.get_mem(left) <= self.get_mem(right)
                self.save(res,solution)
            elif oper == '>':
                solution = self.get_mem(left) > self.get_mem(right)
                self.save(res,solution)
            elif oper == '<':
                solution = self.get_mem(left) < self.get_mem(right)
                self.save(res,solution)
            elif oper == 'and':
                solution = self.get_mem(left) and self.get_mem(right)
                self.save(res,solution)
            elif oper == 'or':
                solution = self.get_mem(left) or self.get_mem(right)
                self.save(res,solution)
            elif oper == '*':
                solution = self.get_mem(left) * self.get_mem(right)
                self.save(res,solution)
            elif oper == '/':
                solution = self.get_mem(left) / self.get_mem(right)
                self.save(res,solution)
            elif oper == '+':
                solution = self.get_mem(left) + self.get_mem(right)
                self.save(res,solution)
            elif oper == '-':
                solution = self.get_mem(left) - self.get_mem(right)
                self.save(res,solution)
            elif oper == '=':
                solution = self.get_mem(left)
                self.save(res,solution)
               
               
            ip += 1

    def execute(self, file_name: str = 'code.json'):
        with open(file_name, 'r') as openfile:
            json_object = json.load(openfile)


        self.add_const_var_to_ram(json_object)
        self.add_global_var_to_ram(json_object)
        self.run_quads(json_object)
      
        print()
        print(self.glob)
        print(self.local)
        print(self.temp)
        print(self.const)




if __name__ == '__main__':
    vm = VM()
    vm.execute()
