class AtoCompileError(Exception):
    """
    This exception is thrown when there's an error in the syntax of the language
    """

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        self.message = message

    @property
    def user_facing_name(self):
        return self.__class__.__name__[3:]


class AtoKeyError(AtoCompileError, KeyError):
    """
    Raised if a name isn't found in the current scope.
    """


class AtoTypeError(AtoCompileError):
    """
    Raised if something is the wrong type.
    """


class AtoNameConflictError(AtoCompileError):
    """
    Raised if something has a conflicting name in the same scope.
    """


class AtoCircularDependencyError(AtoCompileError):
    """
    Raised if something has a conflicting name in the same scope.
    """


class AtoImportNotFoundError(AtoCompileError):
    """
    Raised if something has a conflicting name in the same scope.
    """
