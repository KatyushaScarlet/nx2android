# Magical Girl Witch Trials (01006C5027060000)

Unity 6000.0.72f1 IL2CPP with FMOD on NVN, SDK 21.4.7; update 2.0.1b (v65536), the Chinese Traditional release. Modules main, subsdk0 (NintendoSDK_movie) and sdk.
Nearly everything is in 644 Addressables bundles under `Data/StreamingAssets/aa/Switch` (2.62 GB of the 2.65 GB RomFS): their UnityFS type trees name the engine version, so
`unityfs.py` reads Unity 6's Shader objects and `shader_split.py` split 2,421 shaders from them; `shader_vk.py` translated 2,425 to SPIR-V (9.2 MB bundle). It plays on the Android
port: boot, the title and gameplay at 60 fps.

## What it needs

| Setting | Where | Why |
|---|---|---|
| `mem_reserve 0x140000000`, `mem_alias 0x118000000`, `sys_resource 0x1000000` | [`game.tsv`](game.tsv) | the NPDM declares 16 MB of system resource and main never sets a heap: Unity 6's `nninitStartup` reserves address regions itself and maps its memory, so the game gets a 5 GB block with a 4.375 GB alias region |
| Pan-CJK shared font | the data pack's `standard.ttf` (`--shared-font`) | the game's system text uses the Switch shared font; the Android default (Roboto) has no CJK glyphs, so the port carries Noto Sans CJK (Simplified/Traditional Chinese, Japanese and Korean) |
| `pad_layout full` | [`game.tsv`](game.tsv) | a visual novel played with a controller; touch input is not tested yet |

No game-specific host or rewriter change was needed: the profile's constants are the survey's (`survey.md`), and the stock host runs SDK 21's NVN and services.

## Shaders

The 644 Addressables bundles are the only place that holds shader code: each `Shader` object carries its GLSL control section and code areas, and `unityfs.py` reads them through
the bundle's type tree (Unity 6, as Hollow Knight: Silksong's 6000.0 build). The split found 2,421 shaders; 2,425 programs were translated to SPIR-V.

## On the device

On the AYN Thor (Snapdragon 8 Gen 2, Adreno 740, Android 13): boot, the title and play at 60 fps (frame time p50 16.66 ms, GPU about 1.2 ms), no dropped frames in the 300-frame
windows, no audio underrun, save commits work, the shared font set to a Pan-CJK Noto Sans, no red log line; 21,000 frames logged. The data pack is 2.8 GB (RomFS 2.7 GB, `mods`
103 MB, shaders 9.2 MB). Not tested yet: the whole story and its cinematics, touch input, and other GPUs.
