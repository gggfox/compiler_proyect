'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   procedure_dir.py        #
#   Created_at 2021-09-28   #
#   Updated_at 2021-10-02   #
#############################
''' 

from tabulate import tabulate

class procedure_dir():
    def __init__(self):
        self.curr_scope = "global"
        self.procedures = {}
        self.variable_stack = []

    def print_procedure_directory(self):
        header = ["name", "datatype", "# vars"]
        data = []
        for proc_name in self.procedures:
            datatype = self.procedures[proc_name]["datatype"]
            var_table_len = len(self.procedures[proc_name]["var_table"])
            data.append([proc_name, datatype, var_table_len])
        print()
        print("_"*8,"PROCEDURE DIRECTORY")
        print(tabulate(data, headers=header, tablefmt="fancy_grid"),"\n")

    def print_var_tables(self):
        header = ["name", "datatype", "scope","belongs to"]
        data = []
        procs = self.procedures
        for proc_name in procs:
            for var_name in procs[proc_name]["var_table"]:
                datatype = procs[proc_name]["var_table"][var_name]["datatype"]
                scope = procs[proc_name]["var_table"][var_name]["scope"]
                data.append([var_name,datatype,scope,proc_name])
        print("_"*15,"VARIABLE TABLE")
        print(tabulate(data, headers=header, tablefmt="fancy_grid"),"\n")
    """
    This function is used to collect varibales(name, datatype, scope) in a
    stack that gets emptied when a new procedure is added to the object

    """    
    def add_variable(self, var_name:str, var_datatype:str):
        if self.exist_global_var(var_name):
            return "Error a global variable with that name alredy exists"
        self.variable_stack.append((var_name, var_datatype, self.curr_scope))
    
    def add_procedure(self, proc_name:str, proc_datatype:str):
        # Test for existing procedures
        if self.exist_proc(proc_name):
            return "Error that procedure with that name already exists"
        self.procedures[proc_name] = {"datatype":proc_datatype,"var_table":{}}
        # add variables to procedure
        while len(self.variable_stack) > 0:
            (var_name, var_datatype, var_scope) = self.variable_stack.pop()
            if self.exist_local_var(proc_name, var_name):
                msg = "Error duplicate variable name '{0}' in procedure: '{1}'"
                print(msg.format(var_name,proc_name))
            else:
                data = {
                    "datatype":var_datatype,
                    "scope":var_scope   
                }
                self.procedures[proc_name]["var_table"][var_name] = data
    
    def exist_proc(self, proc_name):
        try:
            return self.procedures[proc_name]
        except:
            return False

    def exist_local_var(self, proc_name, var_name):
        try:
            if self.procedures[proc_name]["var_table"][var_name]:
                return True 
        except:
            return False

    def exist_global_var(self, var_name):
        try:
            if self.procedure["program"]["var_table"][var_name]:
                return True
        except:
            return False

    def search_var(self, proc_name:str, var_name:str):
        if not self.search_proc(proc_name):
            return "Error there is no procedure with that name"
        if self.exist_local_var(proc_name, var_name):
            return self.procedures[proc_name]["var_table"][var_name]
        elif self.exist_global_var(var_name):
            return self.procedures["program"]["var_table"][var_name]
        else:
            msg = "Error variable '{0}' isn't associated with procedure '{1}'"
            return msg.format(var_name,proc_name)

    def search_proc(self, proc_name:str):
        if self.exist_proc(proc_name):
            return self.procedures[proc_name]
        else:
            msg = "Error there is no procedure with the name:{0}"
            return msg.format(proc_name)


if __name__ == '__main__':
    pp = procedure_dir()
    pp.add_variable("i","int","global")
    pp.add_variable("j","int","global")
    pp.add_procedure("global","void")

    pp.add_variable("i","int","local")
    pp.add_variable("j","int","local")
    pp.add_variable("j","int","local")
    pp.add_procedure("calc()","int")
    print(pp.search_var("calc()","i"))
    print(pp.search_proc("calc()"))