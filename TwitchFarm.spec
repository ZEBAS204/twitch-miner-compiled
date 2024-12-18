# -*- mode: python ; coding: utf-8 -*-

import sysconfig
from PyInstaller.utils.hooks import get_package_paths

block_cipher = None

def get_PKG(name, path):
    # Assuming get_package_paths() is already defined elsewhere
    return get_package_paths(name)[1] + path

added_files = [
    ('settings.json', '.'),
    ('TwitchChannelPointsMiner/assets/*', 'assets'),
    # Dependencies
    (get_PKG('irc', '/*.txt'), 'irc'),
    (get_PKG('emoji', '/unicode_codes/*.json'), 'emoji/unicode_codes'),
    (get_PKG('dateutil', '/zoneinfo/*.tar.gz'), 'dateutil\zoneinfo'),
]

a = Analysis(['TwitchFarm.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False
            )

pyz = PYZ(
    a.pure, a.zipped_data, cipher=block_cipher
)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=f"TwitchFarm-{sysconfig.get_platform()}",
          icon='icon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None
          )
