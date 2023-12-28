#Extract data at pointer to a python structure
#@author Me
#@category Export
#@keybinding 
#@menupath 
#@toolbar 

import json

try:
    from ghidra.ghidra_builtins import *
except:
    pass

def collect_all_functions():
    fm = currentProgram.getFunctionManager()
    res = []
    for fn in fm.getFunctions(True):
        fn_body = fn.body
        res.append({
            "name": fn.name,
            "offset": fn.symbol.address.offset,
            "conv": fn.callingConventionName,
            "size": fn_body.maxAddress.subtract(fn_body.minAddress),
        })
    return res


def collect_all_data():
    data = getFirstData()
    res = []
    while data:
        if data.label:
            res.append({"label": data.label, "offset": data.address.offset})
        data = getDataAfter(data)
    return res

functions = collect_all_functions()
datas = collect_all_data()

export_data = {
    "functions": functions,
    "datas": datas,
}

path = askFile("Where to store data", "OK")
with open(str(path), "w") as f:
    f.write(json.dumps(export_data))
