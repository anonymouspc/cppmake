from cppmake.file.file_system  import create_dir, remove_dir, copy_file, copy_dir
from cppmake.utility.decorator import syncable

def include(package, file, dir, relpath="."): ...

def include(package, file=None, dir=None, relpath="."):
    try:
        create_dir(package.include_dir)
        if file is not None:
            copy_file(f"{package.git_dir}/{file}", f"{package.include_dir}/{relpath}/")
        if dir is not None:
            copy_dir(f"{package.git_dir}/{dir}",   f"{package.include_dir}/{relpath}")
    except:
        remove_dir(package.install_dir)
        raise

