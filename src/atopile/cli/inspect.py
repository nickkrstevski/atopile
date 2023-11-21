import logging
from typing import Iterable

import click
import numpy as np
import pandas as pd
import uvicorn
from rich.console import Console
from rich.table import Table, Column

from atopile.cli.common import ingest_config_hat
from atopile.model.accessors import ModelVertexView
from atopile.model.model import EdgeType, VertexType
from atopile.parser.parser import build_model
from atopile.project.config import BuildConfig
from atopile.project.project import Project

# configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class DisplayPin:
    def __init__(self, pin_mvv) -> None:
        self.is_displayed = True
        self.mvv = pin_mvv
        self.associated_pin = []
        self.associated_signal = []
        self.associated_interface = []
        self.cons_by_pin = []
        self.cons_by_signal = []
        self.cons_by_intf = []

def make_list_friendly(things: Iterable[ModelVertexView], type: str = 'ref') -> str:
    if type == 'ref':
        return ", ".join(thing.ref for thing in things)
    else:
        return ", ".join(thing.class_path for thing in things)


# configure UI
@click.command()
@ingest_config_hat
@click.option("--debug/--no-debug", default=False)
def inspect(
    project: Project, build_config: BuildConfig, debug: bool
):
    """
    Inspect the available pins of a component within the context of a module
    eg. `ato inspect path/to/source.ato:module.path`
    """

    if debug:
        # FIXME: Do we need this?
        import atopile.parser.parser

        atopile.parser.parser.log.setLevel(logging.DEBUG)

    # build core model
    model = build_model(project, build_config)
    print(project.module_dir)
    # Putting this as a trial
    root_node = "buck_reg.ato:BuckReg.buck_converter"
    root_mvv = ModelVertexView.from_path(model, root_node)
    return_list = root_mvv.get_adjacents("in", EdgeType.part_of)

    # we start by creating a list of connections between of connection pairs
    # between pins, signals and interfaces on the selected component or module
    available_list: Iterable[tuple[ModelVertexView, ModelVertexView]] = []
    for element in return_list:
        available_list.append((element, None))
        pin_adjacents = list(element.get_adjacents_with_edge_types("in", EdgeType.connects_to)) + list(element.get_adjacents_with_edge_types("out", EdgeType.connects_to))
        for pin_adjacent in pin_adjacents:
            if element.parent == pin_adjacent[1].parent:
                available_list.append((element, pin_adjacent[1]))

    # we then create an equivalent list of pairs between the pins and signals of the component
    # and the element from neighboring components. modules and interfaces that are connected to it
    consumed_list: Iterable[tuple[ModelVertexView, ModelVertexView]] = []
    for element in return_list:
        pin_adjacents = list(element.get_adjacents_with_edge_types("in", EdgeType.connects_to)) + list(element.get_adjacents_with_edge_types("out", EdgeType.connects_to))
        for pin_adjacent in pin_adjacents:
            if element.parent != pin_adjacent[1].parent:
                consumed_list.append((element, pin_adjacent[1]))

    # we now create a list of object that will represent a pin and the elements associated with it
    displayed_pins: Iterable[DisplayPin] = []
    for element in available_list:
        # pins look like this within the available_list: (pin, None)
        if not element[1] and element[0].vertex_type == VertexType.pin:
            displayed_pins.append(DisplayPin(element[0]))

    #TODO: the mechanism is broken for interfaces and will have to be fixed
    # now that the element is created, we add associated element to it
    for display_pin in displayed_pins:
        for element in available_list:
            # pins look like this within the available_list: (pin, None), they should be discarded
            if element[1] and display_pin.mvv.ref == element[0].ref:
                if element[1].vertex_type == VertexType.pin:
                    display_pin.associated_pin.append(element[1])
                elif element[1].vertex_type == VertexType.signal: # This will probs not work for interface, since they are defined a layer deeper in the graph
                    display_pin.associated_signal.append(element[1])
                elif element[1].vertex_type == VertexType.interface:
                    display_pin.associated_interface.append(element[1])

    # we now add the element that are consuming each pin
    for display_pin in displayed_pins:
        for consumer in consumed_list:
            if consumer[0].ref == display_pin.mvv.ref:
                if consumer[1].vertex_type == VertexType.pin:
                    display_pin.cons_by_pin.append(consumer[1])
                elif consumer[1].vertex_type == VertexType.signal: # This will probs not work for interface, since they are defined a layer deeper in the graph
                    display_pin.cons_by_signal.append(consumer[1])
                elif consumer[1].vertex_type == VertexType.interface:
                    display_pin.cons_by_intf.append(consumer[1])
            for signal in display_pin.associated_signal:
                if consumer[0].ref == signal.ref:
                    if consumer[1].vertex_type == VertexType.pin:
                        display_pin.cons_by_pin.append(consumer[1])
                    elif consumer[1].vertex_type == VertexType.signal: # This will probs not work for interface, since they are defined a layer deeper in the graph
                        display_pin.cons_by_signal.append(consumer[1])
                    elif consumer[1].vertex_type == VertexType.interface:
                        display_pin.cons_by_intf.append(consumer[1])
            for interface in display_pin.associated_interface:
                if consumer[0].ref == interface.ref:
                    if consumer[1].vertex_type == VertexType.pin:
                        display_pin.cons_by_pin.append(consumer[1])
                    elif consumer[1].vertex_type == VertexType.signal: # This will probs not work for interface, since they are defined a layer deeper in the graph
                        display_pin.cons_by_signal.append(consumer[1])
                    elif consumer[1].vertex_type == VertexType.interface:
                        display_pin.cons_by_intf.append(consumer[1])


    # a rich table is create
    table = Table(
        Column(header="Pin#", justify="right"),
        Column(header="Signals", justify="left"),
        Column(header="Interface", justify="right"),
        Column(header="Consumed by pin", justify="right"),
        Column(header="Consumed by signal", justify="right"),
        Column(header="Consumed by intf", justify="right"),
        title="Available pins on " + root_node
    )

    for display_pin in displayed_pins:
        table.add_row(
            display_pin.mvv.ref,
            make_list_friendly(display_pin.associated_signal),
            make_list_friendly(display_pin.associated_interface),
            make_list_friendly(display_pin.cons_by_pin, 'class'),
            make_list_friendly(display_pin.cons_by_signal, 'class'),
            make_list_friendly(display_pin.cons_by_intf, 'class'))

    # the table is displayed
    console = Console()
    console.print(table)
