# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

if sys.platform == 'win32':
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.ico')
elif sys.platform == 'darwin':
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.icns')
else:
  icon_file = os.path.join('assets', 'icon', 'SendYourFiles.png')

linuxData = []
linuxHiddenImports = []
if sys.platform.startswith('linux'):
  linuxData = [
    ('/usr/lib/x86_64-linux-gnu/girepository-1.0/DBus-1.0.typelib', 'gi_typelibs/DBus-1.0.typelib'),
    ('/usr/lib/x86_64-linux-gnu/girepository-1.0/AyatanaAppIndicator3-0.1.typelib', 'gi_typelibs/AyatanaAppIndicator3-0.1.typelib'),
    ('/usr/lib/x86_64-linux-gnu/girepository-1.0/Gtk-3.0.typelib', 'gi_typelibs/Gtk-3.0.typelib'),
    ('/usr/lib/x86_64-linux-gnu/girepository-1.0/GObject-2.0.typelib', 'gi_typelibs/GObject-2.0.typelib'),
  ]
  
  linuxHiddenImports = [
    'gi',
    'gi.repository',
    'gi.repository.GObject',
    'gi.repository.Gtk',
    'gi.repository.DBus',
    'gi.repository.AyatanaAppIndicator3',
    'pystray._appindicator',
    'pystray._util.gtk',
    'pystray._util.notify_dbus',
  ]

a = Analysis(
  ['main.py'],
  pathex=[],
  binaries=[],

  datas=[
    ('src', 'src'),
    ('assets', 'assets'),
    ('version.txt', '.'),
    ('src/back/extra/settings.json', 'src/back/system/extra'),
  ] + linuxData,
  hiddenimports=[
    'webview.platforms.winforms',
    'webview.platforms.cocoa',
    'webview.platforms.qt',
    'clr',
    'desktop_notifier',
    'desktop_notifier.resources',
    'pystray._win32',
  ] + linuxHiddenImports,

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