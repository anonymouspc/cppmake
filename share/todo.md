- `Object.__init__(file=..., from_=...)`缺少类型注释，
- `Object`可以改为from_codes = [], lib_dirs = []
- `UnitStatusCacher._reflect()`需要更深的信息，至少把compiler.version反射了

- `get_source_imports()`记录每个module的潜在的(假设同context下的)module.file
- `Source.__init__()`挑选实际存在的module.file
- `get_source_compiled()`对比`Source.import_modules`，如果file存在不同，则`_StatusNeedsUpdateError`.
- `UnitStatusCacher._reflect()`需要更深的信息，至少把`Source.import_modules.keys()`反射了 **注意这里不是keys()**

- 加入"--machine=x84_64-pc-linux-gnu"选项，或 
    - "--machine-architecture=xxx",
    - "--machine-vendor=xxx",
    - "--machine-system=xxx
    - "--machine-abi=xxx",
    - 注意"--target=xxx"已经被占用为"编译目标"了。
        - 用"--architecture"。


