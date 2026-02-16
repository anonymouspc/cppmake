from cppmakelib.basic.context      import context
from cppmakelib.unit.binary        import Binary
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import normal_path, path

class Dynamic(Binary):
    def __new__ (cls : type[Dynamic], file: path) -> Dynamic: ...
    def __init__(self: Dynamic,       file: path) -> None   : ...


@member(Dynamic)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Dynamic, file: path) -> None:
    super(Dynamic, self).__init__(file)
