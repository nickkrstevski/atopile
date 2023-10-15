import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from pathlib import Path
from typing import Iterable

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.ParserRuleContext import ParserRuleContext
from rich.progress import Progress

from atopile.parser.AtopileLexer import AtopileLexer
from atopile.parser.AtopileParser import AtopileParser
from atopile.utils import profile as profile_within

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LanguageError(Exception):
    """
    This exception is thrown when there's an error in the syntax of the language
    """

    def __init__(self, message: str, filepath: Path, line: int, column: int) -> None:
        super().__init__(message)
        self.message = message
        self.filepath = filepath
        self.line = line
        self.column = column


class ParserErrorListener(ErrorListener):
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise LanguageError(f"Syntax error: '{msg}'", self.filepath, line, column)


def _parse_file(file_path: Path) -> ParserRuleContext:
    try:
        error_listener = ParserErrorListener(file_path)

        with file_path.open("r", encoding="utf-8") as f:
            input = InputStream(f.read())

        lexer = AtopileLexer(input)
        stream = CommonTokenStream(lexer)
        parser = AtopileParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.file_input()
        return tree
    except LanguageError as ex:
        log.error(f"Language error @ {ex.filepath}:{ex.line}:{ex.column}: {ex.message}")


def parse(
    file_paths: Iterable[Path], profile: bool = False,
    max_workers: int = 4,
) -> dict[Path, ParserRuleContext]:
    """
    Parse all the files in the given paths, returning a map of their trees

    FIXME: this is currently heavily GIL bound.
        Unfortunately, the simple option of using multiprocessing is not available
        because the antlr4 library is not pickleable.
    """
    log.info("Parsing tree")

    profiler_context = profile_within(log) if profile else nullcontext()

    path_to_tree: dict[Path, ParserRuleContext] = {}

    log.info("Searching...")
    file_paths = list(file_paths)

    with (
        profiler_context,
        ThreadPoolExecutor(max_workers=max_workers) as executor,
        Progress() as progress,
    ):
        progress_task = progress.add_task("Parsing...", total=len(file_paths))

        for path, tree in zip(file_paths, executor.map(_parse_file, file_paths)):
            progress.update(progress_task, advance=1)
            path_to_tree[path] = tree
            log.info(f"Finished {str(path)}")

    return path_to_tree
