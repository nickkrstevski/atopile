#looks at the footprints int the ato files and appends the lib path to the kicad fp lib table
# paths should be relative to kicad project which is by default in elec/layout, but the user will be able 
# to change this in the ato.yaml file

eg="""
    (comp (ref "U94")
      (value "5.1k")
      (footprint "Resistor_SMD:R_0402_1005Metric")
      (libsource (lib "generics.ato:Resistor") (part "Resistor") (description "Resistor"))
      (sheetpath (names "skateboard-light.ato:BrakeLight") (tstamps "7d135dd0-ea7b-5ff1-fe8e-c2e30b443e71"))
      (tstamps "4ff4e0fe-173f-3b35-175c-9f966841da87"))
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import ruamel.yaml
from attrs import frozen

from atopile.model.accessors import ModelVertexView
from atopile.model.model import VertexType
from atopile.project.config import BaseConfig
from atopile.project.project import Project
from atopile.targets.targets import Target, TargetCheckResult, TargetMuster

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

class KicadLibPathConfig(BaseConfig):
    @property
    def kicad_project_dir(self) -> Path:
        rel_path = self._config_data.get("kicad-project-dir", "../layout")
        return (self.project.root / rel_path).resolve().absolute()

class KicadLibPath(Target):
    name = "kicad_lib_paths"

    def __init__(self, muster: TargetMuster) -> None:
        self.component_path_to_lib_name: dict[str, str] = {}
        self.lib_name_to_lib_path: dict[str, Path] = {}
        super().__init__(muster)

    @property
    def config(self) -> KicadLibPathConfig:
        return KicadLibPathConfig.from_config(super().build_config)

    def generate(self) ->  None:
        # iterate over all the footprint properties in the project
        # name to absolute path map
        # dictionary 1: map for kicad netlist generator eg lib1 = /home/user/elec/layout/lib1.pretty
        # dicationary 2: ato component path to lib name map

        # project.py get_abs import path
        root_node = ModelVertexView.from_path(self.model, self.build_config.root_node)
        components = root_node.get_descendants(VertexType.component)
        component_path_to_source_path: dict[str, Path] = {}
        component_path_to_project_root: dict[str, Path] = {}
        for component in components:
            path = self.project.get_abs_import_path_from_std_path(Path(component.file_path))
            component_path_to_source_path[component.path] = path
            source_path = Project.from_path(path).root
            component_path_to_project_root[component.path] = source_path

        # find unique lib paths
        unique_project_roots = set(component_path_to_project_root.values())
        project_root_to_lib_name: dict[Path, str] = {}

        for i, project_root in enumerate(unique_project_roots):
            project = Project.from_path(project_root)
            path = project.config.paths.lib_path
            name = "lib" + str(i)
            self.lib_name_to_lib_path[name] = path
            project_root_to_lib_name[project_root] = name

        # component name to lib name
        for component_path, project_root in component_path_to_project_root.items():
            self.component_path_to_lib_name[component_path] = project_root_to_lib_name[project_root]

    def check(self) -> TargetCheckResult:
        return TargetCheckResult.SOLVABLE

    def build(self) -> None:
        """Builds fp-lib-table"""
        fp_lib_table = ['(fp_lib_table', '  (version 7)']

        for lib_name, lib_path in self.lib_name_to_lib_path.items():
            lib_entry = f'  (lib (name "{lib_name}")(type "KiCad")(uri "{lib_path}")(options "")(descr ""))'
            fp_lib_table.append(lib_entry)

        fp_lib_table.append(')')

        fp_lib_table_str = '\n'.join(fp_lib_table)

        # Now you have the fp-lib-table as a string. You can write it to a file in the project under elec/layout.
        kicad_project_dir = self.config.kicad_project_dir
        with open(kicad_project_dir / 'fp-lib-table', 'w') as f:
            f.write(fp_lib_table_str)
