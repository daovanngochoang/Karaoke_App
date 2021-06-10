# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['GUI/Main.py','Data_manager/src/bill_manager.py', 'Data_manager/src/Order_detail_manager.py',
                'Data_manager/src/orders_manager.py', 'Data_manager/src/product_manager.py', 'Data_manager/src/Storage_data.py',
                'Data_manager/src/time_control.py', 'Data_manager/Controller.py',
                'GUI/tab.py','GUI/Main_image/background.jpg', 'GUI/Main_image/bia-tiger-lon.png',
                'GUI/Main_image/bia_ken.jpg', 'GUI/Main_image/ca_chach _chien.jpg', 'GUI/Main_image/cafe-da.png', 'GUI/Main_image/caffe-sua.png',
                'GUI/Main_image/cha_lua.jpg', 'GUI/Main_image/chao_ga.png', 'GUI/Main_image/dau-phong.png', 'GUI/Main_image/ga_chien.jpg', 'GUI/Main_image/ga_nuong.jpg',
                'GUI/Main_image/girl.jpg', 'GUI/Main_image/keo-siggum.png', 'GUI/Main_image/khan_lanh.png', 'GUI/Main_image/kho-muc.png', 'GUI/Main_image/logo.png', 'GUI/Main_image/mi-xao.jpg',
                'GUI/Main_image/mi_tom.jpg', 'GUI/Main_image/nuoc_chanh.jpg', 'GUI/Main_image/nuoc_ngot.png', 'GUI/Main_image/saigondo.png',
                'GUI/Main_image/snack.png', 'GUI/Main_image/thuoc-hero.png', 'GUI/Main_image/thuocjet.png', 'GUI/Main_image/traicay.png',
                'GUI/Main_image/trungga_nuong.jpg', 'GUI/Main_image/xuc_xich.jpg'],
             pathex=['C:\\Users\\LENOVO\\Desktop\\App'],
             binaries=[],
             datas=[],
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
          [],
          exclude_binaries=True,
          name='Main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Main')
