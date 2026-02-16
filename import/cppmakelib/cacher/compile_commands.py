from cppmakelib.basic.config       import config
from cppmakelib.utility.decorator  import lifetime, member
from cppmakelib.utility.filesystem import absolute_path, current_dir, join_path, new_dir, parent_dir, path
import atexit
import json
import typing

class CompileCommandsCacher:
    def __init__(self: CompileCommandsCacher)                                 -> None: ...
    def __del__ (self: CompileCommandsCacher)                                 -> None: ...
    def   set   (self: CompileCommandsCacher, file: path, command: list[str]) -> None: ...

    _file    : path
    _content : typing.Any

compile_commands_cacher: CompileCommandsCacher



@member(CompileCommandsCacher)
def __init__(self: CompileCommandsCacher) -> None:
    self._file = join_path(config.build_dir, '.cache', 'compile_commands.json')
    try:
        self._content = json.load(open(self._file, 'r'))
    except:
        self._content = []
    atexit.register(self.__del__)

@member(CompileCommandsCacher)
@lifetime(open, json, new_dir, parent_dir)
def __del__(self: CompileCommandsCacher) -> None:
    new_dir(parent_dir(self._file), exist_ok=True)
    json.dump(self._content, open(self._file, 'w'), indent=4)

@member(CompileCommandsCacher)
def set(self: CompileCommandsCacher, file: path, command: list[str]) -> None:
    for entry in self._content:
        if entry['directory'] == absolute_path(current_dir()) and entry['file'] == file:
            self._content.remove(entry)
    self._content.append({
        'directory': absolute_path(''),
        'file'     : file,
        'command'  : ' '.join(command)
    })

compile_commands_cacher = CompileCommandsCacher()
