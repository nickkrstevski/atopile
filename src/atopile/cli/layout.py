"""CLI command definition for `ato build`."""

import logging
import re
import shutil
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import click
from attrs import frozen

from atopile import address
from atopile.bom import generate_bom as _generate_bom
from atopile.bom import generate_designator_map as _generate_designator_map
from atopile.cli.build import BuildArgs
from atopile.cli.common import project_options
from atopile.config import Config, get_project_config_from_addr
from atopile.errors import (handle_ato_errors, iter_through_errors,
                            muffle_fatalities)
from atopile.front_end import set_search_paths
from atopile.netlist import get_netlist_as_str
from atopile import instance_methods, components
from atopile import netlist


log = logging.getLogger(__name__)


@click.command()
@project_options
@click.option("--debug/--no-debug", default=None)
@muffle_fatalities
def layout(config: Config, debug: bool, capture: bool, apply: bool):
    """
    Build the specified --target(s) or the targets specified by the build config.
    Specify the root source file with the argument SOURCE.
    eg. `ato build --target my_target path/to/source.ato:module.path`
    """
    # Set the log level
    if debug:
        logging.root.setLevel(logging.DEBUG)

    # Set the search paths for the front end
    set_search_paths([config.paths.abs_src, config.paths.abs_module_path])

    # Create a BuildArgs object to pass to all the targets
    build_args = BuildArgs.from_config(config)

    # Ensure the build directory exists
    log.info("Writing outputs to %s", build_args.build_path)
    build_args.build_path.mkdir(parents=True, exist_ok=True)

    # generate component map


    # get component positions
    # kicad_layout = get_kicad_component_positions(build_args.build_path / "kicad_pcb.kicad_pcb")
    layout_file = build_args.build_path.parent.parent / f"elec/layout/{build_args.output_name}.kicad_pcb"
    positions = get_kicad_component_positions(layout_file.read_text())

    # save component map

# %%
def _get_super(instance: address.AddrStr) -> address.AddrStr:
    """
    Get the super of the current address.
    """
    raise NotImplementedError


def _kicad_project_for_module(module_addr: address.AddrStr) -> Path:
    """
    Get the path to the kicad project for a module.
    """
    raise NotImplementedError
    module_config = get_project_config_from_addr("<module-addr>")
    for build_config in module_config.builds.values():
        pass


# FIXME: move this to address or instance_methods
def _get_relative_addr_str(address: address.AddrStr, relative_to: address.AddrStr) -> address.AddrStr:
    """
    Get the relative address.
    """
    if not address.startswith(relative_to):
        raise ValueError(f"{address} is not a child of {relative_to}")
    return address[len(relative_to) + 1 :]


def apply_layout_of_module(module_instance: address.AddrStr, offset_x: float, offset_y: float) -> None:
    """
    Get the layout of a module.
    """

    # module_addr ~= "/.../regs.ato:LDO::feedback_vdiv"

    # assuming we have a VDiv module ~= "/.../vdiv.ato::VDiv"
    # under it it has two resistors ~= "/.../vdiv.ato::VDiv:r1" and "/.../vdiv.ato::VDiv:r2"

    # assume that the instance tree under the module is identical to the instance of that module
    # this implies that all the components are in the layout as well
    # if they're not, let's throw an error

    # get components
    subcomponents = filter(instance_methods.match_components, instance_methods.all_descendants(module_instance))
    # eg. "/.../regs.ato:LDO::feedback_vdiv.r1", "/.../regs.ato:LDO::feedback_vdiv.r2"

    from_uuid_to_uuid = {}
    for subcomponent_addr in subcomponents:
        from_addr  = subcomponent_addr
        to_addr = _get_relative_addr_str(subcomponent_addr, module_instance)

        from_uuid = netlist.generate_uid_from_instance_addr_section(from_addr)
        to_uuid = netlist.generate_uid_from_instance_addr_section(to_addr)

        from_uuid_to_uuid[from_uuid] = to_uuid

    # get component positions

    module_super = _get_super()
    kicad_layout = _kicad_project_for_module(module_super)

    from_positions = get_kicad_component_positions(kicad_layout)

    for from_uuid, to_uuid in from_uuid_to_uuid.items():
        from_position = from_positions[from_uuid]
        to_position = from_positions[to_uuid]

        to_position.x = from_position.x + offset_x
        to_position.y = from_position.y + offset_y


def get_kicad_component_positions(file_path: Path) -> list[dict]:
    """
    Parses the .kicad_pcb file data and extracts component information along with the designator.

    Args:
    file_data (str): Contents of the .kicad_pcb file.

    Returns:
    list of dicts: List of components with details (uuid, position, rotation, designator).
    """
    # Regex to match component footprint and extract UUID, position, rotation, and designator
    component_regex = re.compile(
        r'\(footprint\s+"[^"]+"\s+\(layer\s+"[^"]+"\)\s*\(tstamp\s+([^\s]+)\)\s*\(at\s+([0-9.-]+)\s+([0-9.-]+)\s*([0-9.-]*)\).*?\(fp_text\s+reference\s+"([^"]+)"',
        re.MULTILINE | re.DOTALL
    )

    file_data = file_path.read_text()
    components = component_regex.findall(file_data)

    parsed_components = {
        uuid: { 'x': float(x), 'y': float(y), 'rotation': float(rot) if rot else 0.0, 'designator': designator }
        for uuid, x, y, rot, designator in components
    }

    return parsed_components

def set_kicad_component_positions(file_data, updated_components):
    """
    Updates the .kicad_pcb file data with new positions and rotations for components.
    Also updates pad rotations by adding the component's rotation to the original pad rotation.

    Args:
    file_data (str): Original contents of the .kicad_pcb file.
    updated_components (list of dicts): List of components with updated details (uuid, new position, new rotation).

    Returns:
    str: Updated contents of the .kicad_pcb file.
    """
    for component in updated_components:
        uuid = component['uuid']
        new_x = component['x']
        new_y = component['y']
        new_rot = component['rotation']

        # Update the position and rotation of the component in the file data
        file_data = re.sub(
            rf'(\(footprint\s+"[^"]+"\s+\(layer\s+"[^"]+"\)\s*\(tstamp\s+{uuid}\)\s*)\(at\s+([0-9.-]+)\s+([0-9.-]+)\s*([0-9.-]*)\)',
            rf'\1(at {new_x} {new_y} {new_rot})',
            file_data
        )

        # Regex for finding and updating pad rotations
        pad_regex = rf'(\(pad\s+[^\(]*\(at\s+([0-9.-]+)\s+([0-9.-]+)\s*)([0-9.-]+)(\)\s+\(size)'
        def pad_rotation_match(match):
            original_pad_rot = float(match.group(4))
            new_pad_rot = original_pad_rot + new_rot
            return f"{match.group(1)}{new_pad_rot}{match.group(5)}"
        file_data = re.sub(pad_regex, pad_rotation_match, file_data, flags=re.MULTILINE)

    return file_data