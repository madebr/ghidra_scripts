# Change all function pointers in range to __thiscall

#@category Selection

import ghidra
import re
try:
    from ghidra.ghidra_builtins import *
except ImportError:
    pass


import json
all_data = json.load(open("/tmp/mfc42d.json", "r"))
mfc_funcs = all_data["funcs"]
mfc_values = all_data["values"]


def str_to_datatype(s):
    if not s:
      return getDataTypes("void")[0]
    p_i = 0
    print(s)
    while s[-1 - p_i] == "*":
      p_i += 1
    if p_i == 0:
      return getDataTypes(s)[0]
    else:
      t = getDataTypes(s[:-p_i])[0]
      for _ in range(p_i):
        t = ghidra.program.model.data.PointerDataType(t)
      return t



# sel = currentSelection

# current = sel.minAddress
MATCHER = re.compile(u"([0-9]+)+[ \t]+Ordinal_([0-9]+).*")

current = toAddr(0x00640338)
finish = toAddr(0x00640e27)

while current < finish:
  print("current", current)
  comment = getPreCommentAsRendered(current)
  m = MATCHER.match(comment)
  assert m
  assert m.group(1) == m.group(2)
  str_ordinal = m.group(1)
  ordinal = int(str_ordinal)
  print(current, ordinal, comment)
  if str_ordinal in mfc_funcs:
    func_info = mfc_funcs[str_ordinal]
    print("->", func_info)
    func_full_name = func_info["name"]
    if "::" in func_full_name:
      kls, name = func_full_name.rsplit("::", 1)
    else:
      kls, name = None, func_full_name
    symbol_current = getSymbolAt(current)
    if symbol_current:
      assert symbol_current.referenceCount == 1
      r = symbol_current.references[0]
      print("->", r)
      s = getSymbolAt(r.fromAddress)
      assert r.fromAddress == s.address
      f = createFunction(r.fromAddress, name)
      f.setCallingConvention(func_info["callconv"])
      f.setCustomVariableStorage(False)
      if kls:
        f.setParentNamespace(createNamespace(None, kls))
      f.setName(name, ghidra.program.model.symbol.SourceType.ANALYSIS)
      ret_t = str_to_datatype(func_info["ret"])
      f.setReturnType(ret_t, ghidra.program.model.symbol.SourceType.ANALYSIS)
      f.setVarArgs(func_info["vararg"])
      params = []
      for a_i, a in enumerate(func_info["args"]):
        t = str_to_datatype(a)
        print(" -> final datatype=", t)
        p = ghidra.program.model.listing.ParameterImpl("param_%d"%a_i, t, currentProgram, ghidra.program.model.symbol.SourceType.ANALYSIS)
        params.append(p)
      if func_info["callconv"] == "__thiscall":
        t = str_to_datatype(kls+"*")
        p_t = ghidra.program.model.listing.ParameterImpl("this", t, currentProgram, ghidra.program.model.symbol.SourceType.ANALYSIS)
        params.insert(0, p_t)

      f.replaceParameters(ghidra.program.model.listing.Function.FunctionUpdateType.DYNAMIC_STORAGE_ALL_PARAMS,
                          True,
                          ghidra.program.model.symbol.SourceType.ANALYSIS,
                          params)
      # s.setName("CCmdTarget::IsInvokeAllowed", ghidra.program.model.symbol.SourceType.ANALYSIS)
  elif str_ordinal in mfc_values:
    print("->", mfc_values[str_ordinal])
  else:
    print("->", "UNKNOWN")

  current = current.add(4)

