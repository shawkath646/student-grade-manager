# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Build from project root, not scripts folder
# When running from project root: pyinstaller scripts/build_exe.spec
import pathlib
project_root = str(pathlib.Path(__file__).parent.parent.absolute()) if '__file__' in globals() else os.getcwd()

block_cipher = None

# Collect all data files from project root
datas = [
    (os.path.join(project_root, 'data'), 'data'),
    (os.path.join(project_root, 'assets'), 'assets'),
]

# Collect hidden imports
hiddenimports = [
    'mysql.connector',
    'PIL._tkinter_finder',
    'tkinter',
    'tkinter.ttk',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
]

# Collect all submodules
hiddenimports += collect_submodules('mysql.connector')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('matplotlib')

a = Analysis(
    [os.path.join(project_root, 'scripts', 'run_app.py')],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='StudentGradeManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
