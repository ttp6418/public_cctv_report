# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['server_kumkang.py'],
             pathex=['C:\\Users\\82107\\PycharmProjects\\engineeringDesign'],
             binaries=[],
             datas=[('./black.jpg', './'), ('./exit.png', './'), ('./left.png', './'), ('./none.png', './'), ('./right.png', './'), ('./river.png', './'), ('./yolo/coco.names', './yolo'), ('./yolo/yolov4.weights', './yolo'), ('./yolo/yolov4.cfg', './yolo')],
             hiddenimports=[],
             hookspath=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='server_kumkang',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
