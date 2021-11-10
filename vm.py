
import json
from memory_architecture import memory

class VM:
    def __init__(self):
        self.quadruples = []
        self.memory_arch = memory
        self.ram = [None] * 21000

    def verify_segment(self, segment: str) -> None:
        """verifies the segment is allowed

        Args:
            segment (str): name of the segment

        Raises:
            ValueError: if the segment is not equal to 
            either 'global', 'local', 'temporal' or 'constant'
        """
        if not segment in ['global','local','temporal','constant']:
            err = 'segment "{0}" doesn`t exist'.format(segment)
            raise ValueError(err)
        
    def verify_datatype(self, datatype: str) -> None:
        if not datatype in ['int','float','bool','char','string']:
            err = 'datatype "{0}" doesn`t exist'.format(datatype)
            raise ValueError(err)

    def verify_range(self, segment:str, datatype:str, address:int) -> None:
        initial = self.get_initial_address(segment,datatype)
        final = initial + 999
        if address < initial or address > final:
            err = 'address "{0}" is out of the range of [{1}][{2}]'.format(address,segment,datatype)
            raise ValueError(err)

    def get_initial_address(self, segment:str, datatype:str) -> int:
        self.verify_segment(segment)
        self.verify_datatype(datatype)

        return self.memory_arch[segment]['initial_addr'][datatype]

    def get_current_address(self, segment:str, datatype:str) -> int:
        self.verify_segment(segment)
        self.verify_datatype(datatype)
        
        address = self.memory_arch[segment]['current_addr'][datatype]
        self.memory_arch[segment]['current_addr'][datatype] += 1
        return address

    def set_current_address(self, segment:str, datatype:str, new_address:int) -> None:
        self.verify_segment(segment)
        self.verify_datatype(datatype)
        self.verify_range(segment, datatype, new_address)

        self.memory_arch[segment]['current_address'][datatype] = new_address

    def add_to_memory(self, address:int, value:str):
        self.memory_arch['real'][address] = value

    def verify_local(self,addr:int, datatype:str) -> None:
        
        lower = None
        upper = None
        err = ''
        if datatype == type(1):
            lower,upper = 6000,6999
            err = 'int'
        elif datatype == type(1.1):
            lower,upper = 7000,7999
            err = 'float'
        elif datatype == type(True):
            lower,upper = 8000,8999
            err = 'bool'
        elif datatype == type('char') and len(self.ram[addr]) == 1:
            lower,upper = 9000,9999
            err = 'char'
        elif datatype == type('str'):
            lower,upper = 10000,10999
            err = 'string'

        if lower > addr or addr > upper:
            msg = f'wrong type assignation to local {err} variable addr: {addr}'
            raise TypeError(msg)

    def print_ram(self) -> None:
        for i in range(len(self.ram)):
            if self.ram[i] != None:
                print(i, self.ram[i], type(self.ram[i]))    


    def add_const_var_to_ram(self, json_object):
        for datatype in json_object['const_table']:
            for const ,addr in json_object['const_table'][datatype].items():
                if datatype == 'int':
                    const = int(const)
                elif datatype == 'float':
                    cosnt = float(const)
                elif datatype == 'bool':
                    const = bool(const)

                self.ram[addr] = const

    def input_type(self,addr:int):
        base = addr - (addr%1000)
        if base == 6000:
            res = int(input())
        elif base == 7000:
            res = float(input())
        elif base == 8000:
            res = bool(input())
        elif res == 9000:#char
            res = input()
            if len(res) > 1:
                raise ValueError('CHAR datatypes longer than expected')
        else:
            res = input()
        return res

    def clean_datatype(self, addr, value):
        #print(addr,value)
        base = addr - (addr%1000)
        if base == 6000:
            return int(value)
        elif base == 7000:
            return float(value)
        else:
            return value

    def run_quads(self,json_object):
        #self.print_ram()
        quad_length = len(json_object['quads'])
        ip = 0 # instruction pointer

        while ip < quad_length:
            quad = json_object['quads'][str(ip)]
            left = quad['left']            
            right = quad['right']
            res = quad['res']
            if quad['oper'] == 'GOTO':
                ip = int(res)
                continue
            elif quad['oper'] == 'GOTOF':
                if self.ram[left] == False:
                    ip = int(res)
                    continue
            elif quad['oper'] == 'WRITE':
                if self.ram[res] == '\\n':
                    print()
                elif self.ram[res] == '\\t':
                    print(end='\t')
                else:
                    print(self.ram[res],end='')

            elif quad['oper'] == 'READ':
                addr = quad['res']
                self.ram[res] = self.input_type(addr)

            elif quad['oper'] == '==':
                self.ram[res] = self.ram[left] == self.ram[right]
            elif quad['oper'] == '!=':
                self.ram[res] = self.ram[left] != self.ram[right]
            elif quad['oper'] == '>=':
                self.ram[res] = self.ram[left] >= self.ram[right]
            elif quad['oper'] == '<=':
                self.ram[res] = self.ram[left] <= self.ram[right]
            elif quad['oper'] == '>':
                self.ram[res] = self.ram[left] > self.ram[right]
            elif quad['oper'] == '<':
                self.ram[res] = self.ram[left] < self.ram[right]
            elif quad['oper'] == 'and':
                self.ram[res] = self.ram[left] and self.ram[right]
            elif quad['oper'] == 'or':
                self.ram[res] = self.ram[left] or self.ram[right]
            elif quad['oper'] == '*':
                self.ram[res] = self.ram[left] * self.ram[right]
            elif quad['oper'] == '/':
                self.ram[res] = self.ram[left] / self.ram[right]  
            elif quad['oper'] == '+':
                self.ram[res] = self.ram[left] + self.ram[right]      
            elif quad['oper'] == '-':
                self.ram[res] = self.ram[left] - self.ram[right]  
            elif quad['oper'] == '=':
                self.ram[res] = self.clean_datatype(addr=res,value=self.ram[left])
                #self.verify_local(quad['res'], type(self.ram[left]))
            
            #print(ip, self.ram[quad['res']])
            ip += 1

    def execute(self, file_name:str ='code.json'):
        with open(file_name,'r') as openfile:
            json_object = json.load(openfile)

        # for i in json_object['quads']:
        #     print(json_object['quads'][i])

        self.add_const_var_to_ram(json_object)
        self.run_quads(json_object)
        self.print_ram()

if __name__ == '__main__':
    vm = VM()
    vm.execute()


