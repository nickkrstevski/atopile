from pathlib import Path
from typing import Optional


class AtoError(Exception):
    """
    This exception is thrown when there's an error in the syntax of the language
    """

    def __init__(
        self,
        message: str,
        src_path: Optional[str | Path],
        src_line: Optional[int],
        src_col: Optional[int],
        *args: object,
    ) -> None:
        super().__init__(message, *args)
        self.message = message
        self._src_path = src_path
        self.src_line = src_line
        self.src_col = src_col

    @property
    def user_facing_name(self):
        return self.__class__.__name__[3:]


class AtoSyntaxError(AtoError):
    """
    Raised when there's an error in the syntax of the language
    """


class AtoKeyError(AtoError, KeyError):
    """
    Raised if a name isn't found in the current scope.
    """


class AtoTypeError(AtoError):
    """
    Raised if something is the wrong type.
    """


class AtoNameConflictError(AtoError):
    """
    Raised if something has a conflicting name in the same scope.
    """


class AtoCircularDependencyError(AtoError):
    """
    Raised if something has a conflicting name in the same scope.
    """


class AtoImportNotFoundError(AtoError):
    """
    Raised if something has a conflicting name in the same scope.
    """
