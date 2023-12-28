#Find references to some function
#@author Me
#@category Search
#@keybinding
#@menupath
#@toolbar

import struct

try:
    from ghidra.ghidra_builtins import *
except:
    pass


def askFunctionAddress(title, message):
    try:
        s = askString(title, message)
    except ghidra.util.exception.CancelledException:
        raise SystemExit(0)
    s = s.strip()
    address = None
    if address is None:
        try:
            address = toAddr(s)
        except ValueError:
            pass

    if address is None:
        func = getFunction(s)
        if func is not None:
            address = func.body.minAddress.getUnsignedOffset()

    if address is None:
        raise ValueError("Unknown address: {}".format(s))

    return address

def main():
    function_address = askFunctionAddress("Function name or address", "Enter function name or function address")
    print "addr", function_address, function_address.getUnsignedOffset()
    m = currentProgram.getMemory()
    for r in m.getAddressRanges():
        for s in range(r.minAddress.getUnsignedOffset(), r.maxAddress.getUnsignedOffset() - 3):
            try:
                bs = getBytes(toAddr(s), 4)
            except ghidra.program.model.mem.MemoryAccessException:
                break
            v, = struct.unpack("<l", bs)
            if v == function_address.subtract(toAddr(s + 4)):
                print "HIT at", toAddr(s)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
