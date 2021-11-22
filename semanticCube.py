Error:str = 'type mismatch'

SemanticCube = {
    '^':{
        'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '*':{
        'int':{
            'int':'int',
            'float':'float',
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':'string',
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':'string',
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
        '%':{
        'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '/':{
       'int':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '+':{
       'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
    },
    '-':{
        'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '*=':{
        'int':{
            'int':'int',
            'float':'float',
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':'string',
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':'string',
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '/=':{       
        'int':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '+=':{       
        'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': 'string',
            'bool': Error,
            'string': 'string',
        },
    },
    '-=':{
        'int':{
            'int':'int',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'float',
            'float':'float',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '<':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,          
        },
    },
    '>':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,          
        },
    },
    '<=':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,          
        },     
    },
    '>=':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,          
        },
    },
    '==':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'char':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'bool':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'string':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',              
        }
    },
    '!=':{
        'int':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'float':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'char':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'bool':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',  
        },
        'string':{
            'int':'bool',
            'float':'bool',
            'char': 'bool',
            'bool': 'bool',
            'string': 'bool',             
        }
    },
    '&&':{
        'int':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': 'bool',
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    '||':{
        'int':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': 'bool',
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    'and':{        
        'int':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': 'bool',
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
    'or':{
        'int':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'float':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'char':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
        'bool':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': 'bool',
            'string': Error,
        },
        'string':{
            'int':Error,
            'float':Error,
            'char': Error,
            'bool': Error,
            'string': Error,
        },
    },
}