'''
#############################
#   Gerardo Galan Garzafox  #
#   A00821196               #
#                           #
#   procedure_dir.py        #
#   Created_at 2021-09-28   #
#   Updated_at 2021-10-09   #
#############################
''' 

from tabulate import tabulate

"""
    PROCEDURE DIRECTORY
    -------------------
    name      -> name of the procedure
    datatype  -> datatype of the procedure 
    size      -> memory size of the procedure
    params    -> a vector of the datatypes expected by the params
    var_table -> a table of all the variables in the procedure.

    VARIABLE TABLE
    --------------

"""
class procedure_dir():
    def __init__(self):
        self.curr_proc = ""
        self.curr_quadruple = 0
        self.curr_temp = 0
        self.curr_datatype = ""
        self.procedures = {}
        self.variable_stack = []
        self.curr_arg_k = 0

    def get_curr_temp(self) -> int:
        self.curr_temp += 1
        self.procedures[self.curr_proc]["temps"] += 1
        return self.curr_temp

    def reset_curr_temp(self) -> None:
        self.curr_temp = 0
        
    def get_curr_quadruple(self) -> int:
        self.curr_quadruple += 1
        return self.curr_quadruple

    def set_curr_proc(self, proc_name: str, proc_datatype:str = "void") -> None:
        self.curr_proc = proc_name
        self.add_procedure(proc_name,proc_datatype)

    def print_procedure_directory(self) -> None:
        header = ["name", "datatype", "size","quad range","#params","#vars","#temps"]
        data = []
        
        for proc in self.procedures:
            datatype = self.procedures[proc]["datatype"]
            size = self.procedures[proc]["size"]
            quad_range = self.procedures[proc]["quad_range"]
            params = len(self.procedures[proc]["param_vector"])
            variables = len(self.procedures[proc]["var_table"])
            temps = self.procedures[proc]["temps"]
            res = [proc, datatype, size, quad_range, params, variables, temps]
            data.append(res)
        print("\n"," "*16,"PROCEDURE DIRECTORY")
        print(tabulate(data, headers=header, tablefmt="fancy_grid"),"\n")

    def print_var_tables(self) -> None:
        header = ['name', 'datatype', 'scope','belongs to','address']
        data = []
        procs = self.procedures
        for proc_name in procs:
            for var_name in procs[proc_name]['var_table']:
                datatype = procs[proc_name]['var_table'][var_name]['datatype']
                scope = procs[proc_name]['var_table'][var_name]['scope']
                address = procs[proc_name]["var_table"][var_name]['address']
                data.append([var_name, datatype, scope, proc_name, address])
        print(' '*15,'VARIABLE TABLE')
        print(tabulate(data, headers=header, tablefmt='fancy_grid'),'\n')

    """
    This function is used to collect varibales(name, datatype, scope) in a
    stack that gets emptied when a new procedure is added to the object

    """    
    def add_variable(self, var_name:str, datatype:str = "", address:int = -1):
        if datatype == "":
            datatype = self.curr_datatype
        if self.exist_global_var(var_name):
            return "Error a global variable with that name alredy exists"
        [scope] = ["global" if self.curr_proc == "program" else "local"]
        data = {
            "datatype":datatype, 
            "scope": scope,
            "address": address
        }
        self.procedures[self.curr_proc]["var_table"][var_name] = data

    """
    This function adds a new procedure to the procedure directory
    """
    def add_procedure(self, proc_name:str, proc_datatype:str):
        # Test for existing procedures
        if self.exist_proc(proc_name):
            return "Error that procedure with that name already exists"
        self.procedures[proc_name] = {
            "datatype":proc_datatype,
            "size":0,
            "quad_range":(None,None),
            "param_vector":[],
            "var_table":{},
            "temps":0
        }       
    
    def reset_curr_arg_k(self):
        self.curr_arg_k = 0

    def get_curr_arg_k(self):
        self.curr_arg_k += 1
        return self.curr_arg_k


    def get_param_num(self, func_name):
        return len(self.procedures[func_name]["param_vector"])
    """
    Adds a param datatype to the current procedure
    """
    def add_param(self, param_name:str, datatype:str) -> None:
        self.procedures[self.curr_proc]["param_vector"].append(datatype)
        self.add_variable(param_name, datatype)


    """
    Sets the start of a quadruple to a given integer
    """
    def set_quad_start(self, quad_start:int) -> None:
        self.procedures[self.curr_proc]["quad_range"] = (quad_start,None)

    """
    Sets the start of a quadruple to a given integer
    """
    def set_quad_end(self, quad_end:int) -> None:
        (start,_) = self.procedures[self.curr_proc]["quad_range"] 
        self.procedures[self.curr_proc]["quad_range"] = (start, quad_end)

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

    def get_var_type(self, proc_name:str, var_name:str) -> str:
        try:
            procs = self.procedures
            dt = procs[proc_name]["var_table"][var_name]["datatype"]
            return dt    
        except:
            return "ERROR"

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