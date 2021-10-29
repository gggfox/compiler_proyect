class VM():
    def __init__(self):
        self.quadruples = []
        self.memory = {
            'global': {
                'initial_address': {
                    'int': 1000,
                    'float': 2000,
                    'bool': 3000,
                    'char': 4000,
                    'string': 5000
                }, 
                'current_address': {
                    'int': 1000,
                    'float': 2000,
                    'bool': 3000,
                    'char': 4000,
                    'string': 5000
                }
            },
            'local': {
                'initial_address': {
                    'int': 6000,
                    'float': 7000,
                    'bool': 8000,
                    'char': 9000,
                    'string': 10000
                }, 
                'current_address': {
                    'int': 6000,
                    'float': 7000,
                    'bool': 8000,
                    'char': 9000,
                    'string': 10000
                }

            },
            'temporal': {
                'initial_address': {
                    'int': 11000,
                    'float': 12000,
                    'bool': 13000,
                    'char': 14000,
                    'string': 15000
                }, 
                'current_address': {
                    'int': 11000,
                    'float': 12000,
                    'bool': 13000,
                    'char': 14000,
                    'string': 15000
                }
            },
            'constant': {
                'initial_address': {
                    'int': 16000,
                    'float': 17000,
                    'bool': 18000,
                    'char': 19000,
                    'string': 20000
                }, 
                'current_address': {
                    'int': 16000,
                    'float': 17000,
                    'bool': 18000,
                    'char': 19000,
                    'string': 20000
                }

            }
        }

    def verify_segment(self, segment: str) -> None:
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

        return self.memory[segment]['initial_address'][datatype]

    def get_current_address(self, segment:str, datatype:str) -> int:
        self.verify_segment(segment)
        self.verify_datatype(datatype)
        
        address = self.memory[segment]['current_address'][datatype]
        self.memory[segment]['current_address'][datatype] += 1
        return address

    def set_current_address(self, segment:str, datatype:str, new_address:int) -> None:
        self.verify_segment(segment)
        self.verify_datatype(datatype)
        self.verify_range(segment, datatype, new_address)

        self.memory[segment]['current_address'][datatype] = new_address




if __name__ == '__main__':
    machine = VM()
    addr = machine.get_initial_address('global', 'int')
    print(addr)