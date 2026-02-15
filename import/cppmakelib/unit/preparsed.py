from cppmakelib.basic.context      import context
from cppmakelib.unit.binary        import Binary
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import normal_path, path

class Preparsed(Binary):
    def __new__ (cls,  file: path) -> Preparsed: ...
    def __init__(self, file: path) -> None     : ...



@member(Preparsed)
@unique_in(context.package)
@pre(normal_path)
def __init__(self: Preparsed, file: path) -> None:
    super(Preparsed, self).__init__(file)