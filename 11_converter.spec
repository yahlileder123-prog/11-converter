# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for 11 CONVERTER. Build: pyinstaller 11_converter.spec
# See PACKAGING.md.
import os

from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []

for pkg in ("tkinterdnd2", "customtkinter"):
    tmp_ret = collect_all(pkg)
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]

_root = os.path.abspath(SPECPATH)
_ffdir = os.path.join(_root, "vendor", "ffmpeg")
for _name in ("ffmpeg.exe", "ffprobe.exe"):
    _path = os.path.join(_ffdir, _name)
    if os.path.isfile(_path):
        binaries.append((_path, "."))

_icon = "app.ico" if os.path.isfile("app.ico") else None

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="11_CONVERTER",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="11_CONVERTER",
    strip=False,
    upx=False,
    upx_exclude=[],
)
