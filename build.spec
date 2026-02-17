# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Detect platform for the icon
if sys.platform == 'win32':
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.ico')
elif sys.platform == 'darwin':
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.icns')
else:
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.png')

a = Analysis(
  ['main.py'],
  pathex=[],
  binaries=[],
  datas=[
    ('src', 'src'),
    ('assets', 'assets'),
    ('version.txt', '.'),
    ('src/back/extra/settings.json', 'src/back/system/extra'),
  ],
  hiddenimports=[
    'webview.platforms.winforms',
    'webview.platforms.cocoa',
    'webview.platforms.qt',
    'clr',
    'desktop_notifier',
    'desktop_notifier.resources',
    'pystray._win32',
  ],
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
  name='SendYourFiles',
  debug=False,
  bootloader_ignore_signals=False,
  strip=False,
  upx=True,
  upx_exclude=[],
  runtime_tmpdir=None,
  console=False,
  disable_windowed_traceback=False,
  argv_emulation=False,
  target_arch=None,
  codesign_identity=None,
  entitlements_file=None,
  icon=icon_file,
)
