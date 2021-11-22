class Stack:

    def __init__(self):
        self.operands = []
        self.operators = []
        self.datatypes = []
        self.jumps = []


    def top(self, stack:list):
        """returns the top element of a given stack/list

        Args:
            stack (list): a general stack

        Returns:
            item: top item in given stack
        """
        if len(stack) > 0:
            return stack[len(stack) - 1]
        return 'Stack length is 0'


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