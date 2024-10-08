# -*- mode: python -*-

block_cipher = None

from site import getsitepackages

include_files = [
    ('./README.md', '.'),
    ('license.txt', '.'),
    ('*.cfg.default', '.'),
    ('version', '.'),
    ('art', 'art'),
    ('charsets', 'charsets'),
    ('palettes', 'palettes'),
    ('artscripts', 'artscripts'),
    ('formats', 'formats'),
    ('shaders', 'shaders'),
    ('games', 'games'),
    ('ui/*.png', 'ui'),
    ('docs/html/*.*', 'docs/html'),
    ('docs/html/generated/*.*', 'docs/html/generated')
]

include_bins = [
    ('/usr/local/Cellar/sdl2/2.0.16/lib/libSDL2-2.0.0.dylib', '.'),
    ('/usr/local/Cellar/sdl2_mixer/2.0.4_2/lib/libSDL2_mixer-2.0.0.dylib', '.'),
    ('/usr/local/Cellar/flac/1.3.3/lib/libFLAC.8.dylib', '.'),
    ('/usr/local/Cellar/libmikmod/3.3.11.1/lib/libmikmod.3.dylib', '.'),
    ('/usr/local/Cellar/libmodplug/0.8.9.0/lib/libmodplug.1.dylib', '.'),
    ('/usr/local/Cellar/libogg/1.3.5/lib/libogg.0.dylib', '.'),
    ('/usr/local/Cellar/libvorbis/1.3.7/lib/libvorbis.0.dylib', '.'),
    ('/usr/local/Cellar/libvorbis/1.3.7/lib/libvorbisfile.3.dylib', '.'),
    ('/usr/local/Cellar/smpeg2/2.0.0/lib/libsmpeg2-2.0.0.dylib', '.')
]

a = Analysis(['playscii.py'],
             pathex=['./'],
             binaries=include_bins,
             datas=include_files,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=['pdoc'],
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='playscii',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='playscii')
app = BUNDLE(coll,
             name='Playscii.app',
             icon='ui/playscii.icns',
             bundle_identifier='net.jplebreton.playscii')
