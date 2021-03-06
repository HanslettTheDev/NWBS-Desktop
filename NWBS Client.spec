# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['manage.py'],
             pathex=[],
             binaries=[],
             datas=[('./debug/*', 'debug'), ('./logs/*', 'logs'), ('./meeting_parts/*', 'meeting_parts'), ('./resources/*', 'resources'), ('./scripts', 'scripts'), ('./templates/*', 'templates'), ('./years/*', 'years'), ('./_programs/*', '_programs')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='NWBS Client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , uac_admin=True, icon='logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='NWBS Client')
