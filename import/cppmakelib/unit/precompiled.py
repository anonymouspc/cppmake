from cppmakelib.basic.context      import context
from cppmakelib.unit.binary        import Binary
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import normal_path, path

class Precompiled(Binary):
    def __new__ (cls,  file: path) -> Precompiled: ...
    def __init__(self, file: path) -> None       : ...



@member(Precompiled)
@unique_in(context.package)
@pre(normal_path)
def __init__(self: Precompiled, file: path) -> None:
    super(Precompiled, self).__init__(file)