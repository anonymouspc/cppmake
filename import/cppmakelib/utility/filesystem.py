from cppmakelib.utility.time import time
import os
import shutil
import typing

path = str
resolvable_path = str

def absolute_path        (path         : path)                    -> path                 : ...
def add_file_suffix      (file         : path, suffix     : str)  -> path                 : ...
def change_current_dir   (dir          : path)                    -> None                 : ...
def copy_dir             (from_dir     : path, to_dir     : path) -> None                 : ...
def copy_file            (from_file    : path, to_file    : path) -> None                 : ...
def copy_softlink        (from_softlink: path, to_softlink: path) -> None                 : ...
def count_hardlink       (hardlink     : path)                    -> int                  : ...
def create_dir           (dir          : path)                    -> None                 : ...
def create_file          (file         : path)                    -> None                 : ...
def create_hardlink      (from_hardlink: path, to_path    : path) -> None                 : ...
def create_softlink      (from_softlink: path, to_path    : path) -> None                 : ...
def current_dir          ()                                       -> path                 : ...
def exist_dir            (dir          : path)                    -> bool                 : ...
def exist_file           (file         : path)                    -> bool                 : ...
def get_file_modify_time (file         : path)                    -> time                 : ...
def get_file_name        (file         : path)                    -> str                  : ...
def get_file_size        (file         : path)                    -> int                  : ...
def iterate_dir          (dir          : path)                    -> typing.Iterable[path]: ...
def join_path            (*paths       : str)                     -> path                 : ...
def normal_path          (path         : path)                    -> path                 : ...
def parent_dir           (path         : path)                    -> path                 : ...
def read_softlink        (softlink     : path)                    -> path                 : ...
def recursive_iterate_dir(dir          : path)                    -> typing.Iterable[path]: ...
def relative_path        (from_path    : path, to_path    : path) -> path                 : ...
def remove_dir           (dir          : path)                    -> None                 : ...
def remove_file          (file         : path)                    -> None                 : ...
def remove_file_suffix   (file         : path)                    -> path                 : ...
def replace_file_suffix  (file         : path, suffix     : str)  -> path                 : ...
def resolve_file         (file         : resolvable_path)         -> path                 : ...
def root_dir             (path         : path)                    -> path                 : ...
def set_file_modify_time (file         : path, time       : time) -> None                 : ...



def absolute_path(path: path) -> path:
    return os.path.abspath(path)

def add_file_suffix(file: path, suffix: str) -> path:
    if suffix != '':
        return file + os.path.extsep + suffix
    else:
        return file

def change_current_dir(dir: path) -> None:
    os.chdir(dir)

def copy_dir(from_dir: path, to_dir: path) -> None:
    shutil.copytree(from_dir, to_dir, dirs_exist_ok=True)

def copy_file(from_file: path, to_file: path) -> None:
    shutil.copyfile(from_file, to_file)

def copy_softlink(from_softlink: path, to_softlink: path) -> None:
    create_softlink(to_softlink, read_softlink(from_softlink))

def count_hardlink(hardlink: path) -> int:
    return os.stat(hardlink).st_nlink

def create_dir(dir: path) -> None:
    os.makedirs(dir, exist_ok=True)

def create_file(file: path) -> None:
    create_dir(parent_dir(file))
    open(file, 'w')

def create_hardlink(from_hardlink: path, to_path: path) -> None:
    os.link(to_path, from_hardlink)

def create_softlink(from_softlink: path, to_path: path) -> None:
    os.symlink(relative_path(to_path, from_softlink), from_softlink)

def current_dir() -> path:
    return os.path.curdir

def exist_dir(dir: path) -> bool:
    return os.path.isdir(dir)

def exist_file(file: path) -> bool:
    return os.path.isfile(file)

def get_file_modify_time(file: path) -> time:
    return os.stat(file).st_mtime_ns

def get_file_name(file: path) -> str:
    return os.path.split(file)[-1]

def get_file_size(file: path) -> int:
    return os.stat(file).st_size

def iterate_dir(dir: path) -> typing.Iterable[path]:
    for subpath in os.listdir(dir):
        yield join_path(dir, subpath)

def join_path(*paths: str) -> path:
    return os.path.join(*paths)

def normal_path(path: path) -> path:
    return os.path.normpath(path)

def parent_dir(self: path) -> path:
    return os.path.dirname(self)

def read_softlink(softlink: path) -> path:
    return os.readlink(softlink)

def recursive_iterate_dir(dir: path) -> typing.Iterable[path]:
    for root, _, subfiles in os.walk(dir):
        for subfile in subfiles:
            yield join_path(root, subfile)

def relative_path(from_path: path, to_path: path) -> path:
    return os.path.relpath(to_path, from_path)

def remove_dir(dir: path) -> None:
    shutil.rmtree(dir)

def remove_file(file: path) -> None:
    os.remove(file)

def remove_file_suffix(file: path) -> path:
    return os.path.splitext(file)[0]

def replace_file_suffix(file: path, suffix: str) -> path:
    if suffix != '':
        return os.path.splitext(file)[0] + os.path.extsep + suffix
    else:
        return os.path.splitext(file)[0]

def resolve_file(file: resolvable_path) -> path:
    resolved = shutil.which(file)
    if resolved is not None:
        return resolved
    else:
        raise FileNotFoundError(file)

def root_dir(path: path) -> path:
    return os.path.splitroot(path)[0]

def set_file_modify_time(file: path, time: time) -> None:
    os.utime(file, ns=(time, time))
