# %%
import sympy

from numbers import Number
from typing import Iterable, Optional, Callable

from atopile import address, errors, instance_methods
from atopile.address import AddrStr
from atopile.front_end import Physical  # FIXME: this doesn't belong here


# %%

class _MockInstance:
    """
    This exists because the variables are dot-accessed in equations,
    and we need to put something in place for the objects on path,
    except the final variable.
    """

    def __init__(
        self,
        mocking: AddrStr,
        eqn_builder: "EquationBuilder"
    ) -> None:
        self.mocking = mocking
        self.eqn_builder = eqn_builder

    def __getattr__(self, key):
        abs_addr = address.add_instance(self.mocking, key)
        if abs_addr in self.eqn_builder.mock_instances:
            return self.eqn_builder.mock_instances[abs_addr]

        if abs_addr in self.eqn_builder.symbols:
            return self.eqn_builder.symbols[key]

        if phys := instance_methods.get_data_dict(self.mocking).get(key):
            if isinstance(phys, Physical):
                new_symbol = sympy.Symbol(abs_addr.replace(".", "_"), real=True)
                self.eqn_builder.symbols[abs_addr] = new_symbol
                return new_symbol

            raise errors.AtoTypeError(f"Cannot use {phys} in equations", addr=abs_addr)

        return super().__getattribute__(key)


class EquationBuilder:
    """This guy builds equations."""
    def __init__(self) -> None:
        self._entry: Optional[str] = None
        self.mock_instances: dict[AddrStr, _MockInstance] = {}
        self.symbols: dict[AddrStr, sympy.Symbol] = {}
        self.equations: list[sympy.Eq] = []

    def _visit_instance(self, instance: AddrStr) -> None:
        """
        Create a mock instance object; a thin wrapper upon the
        instance tree so we can readily parse variables from it.

        This is a recursive function that registers the mock instances
        withing the EquationBuilder.
        """
        local_symbols = {
            child_name: self._visit_instance(child_addr)
            for child_name, child_addr in instance_methods.get_children_items(instance)
        }

        self.mock_instances[instance] = _MockInstance(instance, self)

        for equation in instance_methods.get_equations(instance):
            eqn = sympy.sympify(equation, evaluate=False, locals=local_symbols)
            self.equations.append(eqn)
            assert isinstance(eqn, sympy.Eq)
            assert eqn.free_symbols.issubset(
                self.symbols.values()
            ), "equation contains unknown symbols"

    def build(self, root: AddrStr) -> None:
        """Build equations for a given root."""
        if self._entry is None:
            self._entry = address.get_entry(root)
        elif address.get_entry(root) != self._entry:
            raise ValueError("EquationBuilder only supports one entry point")

        # build the mock instance tree
        self._visit_instance(root)

    def lambdify_for(
        self, solve_for: AddrStr
    ) -> Callable[[], Number]:
        """Solve the equation set for everything we can, given a set of known values."""
        solutions = sympy.solve(self.equations, self.symbols[solve_for], dict=True)

        # Check the type of the solution and convert to dictionary if necessary
        if isinstance(solutions, list):
            # Assuming only one solution set in the list
            solution_dict = {
                unknown: sol for unknown, sol in zip(solve_for_symbols, solutions[0])
            }
        else:
            # Solution is already a dictionary
            solution_dict = solutions

        return {
            addr: float(solution_dict[sym])
            for addr, sym in solution_dict.items()
            if isinstance(solution_dict[sym], Number)
        }

# %%
x = sympy.Symbol("x")
y = sympy.Symbol("y")
z = sympy.Symbol("z")

# unused - here for the ride
a = sympy.Symbol("a")
b = sympy.Symbol("b")

all_symbols = [x, y, z, a, b]

# %%
eq = sympy.Eq(x, y + z)
# %%
solutions = sympy.solve(eq, x, dict=True)
assert len(solutions) == 1
assert len(solutions[0]) == 1
expr = list(solutions[0].values())[0]
func = sympy.lambdify(all_symbols, expr, "numpy")
# %%
func(1, 2, 3, 4, 5)
# %%
