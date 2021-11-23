import json 

class OBJ:
    def print_quadruples(self, quadruples) -> None:
        for index, quad in enumerate(quadruples):
            (a, b, c, d) = quad
            [a] = ['_' if a == None else a]
            [b] = ['_' if b == None else b]
            [c] = ['_' if c == None else c]
            [d] = ['_' if d == None else d]
            print('{0}:\t({1},{2},{3},{4})'.format(index, a, b, c, d))

    
    def quad_to_json(self, quadruples, procedure_dir, constant_table):
        obj = {'proc_dir': {}, 'quads': {}, 'const_table': {}}
        for index, quad in enumerate(quadruples):
            (a, b, c, d) = quad
            obj['quads'][index] = {'oper': a, 'left': b, 'right': c, 'res': d}
        obj['proc_dir'] = procedure_dir
        obj['const_table'] = constant_table
        return json.dumps(obj, indent=4)


    def gen_obj_code(self, quadruples, procedure_dir, constant_table) -> None:
        json_object = self.quad_to_json(quadruples, procedure_dir, constant_table)
        with open('code.json', 'w') as outfile:
            outfile.write(json_object)
