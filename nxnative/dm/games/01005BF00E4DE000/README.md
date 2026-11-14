# Rabi-Ribi (01005BF00E4DE000)

CreSpirit's own 2D engine on NVN, SDK 7.4.0; update 1.2.0 (v131072). Modules main, subsdk0 (GLSLC, NVN's runtime shader compiler), subsdk1 (the movie library) and sdk.
Its shaders are compiled at run time with the game's own GLSLC (main keeps 5 GLSL sources and calls glslcCompile in subsdk0), so no game file holds them: the port took the
24 outputs the game saved on the device and split the tables from them. It plays on the Android port: boot, title, save select and gameplay at 60 fps.

## What it needs

| Setting | Where | Why |
|---|---|---|
| run-time GLSLC captures | this profile's tables; `--glslc-captures` | the game compiles its shaders at run time: a bootstrap port carries `DM_GLSLC_CAPTURE` in the data pack's `env.txt` and the app saves every compile to `files/glslc_capture`; `porter port --glslc-captures` takes that folder |
| `nv::GetGraphicsMemoryInfo` | `dm/host/hle_nvmem.c` | SDK 7's main calls the NVN internal helper, which reads the NVN driver's interface object; the host replaces the NVN API, so that object is null and the call faults right after the swap chain is created. The host has no separate video memory, so the 16-byte MemoryInfo comes back zeroed |
| descriptor pool lifetime | `dm/gfx/nvn/hle_nvn.c` | the game makes two or three texture and sampler pools a frame and finalizes them; a table that never forgot a pool fills, and later screens read other pools' IDs. A finalized pool, or one whose NVNmemoryPool goes, hands its slot and base range back for the next pool no larger; the table holds 1024 live pools, and no live pool is evicted |
| masked offset jump table | `dm/tools/patch_nso.py` | `main+0x446f0c` is an offset jump table whose bounds check masks the index and tests the mask (and, mvn, tst) instead of comparing it; `jump_mask_offsets` reads the mask and the table's mask+1 targets |

## Shaders

main holds 5 GLSL sources and subsdk0 is NVIDIA's GLSLC: the game compiles the programs it needs at run time, and no file in the RomFS holds a shader. The 24 outputs a
bootstrap port saved on the device were split with this repository's `shader_split.py` into the profile's tables and translated to SPIR-V (23 KB).

## On the device

On the AYN Thor (Snapdragon 8 Gen 2, Adreno 740, Android 13): frame time p50 16.66 ms and no dropped frames in the 300-frame windows, no red log line, the shared font set
to a Pan-CJK Noto Sans. The data pack is 0.7 GB (RomFS 0.67 GB, shaders.dmsv 23 KB).
