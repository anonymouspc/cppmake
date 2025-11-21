from cppmakelib.basic.config     import *
from cppmakelib.file.file_system import absolute_path, base_path

project = ...



class _Project:
    pass

project = _Project()
project.name = base_path(absolute_path('.'))