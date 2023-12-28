# Change all function pointers in range to __thiscall

#@category C++

import ghidra
try:
    from ghidra.ghidra_builtins import *
except ImportError:
    pass


# def create_empty_signature(func):
#   assert func
#   si = func.signature
#   assert "undefined" not in func.returnType.name, "%s has an undefined return type" % si.name
#   for arg in si.arguments:
#     assert "undefined" not in arg.dataType.name, "%s has an undefined argument" % si.name
#     arg.name = ""
#   return si


def iterate_range(r):
  addr = r.minAddress
  dat = getDataAt(addr)
  while dat.address < r.maxAddress:
    assert dat.pointer
    funcAddr = dat.value
    func = getFunctionAt(funcAddr)
    if func:
        funcName = func.name
    else:
        funcName = "FUN_{}".format(dat.value)
        createFunction(funcAddr, "FUN_{}".format(dat.value))
        func = getFunctionAt(funcAddr)

    func.

    if func.callingConventionName == "__stdcall":
        # convert stdcall to __thiscall
        func.setCallingConvention("__thiscall")
    elif func.callingConventionName == "__fastcall":
        print("__fastcall detected... at {}".format(funcAddr))
        original_parameters = func.parameters
        print(original_parameters)
        func.removeParameter(0)
        func.setCallingConvention("__thiscall")
    elif func.callingConventionName == "__thiscall":
        pass # thiscall is okay!
    else:
        print("UNKNOWN convention at {}: {}".format(funcAddr, func.callingConventionName))
    dat = getDataAfter(dat)


iterate_range(currentSelection.firstRange)
