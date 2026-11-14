# GUNDAM BREAKER 4 (010093E01CEFE000): the rewriter's patches of this game's own builds. dm/tools/patch_nso.py loads every profile's patches.py and applies those of a module's NSO build ID;
# CUTS and OBS as described there ("Registered patches"). The engine-wide Unreal rules of the Mac rewriter (dm/tools/ue_malloc.py) do not exist in this Android tree yet, so the cut is registered here
CUTS = {
  # GUNDAM BREAKER 4 1.12.0 (v720896) main: Unreal Engine 4.27's FMallocBinned3 constructor (main+0x1ab1f48) reserves 37 GB of address space for its pools. The allocator is made on the first
  # allocation, during the static constructors: main+0x1a52c1c mov w0, #0x1c38; bl malloc(0x1abbefc); mov x19, x0; bl constructor (main+0x1a52c28). The constructor is cut at its entry (ret), and
  # observation gate OBS_UE_MALLOC right after the call puts the host allocator's vtable into the new object, still in x19 (dm/host/hle_uemalloc.c)
  'ba96dfdf82b7ac48ab945fef316c361c': [
    (0x1ab1f48, 'fd7bbaa9', 'c0035fd6', 'FMallocBinned3 constructor entry (called at main+0x1a52c28) -> ret: the 37 GB address space is not reserved; the host allocator vtable goes in at the gate after the call (hle_uemalloc.c)'),
  ],
}
OBS = {
  # right after the (now returning) constructor call, x19 = the new allocator object; the host writes its vtable there
  'ba96dfdf82b7ac48ab945fef316c361c': [
    (0x1a52c2c, 21, 'aa1303e0', 'GCreateMalloc: the allocator object is in x19, before it is used: the host puts its vtable in; orig mov x0, x19'),
  ],
}
