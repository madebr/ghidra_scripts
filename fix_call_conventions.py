#Fix function call conventions
#@author Me
#@category Fixes
#@keybinding 
#@menupath 
#@toolbar

try:
    from ghidra.ghidra_builtins import *
except:
    pass


def to_ubyte(b):
    if b < 0:
        return b + 256
    return b

def to_ubytes(bs):
    return [to_ubyte(b) for b in bs]


def is_probably_cdecl(fn):
    last_instruction = get_last_function_instruct(fn)
    return to_ubytes(last_instruction.bytes) == [0xc3]


def get_last_function_instruct(fn):
    instruction = None
    iterator = currentProgram.getListing().getCodeUnits(fn.body, True)
    while iterator.hasNext():
        instruction = iterator.next()
    return instruction

fm = currentProgram.getFunctionManager()
res = []
# fn = getFunctionAt(toAddr(0x004e0aa0))
# if True:
for fn in fm.getFunctions(True):
    if "FUN_" in fn.name:
        continue
    if is_probably_cdecl(fn) and fn.callingConventionName != "__cdecl":
        print "{} is probably __cdecl, but isn't tagged like that".format(fn.name)
        fn.setCallingConvention("__cdecl")
    # else:
    #     fn.setCallingConvention("__stdcall")

