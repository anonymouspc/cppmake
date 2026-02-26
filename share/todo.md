- 关于继承的设计准则: 不主动使用**抽象**基类.
    - 例如:
        - Clang是客观存在的,且Clang宣称自己是Gcc(因为#define __GNUC__),且Clang('clang++')与Gcc('clang++')含义无关,那么Clang继承自Gcc
        - StdPackage是客观存在的,且StdPackage宣称自己是特殊的包,且StdPackage('boost')非良构,所以StdPackage继承自Package
        - Code不是客观存在的(而是抽象类),且Module('import/cppcore.cpp')会和Code('import/cppcore.cpp')产生歧义,所以不应当抽象出Module继承自Code
    - 一个简单的判别方法是:
        - 是否使用super().__init__().抽象基类通常需要super().__init__(),而客观基类通常不需要super().__init__().

- 关于共享接口的设计准则: 你不必为你用不到的特性付出代价.
    - 例如:
        - Gcc不需要precompile后再compile,而RemoteCompiler需要precompile后再compile,则RemoteCompiler自行实现Source->Preprocessed->Object的逻辑而不干涉常规Gcc的Source->Object逻辑
        - Clang没有.sarif,而Gcc有.sarif,则Gcc自行实现.sarif的输出.
    - 简单的判别方法是
        - 使用replace_file_suffix的通常是"不付出额外代价"的.

- 重新把@unique_in中改为层层{},而不是[(a, b, c)]

- UnitStatusCacher._reflect()需要更深的信息，至少把compiler.version反射了

- get_source_imports()记录每个module的潜在的(假设同context下的)module.file
- Source.__init__()挑选实际存在的module.file
- get_source_compiled()对比Source.import_modules，如果file存在不同，则_StatusNeedsUpdateError.
- UnitStatusCacher._reflect()需要更深的信息，至少把Source.import_modules.keys()反射了 **注意这里不是keys()**

- UnitStatusCacher.get_module_name()调用compiler.xxx(), 同时set_module_name()和set_module_imports(), 能高效。
    - 保留.ipp
        - -H的结果以注释形式存放在开头/末尾
        - .ipp不是必须的产物
        - preprocess()遵循产出文件而非stdout的统一格式
    - 不保留.ipp
        - 每个preprocess()有不同的约束。例如Module.preprocess()一般要检查export，而Source.preprocess()一般不检查export.
            - 所以不可以Code.preprocess()，而应该compiler.preprocess()或者compiler.get_meta()
            - 即, compiler必须完成parse-stderr-from-H这一步

- 加入"--machine=x86_64-pc-linux-gnu"选项，或 
    - "--machine-architecture=xxx",
    - "--machine-vendor=xxx",
    - "--machine-system=xxx
    - "--machine-abi=xxx",
    - 注意"--target=xxx"已经被占用为"编译目标".
        - 用"--architecture".



Package -> context -> main_package ->? Package
- StdPackage改名为StdLibrary,MainPackage改名? 这样这样就能"平行"了.
