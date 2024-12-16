# -*- mode: python ; coding: utf-8 -*-

import sysconfig

block_cipher = None

added_files = [
    ('settings.json', '.'),
    ('TwitchChannelPointsMiner/assets/*', 'assets'),
    # Dependencies
    ('venv/Lib/site-packages/irc/*.txt', 'irc'),
    ('venv/Lib/site-packages/emoji/unicode_codes/*.json', 'emoji/unicode_codes'),
    ('venv/Lib/site-packages/dateutil/zoneinfo/*.tar.gz', 'dateutil\zoneinfo'),
]

a = Analysis(['TwitchFarm.py'],
             pathex=['venv/Lib'],
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
