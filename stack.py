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
        """retursn the top element of a given list

        Args:
            stack (list): a general stack

        Returns:
            item: top item in given stack
        """
        if len(stack) > 0:
            return stack[len(stack) - 1]
        return 'Stack length is 0'


    def top_operator_priority(self) -> int:
        """returns the priority of the operator in top of the operator stack

        Returns:
            int: priority
        """
        return self.priority(self.top(self.operators))

    def priority(self, op:str) -> int:
        """reutns the priority of an operator

        Args:
            op (str): operator

        Returns:
            int: value of a given operator
        """
        val = 0
        if op in ['=', '+=', '-=', '*=', '/=']:
            val = 1
        if op in ['and', 'or', 'AND', 'OR']:
            val = 2
        elif op in ['>','<','>=','<=','==','!=', 'DIFFERENT','EQUIVALENT']:
            val = 3
        elif op in ['+','-']:
            val = 4
        elif op in ['*','/','%']:
            val = 5
        elif op in ['^']:
            val = 6
        elif op == '(':
            val = 7
        else:
            val = 0
        lvl = self.operators.count('(') + 1
        return val * lvl

    def top_isnt_lpar(self) -> bool:
        """
         return true if the top of the list of operators isn`t a right parenthesis
        """
        res = self.top(self.operators) != '('
        return res

    def get_RL_operands(self) -> (str,str):
        """pops the right and left operands out of the operand stack

        Returns:
            (int,int): returns a tuple of ints
        """
        right  = self.operands.pop()
        left   = self.operands.pop()
        return (right,left)

    def print_all_stacks(self) -> None:
        """prints all stacks
        """
        print('jumps',self.jumps)
        print('operators',self.operators)
        print('operands',self.operands)
        print('datatypes',self.datatypes)
        print()