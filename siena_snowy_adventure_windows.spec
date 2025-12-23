# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Siena's Snowy Adventure - WINDOWS VERSION
Run this on a Windows machine to build the .exe
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config.yaml', '.'),
        ('src', 'src'),
        ('VERSION', '.'),  # Include version file
        ('.env', '.'),  # Include Firebase configuration
        # Note: firebase-key.json not needed - game uses REST API, not admin SDK
    ],
    hiddenimports=['dotenv', 'dotenv.main'],
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
    [],
    exclude_binaries=True,
    name='SienaSnowyAdventure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    target_arch=None,
    icon='assets/icon.ico',  # Windows application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SienaSnowyAdventure',
)
