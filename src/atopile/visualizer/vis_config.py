# this is way too complicated for what we're currently trying to do, dropping it for now

from pathlib import Path
from typing import Dict, List

import ruamel.yaml

from atopile.model.model import Model
from atopile.project.project import Project

VIS_FILE_NAME = "vis.yaml"

class VisCascade:
    def __init__(self, project: Project, model: Model) -> None:
        self._project: Project = project
        self._model: Model = model
        self._files: List[Path] = []
        self._entries: Dict[str, List[VisEntry]] = {}

    def setup(self) -> None:
        """
        Run once after the project and model are loaded to find and process all the vis configs.
        """

        # find all the vis files in the project
        model_abs_src_files = [self._project.get_abs_import_path_from_std_path(i) for i in self._model.src_files]
        vis_search_paths = {p.parent for p in model_abs_src_files}
        for p in vis_search_paths:
            vis_candidate = p / VIS_FILE_NAME
            if vis_candidate.exists():
                self._files.append(vis_candidate)

        # find all the entries in the vis files

    def get_entries_for_path(self, object_path: str) -> List["VisEntry"]:
        """
        Return a list of VisEntry objects for the given model object_path in order of precidence
        """
        return self._entries.get(object_path, [])

class VisEntry:
    """
    Thin wrapper around the properties we expect to access for a visualization configuration block in a YAML file.
    This exists to allow us to access and manipulate these properties in a structured way, without copying all the data and messing up the stucture/comments.
    """

    def __init__(self, cascade: VisCascade, file: Path, block: str) -> None:
        self.file_data = file_data
        self.entry_key = entry_key

    @property
    def path(self) -> str:
        return self.file_data[self.entry_key]['path']

    @path.setter
    def path(self, value: str) -> None:
        self.file_data[self.entry_key]['path'] = value

class VisPin(VisEntry):
    @property
    def stub(self) -> bool:
        return self.file_data[self.entry_key]['stub']

    @stub.setter
    def stub(self, value: bool) -> None:
        self.file_data[self.entry_key]['stub'] = value

    @property
    def position(self) -> str:
        return self.file_data[self.entry_key]['position']

    @position.setter
    def position(self, value: str) -> None:
        self.file_data[self.entry_key]['position'] = value
