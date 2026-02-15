from cppmakelib.utility.decorator import implement
from cppmakelib.utility.time      import time
import os
import shutil
import typing

path = str
resolvable_path = str

def absolute_path        (path         : path)                                                   -> path                 : ...
def add_file_suffix      (file         : path, suffix     : str)                                 -> path                 : ...
def change_current_dir   (dir          : path)                                                   -> None                 : ...
def copy_dir             (from_dir     : path, to_dir     : path)                                -> None                 : ...
def copy_file            (from_file    : path, to_file    : path)                                -> None                 : ...
def copy_softlink        (from_softlink: path, to_softlink: path)                                -> None                 : ...
def count_hardlink       (hardlink     : path)                                                   -> int                  : ...
def current_dir          ()                                                                      -> path                 : ...
def delete_dir           (dir          : path,                    *, not_exist_ok: bool = False) -> None                 : ...
def delete_file          (file         : path,                    *, not_exist_ok: bool = False) -> None                 : ...
def delete_hardlink      (hardlink     : path,                    *, not_exist_ok: bool = False) -> None                 : ...
def delete_softlink      (softlink     : path,                    *, not_exist_ok: bool = False) -> None                 : ...
def exist                (path         : path)                                                   -> bool                 : ...
def get_file_modify_time (file         : path)                                                   -> time                 : ...
def get_file_name        (file         : path)                                                   -> str                  : ...
def get_file_size        (file         : path)                                                   -> int                  : ...
def is_dir               (path         : path)                                                   -> bool                 : ...
def is_file              (path         : path)                                                   -> bool                 : ...
def iterate_dir          (dir          : path)                                                   -> typing.Iterable[path]: ...
def join_path            (*paths       : str)                                                    -> path                 : ...
def new_dir              (dir          : path,                    *, exist_ok    : bool = False) -> path                 : ...
def new_file             (file         : path,                    *, exist_ok    : bool = False) -> path                 : ...
def new_hardlink         (from_hardlink: path, to_path    : path, *, exist_ok    : bool = False) -> path                 : ...
def new_softlink         (from_softlink: path, to_path    : path, *, exist_ok    : bool = False) -> path                 : ...
def normal_path          (path         : path)                                                   -> path                 : ...
def parent_dir           (path         : path)                                                   -> path                 : ...
def read_softlink        (softlink     : path)                                                   -> path                 : ...
def recursive_iterate_dir(dir          : path)                                                   -> typing.Iterable[path]: ...
def relative_path        (from_path    : path, to_path    : path)                                -> path                 : ...
def remove_file_suffix   (file         : path)                                                   -> path                 : ...
def replace_file_suffix  (file         : path, suffix     : str)                                 -> path                 : ...
def resolve_file         (file         : resolvable_path)                                        -> path                 : ...
def root_dir             (path         : path)                                                   -> path                 : ...
def set_file_modify_time (file         : path, time       : time)                                -> None                 : ...



@implement
def absolute_path(path: path) -> path:
    return os.path.abspath(path)

@implement
def add_file_suffix(file: path, suffix: str) -> path:
    if suffix != '':
        return file + os.path.extsep + suffix
    else:
        return file

@implement
def change_current_dir(dir: path) -> None:
    os.chdir(dir)

@implement
def copy_dir(from_dir: path, to_dir: path) -> None:
    shutil.copytree(from_dir, to_dir, dirs_exist_ok=True)

@implement
def copy_file(from_file: path, to_file: path) -> None:
    if not is_file(from_file):
        raise FileNotFoundError(from_file)
    shutil.copyfile(from_file, to_file)

@implement
def copy_softlink(from_softlink: path, to_softlink: path) -> None:
    new_softlink(to_softlink, read_softlink(from_softlink))

@implement
def count_hardlink(hardlink: path) -> int:
    return os.stat(hardlink).st_nlink

@implement
def current_dir() -> path:
    return os.path.curdir

@implement
def delete_dir(dir: path, *, not_exist_ok: bool = False) -> None:
    try:
        shutil.rmtree(dir)
    except FileNotFoundError:
        if not_exist_ok == False:
            raise

@implement
def delete_file(file: path, *, not_exist_ok: bool = False) -> None:
    try:
        os.remove(file)
    except FileNotFoundError:
        if not_exist_ok == False:
            raise

@implement
def delete_hardlink(hardlink: path, *, not_exist_ok: bool = False) -> None:
    try:
        os.remove(hardlink)
    except FileNotFoundError:
        if not_exist_ok == False:
            raise

@implement
def delete_softlink(softlink: path, *, not_exist_ok: bool = False) -> None:
    try:
        os.remove(softlink)
    except FileNotFoundError:
        if not_exist_ok == False:
            raise

@implement
def exist(path: path) -> bool:
    return os.path.exists(path)

@implement
def get_file_modify_time(file: path) -> time:
    return os.stat(file).st_mtime

@implement
def get_file_name(file: path) -> str:
    return os.path.split(file)[-1]

@implement
def get_file_size(file: path) -> int:
    return os.stat(file).st_size

@implement
def is_dir(path: path) -> bool:
    return os.path.isdir(path)

@implement
def is_file(path: path) -> bool:
    return os.path.isfile(path)

@implement
def iterate_dir(dir: path) -> typing.Iterable[path]:
    for subpath in os.listdir(dir):
        yield join_path(dir, subpath)

@implement
def join_path(*paths: str) -> path:
    return os.path.join(*paths)

@implement
def new_dir(dir: path, *, exist_ok: bool = False) -> path:
    try:
        os.makedirs(dir)
    except FileExistsError:
        if exist_ok == False:
            raise
    return dir

@implement
def new_file(file: path, *, exist_ok: bool = False) -> path:
    new_dir(parent_dir(file), exist_ok=True)
    try:
        open(file, 'x')
    except FileExistsError:
        if exist_ok == False:
            raise
    return file

@implement
def new_hardlink(from_hardlink: path, to_path: path, *, exist_ok: bool = False) -> path:
    try:
        os.link(to_path, from_hardlink)
    except FileExistsError:
        if exist_ok == False:
            raise
    return from_hardlink

@implement
def new_softlink(from_softlink: path, to_path: path, *, exist_ok: bool = False) -> path:
    try:
        os.symlink(relative_path(to_path, parent_dir(from_softlink)), from_softlink)
    except FileExistsError:
        if exist_ok == False:
            raise
    return from_softlink

@implement
def normal_path(path: path) -> path:
    return os.path.normpath(path)

@implement
def parent_dir(path: path) -> path:
    return normal_path(join_path(path, os.path.pardir))

@implement
def read_softlink(softlink: path) -> path:
    return os.readlink(softlink)

@implement
def recursive_iterate_dir(dir: path) -> typing.Iterable[path]:
    for root, _, subfiles in os.walk(dir):
        for subfile in subfiles:
            yield join_path(root, subfile)

@implement
def relative_path(from_path: path, to_path: path) -> path:
    return os.path.relpath(to_path, from_path)

@implement
def remove_file_suffix(file: path) -> path:
    return os.path.splitext(file)[0]

@implement
def replace_file_suffix(file: path, suffix: str) -> path:
    if suffix != '':
        return os.path.splitext(file)[0] + os.path.extsep + suffix
    else:
        return os.path.splitext(file)[0]

@implement
def resolve_file(file: resolvable_path) -> path:
    resolved = shutil.which(file)
    if resolved is not None:
        return resolved
    else:
        raise FileNotFoundError(file)

@implement
def root_dir(path: path) -> path:
    return os.path.splitroot(path)[0]

@implement
def set_file_modify_time(file: path, time: time) -> None:
    os.utime(file, (time, time))
