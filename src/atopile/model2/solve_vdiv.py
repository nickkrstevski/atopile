from typing import Any, Iterable, Mapping, Optional, Type

from .datamodel import Instance
from .instance_methods import match_modules, dfs
from atopile.model2.datatypes import Ref
from atopile.model2.object_methods import iter_supers
from sympy import symbols, Eq, solve, Float, Integer
import eseries


R1, R2, Vin, Vout, I, r_total = symbols('R1 R2 Vin Vout I r_total')

# Define the equations
equation1 = Eq(Vout, Vin * (R2 / (R1 + R2)))
equation2 = Eq(I, Vin / (R1 + R2))
equation3 = Eq(r_total, R1 + R2)

# Function to solve the equations based on specified values
def solve_circuit(values):
    substituted_eqs = [eq.subs(values) for eq in [equation1, equation2, equation3]]

    # Determine which variables are still unknown
    unknowns = [var for var in [R1, R2, Vin, Vout, I, r_total] if var not in values]

    # Solve the equations for the unknowns
    solutions = solve(substituted_eqs, unknowns)

    # Check the type of the solution and convert to dictionary if necessary
    if isinstance(solutions, list):
        # Assuming only one solution set in the list
        solution_dict = {unknown: sol for unknown, sol in zip(unknowns, solutions[0])}
    else:
        # Solution is already a dictionary
        solution_dict = solutions

    return solution_dict

def suggest_eseries(value):
    # Find the nearest E24 values
    return eseries.find_nearest(eseries.E24, value)


def solve_vdivs(root: Instance) -> Instance:
    """Solve the values of the resistor in the vdiv."""
    # Define all symbols
    instances = list(filter(match_modules, dfs(root)))

    regulator_ref = Ref((('Regulator',),))
    # First pass to find used designators
    for instance in instances:
        for super_ref in instance.origin.supers_refs:
            for _super in iter_supers(instance.origin):
                if _super.supers_refs == regulator_ref:
                    vdiv_instance = instance.children.get("feedback_vdiv")
                    res_total = vdiv_instance.children.get("r_total", "unknown")

                    r_top_intance = vdiv_instance.children.get("r_top")
                    r_bottom_intance = vdiv_instance.children.get("r_bottom")

                    r_top_value = r_top_intance.children.get("value", "unknown")
                    r_bottom_value = r_bottom_intance.children.get("value", "unknown")

                    in_instance = instance.children.get("v_out")
                    out_instance = instance.children.get("v_fb")

                    in_voltage = in_instance.children.get("voltage", "unknown")
                    out_voltage = out_instance.children.get("voltage", "unknown")

                    output_values = {}

                    output_values[R1] = r_top_value
                    output_values[R2] = r_bottom_value
                    output_values[r_total] = res_total
                    output_values[Vin] = in_voltage
                    output_values[Vout] = out_voltage

                    input_values = {}
                    for value_key, value in output_values.items():
                        if value is not "unknown":
                            input_values[value_key] = value
                    output_values.update(solve_circuit(input_values))

                    if (isinstance(output_values[R1], Integer) or isinstance(output_values[R1], Float)) and (isinstance(output_values[R2], Integer) or isinstance(output_values[R1], Float)):
                        r_top_intance.children["value"] = suggest_eseries(output_values[R1])
                        r_bottom_intance.children["value"] = suggest_eseries(output_values[R2])
                    else:
                        print('could not resolve value of r_top, r_bottom')
                        r_top_intance.children["value"] = 0
                        r_bottom_intance.children["value"] = 0

