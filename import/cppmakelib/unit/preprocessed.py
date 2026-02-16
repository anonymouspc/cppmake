from cppmakelib.basic.context      import context
from cppmakelib.unit.binary        import Binary
from cppmakelib.utility.decorator  import member, pre, unique_in
from cppmakelib.utility.filesystem import normal_path, path

class Preprocessed(Binary): # `Preprocessed` is phycially `Code` but logically `Binary`
    def __new__ (cls : type[Preprocessed], file: path) -> Preprocessed: ...
    def __init__(self: Preprocessed,       file: path) -> None        : ...



@member(Preprocessed)
@unique_in(context.package)
@pre(1, normal_path)
def __init__(self: Preprocessed, file: path) -> None:
    super(Preprocessed, self).__init__(file)