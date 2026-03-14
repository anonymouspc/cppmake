Here are several principles of developments.

0. A builder should not rely on another builder (just like the question "the chicken or the egg appears first"). So that:
    - We **cannot** use `cmake` or `makefile` as our builder.
    - We **cannot** import libraries who uses `cmake` of `makefile` as builder.
        - `boost` uses `b2` (which only depends on `bootstrap.sh` that invokes the compiler and outputs a self-written builder) as builder.
        - `stdexec` or `beman::execution` are header-only, which only depends on `cp` command.
    - We should use **as less commands as possible** in the `xxx-make` script.
