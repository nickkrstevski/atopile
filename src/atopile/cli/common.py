import functools
import logging
import sys
from pathlib import Path

import click

from atopile.project.config import BuildConfig, CustomBuildConfig
from atopile.project.project import Project
from atopile.project.refs import Ref
from atopile.version import check_project_version

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def ingest_config_hat(f):
    # to calculate the config, we need a project and we need them in that order.
    # click doesn't guarentee the order of processing, and it's substantiall up to the user entering the options.
    # since we always need the project to figure out the config, we may as well decorate the command ourselves,
    # process things in the right order and hand them back as kw_args

    @click.argument("source", required=False, default=None)
    @click.option("--build-config", default=None)
    @functools.wraps(f)
    def wrapper(
        *args,
        source: str,
        build_config: str,
        **kwargs,
    ):
        if source:
            root = Ref.from_str(source)
        else:
            root = Ref(Path.cwd())

        try:
            project: Project = Project.from_path(root.to)
        except FileNotFoundError as ex:
            raise click.BadParameter(
                f"Could not find project from path {str(root.to)}. Is this file path within a project?"
            ) from ex

        log.info("Using project %s", project.root)

        if module_path or source_path.is_file():
            root_file_path = project.standardise_import_path(source_path)
            root_node_path = str(root_file_path) + ":" + module_path
        else:
            root_file_path = None
            root_node_path = None

        if build_config is None:
            base_build_config_obj: BuildConfig = project.config.builds["default"]
        else:
            if build_config in project.config.builds:
                base_build_config_obj = project.config.builds[build_config]
            else:
                raise click.BadParameter(
                    f'Could not find build-config "{build_config}".'
                )

        if root_file_path is not None:
            build_config_obj = CustomBuildConfig.from_build_config(
                base_build_config_obj
            )
            build_config_obj.root = (
                (project.root / root_file_path).resolve().absolute()
            )
            if root_node_path is not None:
                build_config_obj.root = root_node_path
        else:
            if root_node_path is not None:
                raise click.BadParameter(
                    "Cannot specify root-node without specifying root-file via positional argument."
                )
            build_config_obj = base_build_config_obj
        log.info("Using build config %s", build_config_obj.name)

        # perform pre-build checks
        if not check_project_version(project):
            sys.exit(1)

        # do the thing
        return f(*args, project, build_config_obj, **kwargs)

    return wrapper
