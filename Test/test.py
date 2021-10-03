procedures = {
    "porgram":{
        "datatype":"void",
        "vars":{
            "i":{
                "datatype":"int",
                "scope":"global",
            },
            "j":{
                "datatype":"int",
                "scope":"global",
            }
        }
    },
    "main":{
        "datatype":"void",
        "vars":{
            "i":{
                "datatype":"int",
                "scope":"local",
            },
            "j":{
                "datatype":"int",
                "scope":"local",
            }
        }
    },
}
t = "int"
procedures["perro"] = {"datatype":t, "vars":{}}
print(procedures)