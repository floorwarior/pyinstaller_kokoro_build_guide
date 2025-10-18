# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['kokororeader.py'],
    pathex=[],
    binaries=[],
    datas=[
        (".venv/Lib/site-packages/language_tags","language_tags"),
        (".venv/Lib/site-packages/language_data","language_data"),
        (".venv/Lib/site-packages/spacy","spacy"),
        (".venv/Lib/site-packages/spacy_legacy","spacy_legacy"),
        (".venv/Lib/site-packages/spacy_curated_transformers","spacy_curated_transformers"),
        (".venv/Lib/site-packages/spacy_loggers","spacy_loggers"),
        (".venv/Lib/site-packages/espeakng_loader","espeakng_loader"),
        (".venv/Lib/site-packages/misaki","misaki"),
        ("kokoromodels","kokoromodels"),
        ("en_core_web_sm","en_core_web_sm")
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='kokororeader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='kokororeader',
)
