# Global imports
import argparse
import logging
import os
import re
import sys
from textwrap import dedent
from typing import List

from easyeda2kicad import __version__
from easyeda2kicad.easyeda.easyeda_api import EasyedaApi
from easyeda2kicad.easyeda.easyeda_importer import (
    Easyeda3dModelImporter,
    EasyedaFootprintImporter,
    EasyedaSymbolImporter,
)
from easyeda2kicad.easyeda.parameters_easyeda import EeSymbol
from easyeda2kicad.helpers import (
    add_component_in_symbol_lib_file,
    id_already_in_symbol_lib,
    set_logger,
    update_component_in_symbol_lib_file,
)
from easyeda2kicad.kicad.export_kicad_3d_model import Exporter3dModelKicad
from easyeda2kicad.kicad.export_kicad_footprint import ExporterFootprintKicad
from easyeda2kicad.kicad.export_kicad_symbol import ExporterSymbolKicad
from easyeda2kicad.kicad.parameters_kicad_symbol import KicadVersion
from atopile.asset_manager.easyeda2ato import ExporterAto


def delete_component_in_symbol_lib(
    lib_path: str, component_id: str, component_name: str
) -> None:
    with open(file=lib_path, encoding="utf-8") as f:
        current_lib = f.read()
        new_data = re.sub(
            rf'(#\n# {component_name}\n#\n.*?F6 "{component_id}".*?ENDDEF\n)',
            "",
            current_lib,
            flags=re.DOTALL,
        )

    with open(file=lib_path, mode="w", encoding="utf-8") as my_lib:
        my_lib.write(new_data)


def fp_already_in_footprint_lib(lib_path: str, package_name: str) -> bool:
    if os.path.isfile(f"{lib_path}/{package_name}.kicad_mod"):
        logging.warning(f"The footprint for this id is already in {lib_path}")
        return True
    return False


def main(argv: List[str] = sys.argv[1:]) -> int:
    print(f"-- easyeda2kicad.py v{__version__} --")

    # cli interface
    parser = get_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code
    arguments = vars(args)

    if arguments["debug"]:
        set_logger(log_file=None, log_level=logging.DEBUG)
    else:
        set_logger(log_file=None, log_level=logging.INFO)

    if not valid_arguments(arguments=arguments):
        return 1

    # conf = get_local_config()

    component_id = arguments["lcsc_id"]
    kicad_version = arguments["kicad_version"]
    sym_lib_ext = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"

    # Get CAD data of the component using easyeda API
    api = EasyedaApi()
    cad_data = api.get_cad_data_of_component(lcsc_id=component_id)

    # API returned no data
    if not cad_data:
        logging.error(f"Failed to fetch data from EasyEDA API for part {component_id}")
        return 1


    # ---------------- ATOPILE ----------------
    if arguments["ato"]:
        importer = EasyedaSymbolImporter(easyeda_cp_cad_data=cad_data)
        easyeda_symbol: EeSymbol = importer.get_symbol()
        # print(easyeda_symbol)
        component_name=easyeda_symbol.info.name
        ato_full_path = f"{arguments['output']}/{component_name}.ato"
        is_ato_already_in_lib_folder = os.path.isfile(ato_full_path)

        if not arguments["overwrite"] and is_ato_already_in_lib_folder:
            logging.error("Use --overwrite to update the older ato file")
            return 1
        
        footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=cad_data)
        easyeda_footprint = footprint_importer.get_footprint()
        package_name=easyeda_footprint.info.name

        exporter = ExporterAto(
            symbol = easyeda_symbol,
            component_id = component_id,
            component_name = component_name,
            footprint = package_name
        )
        # print(exporter.output)
        exporter.export(
            ato_full_path = ato_full_path
        )


        logging.info(
            f"Created Atopile file for ID : {component_id}\n"
            f"       Symbol name : {easyeda_symbol.info.name}\n"
            f"       Library path : {ato_full_path}"
        )


    # ---------------- SYMBOL ----------------
    if arguments["symbol"]:
        importer = EasyedaSymbolImporter(easyeda_cp_cad_data=cad_data)
        easyeda_symbol: EeSymbol = importer.get_symbol()
        # print(easyeda_symbol)

        is_id_already_in_symbol_lib = id_already_in_symbol_lib(
            lib_path=f"{arguments['output']}.{sym_lib_ext}",
            component_name=easyeda_symbol.info.name,
            kicad_version=kicad_version,
        )

        if not arguments["overwrite"] and is_id_already_in_symbol_lib:
            logging.error("Use --overwrite to update the older symbol lib")
            return 1

        exporter = ExporterSymbolKicad(
            symbol=easyeda_symbol, kicad_version=kicad_version
        )
        # print(exporter.output)
        kicad_symbol_lib = exporter.export(
            footprint_lib_name=arguments["output"].split("/")[-1].split(".")[0],
        )

        if is_id_already_in_symbol_lib:
            update_component_in_symbol_lib_file(
                lib_path=f"{arguments['output']}.{sym_lib_ext}",
                component_name=easyeda_symbol.info.name,
                component_content=kicad_symbol_lib,
                kicad_version=kicad_version,
            )
        else:
            add_component_in_symbol_lib_file(
                lib_path=f"{arguments['output']}.{sym_lib_ext}",
                component_content=kicad_symbol_lib,
                kicad_version=kicad_version,
            )

        logging.info(
            f"Created Kicad symbol for ID : {component_id}\n"
            f"       Symbol name : {easyeda_symbol.info.name}\n"
            f"       Library path : {arguments['output']}.{sym_lib_ext}"
        )

    # ---------------- FOOTPRINT ----------------
    if arguments["footprint"]:
        importer = EasyedaFootprintImporter(easyeda_cp_cad_data=cad_data)
        easyeda_footprint = importer.get_footprint()

        is_id_already_in_footprint_lib = fp_already_in_footprint_lib(
            lib_path=f"{arguments['output']}.pretty",
            package_name=easyeda_footprint.info.name,
        )
        if not arguments["overwrite"] and is_id_already_in_footprint_lib:
            logging.error("Use --overwrite to replace the older footprint lib")
            return 1

        ki_footprint = ExporterFootprintKicad(footprint=easyeda_footprint)
        footprint_filename = f"{easyeda_footprint.info.name}.kicad_mod"
        footprint_path = f"{arguments['output']}.pretty"
        model_3d_path = f"{arguments['output']}.3dshapes".replace("\\", "/").replace(
            "./", "/"
        )

        if arguments.get("use_default_folder"):
            model_3d_path = "${EASYEDA2KICAD}/easyeda2kicad.3dshapes"
        if arguments["project_relative"]:
            model_3d_path = "${KIPRJMOD}" + model_3d_path

        ki_footprint.export(
            footprint_full_path=f"{footprint_path}/{footprint_filename}",
            model_3d_path=model_3d_path,
        )

        logging.info(
            f"Created Kicad footprint for ID: {component_id}\n"
            f"       Footprint name: {easyeda_footprint.info.name}\n"
            f"       Footprint path: {os.path.join(footprint_path, footprint_filename)}"
        )

    # ---------------- 3D MODEL ----------------
    if arguments["3d"]:
        exporter = Exporter3dModelKicad(
            model_3d=Easyeda3dModelImporter(
                easyeda_cp_cad_data=cad_data, download_raw_3d_model=True
            ).output
        )
        exporter.export(lib_path=arguments["output"])
        if exporter.output:
            filename = f"{exporter.output.name}.wrl"
            lib_path = f"{arguments['output']}.3dshapes"

            logging.info(
                f"Created 3D model for ID: {component_id}\n"
                f"       3D model name: {exporter.output.name}\n"
                f"       3D model path: {os.path.join(lib_path, filename)}"
            )

        # logging.info(f"3D model: {os.path.join(lib_path, filename)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
