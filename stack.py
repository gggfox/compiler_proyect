class Stack:

    def __init__(self):
        self.operands = []
        self.operators = []
        self.datatypes = []
        self.jumps = []
        self.arr_dim = []

    '''
    returns the item on top of the stack, 
    aka the last operator to be added into the stack
    '''
    def top(self, stack:list):
        if len(stack) > 0:
            return stack[len(stack) - 1]
        return 'Stack length is 0'


    def top_operator_priority(self):
        return self.priority(self.top(self.operators))

    '''
    returns the priority of a given operator
    '''
    def priority(self, op:str) -> int:
        val = 0
        if op in ['and', 'or', '&&', '||', 'not', '!', 'AND', 'OR']:
            val = 1
        if op in ['>','<','>=','<=','==','!=', 'DIFFERENT']:
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
        lvl = self.operators.count('(') + 1
        return val * lvl


    def verify_priority(self, op:str) -> bool:
        """This is a function that returns true
        if the given operand has a lower priority
        than the operand on top of the operand stack

        Args:
            op (str): operand

        Returns:
            bool: returns true if op has a lower priority than the operand 
                on top of the operand stack 
        """
        #print(self.priority(op),'<=',self.priority(self.top(self.operators)))
        #print(op,'<=',self.top(self.operators))
        #self.print_all_stacks()
        return self.priority(op) <= self.priority(self.top(self.operators))


    def top_isnt_lpar(self) -> bool:
        """
         return true if the top of the list of operators isn`t a right parenthesis
        """
        res = self.top(self.operators) != '('
        return res

    def get_RL_operands(self) -> (str,str):
        right  = self.operands.pop()
        left   = self.operands.pop()
        return (right,left)

    def print_all_stacks(self) -> None:
        print('jumps',self.jumps)
        print('operators',self.operators)
        print('operands',self.operands)
        print('datatypes',self.datatypes)
        print()