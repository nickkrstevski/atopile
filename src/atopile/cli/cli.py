import click
from atopile import __version__
from pathlib import Path

@click.group()
@click.version_option(__version__)
def root():
    pass

@root.command()
@click.argument("input")
@click.option("--output")
def build(input, output):
    from atopile.parser.parser import parse_file
    from atopile.netlist.kicad import KicadNetlist

    input_path_str, main_file = input.split(":")
    input_file = Path(input_path_str)
    if not input_file.exists():
        raise click.FileError(input_file, "File does not exist")

    if output is None:
        output_path = input_file.with_suffix(".net")
    else:
        output_path = Path(output)

    if not output_path.is_absolute():
        output_path = output_path.relative_to(input_file)

    if output_path.is_dir():
        output_file = input_file.with_suffix(".net").name
    else:
        output_file = output_path

    model = parse_file(input_file)
    netlist = KicadNetlist.from_model(model, main_file)
    netlist.to_file(output_file)

if __name__ == "__main__":
    root()
