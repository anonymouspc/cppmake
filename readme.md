# make.cpp

A modern C++ builder based on C++20 Modules.

## Overview

`make.cpp` (`cppmake`) is a build system written in modern C++ that leverages C++26 Modules. It supports building C++ projects on Linux, macOS (Mach), and Windows.

## Requirements

- A C++26-capable compiler:
  - **Linux**: GCC with `-std=c++26 -fmodules`
  - **macOS**: Clang with `-std=c++26 -stdlib=libc++`
  - **Windows**: MSVC
- Boost libraries (asio, dll, process, program_options)

## Building

### Linux

```sh
./make-linux.sh
```

### macOS

```sh
./make-mach.sh
```

### Windows

```cmd
make-win32.cmd
```

The compiled binary will be placed at `.cppmake/bin/main`.

## Project Structure

```
bin/          # Entry point (main.cpp)
import/       # cppmake module source files
  cppmake.cpp           # Root module
  cppmake/
    basic/    # Configuration
    compiler/ # Compiler abstractions (gcc, clang, emcc)
    error/    # Error types
    system/   # Platform detection (linux, mach, win32)
    unit/     # Build unit types (executable, module, object, …)
    utility/  # Helpers (argv, filesystem, templates, …)
pkg/          # Dependency build scripts (std, boost)
share/        # Design notes
```

## License

See [license.txt](license.txt).
