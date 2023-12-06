import logging
import os
import sys
from pathlib import Path

import click
import yaml
from caseconverter import kebabcase, pascalcase
from git import InvalidGitRepositoryError, Repo
from .install import add_dependency_to_ato_yaml

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Constants
PROJECT_BASE_URL = "https://gitlab.atopile.io/community-projects"
MODULES_BASE_URL = "https://gitlab.atopile.io/packages"
PROJECT_TEMPLATE_URL = "https://gitlab.atopile.io/atopile/atopile-project-template.git"
MODULES_TEMPLATE_URL = "https://gitlab.atopile.io/packages/module-template.git"
MODULES_DIR = ".ato/modules"

@click.command()
@click.argument("name")
def create(name: str):
    """
    Create a new project or module. If within a repo, creates a module.
    Otherwise, creates a new project.
    """
    project_type, project_path, top_level_dir = determine_project_type_and_path(name)
    clone_project_template(project_type, project_path)

    if project_type == 'module':
        project_path, new_repo_url = init_module(project_path, top_level_dir, name)
    else:
        project_path, new_repo_url = init_project(project_path, top_level_dir, name)

    commit_message = f"Initial commit for {name}"
    commit_and_push_changes(project_path, commit_message)

    push_to_new_repo(project_path, new_repo_url)

    log.info(f"New project created at {PROJECT_BASE_URL}/{name}")

    if project_type == 'module':
        logging.log(msg=f"New module created at {MODULES_BASE_URL}/{name}", level=logging.INFO)
    else:
        logging.log(msg=f"New project created at {PROJECT_BASE_URL}/{name}", level=logging.INFO)

def determine_project_type_and_path(name):
    try:
        repo = Repo(".", search_parent_directories=True)
        top_level_dir = Path(repo.git.rev_parse("--show-toplevel"))
        project_type = 'module'
        project_path = top_level_dir / ".ato" / "modules" / kebabcase(name)
        log.info("Detected existing ato project. Creating a module.")
    except InvalidGitRepositoryError:
        project_type = 'project'
        project_path = Path(kebabcase(name)).resolve()
        top_level_dir = project_path.parent
        log.info("No ato project detected. Creating a new project.")
    return project_type, project_path, top_level_dir

def commit_and_push_changes(repo_path, commit_message):
    repo = Repo(repo_path)
    repo.git.add(A=True)  # Adds all changes to the staging area
    repo.index.commit(commit_message)  # Commits the changes
    repo.git.push()  # Pushes the commit to the remote repository

def clone_project_template(project_type, project_path):
    template_url = MODULES_TEMPLATE_URL if project_type == 'module' else PROJECT_TEMPLATE_URL
    # if project_path.exists():
    #     log.error(f"Directory {project_path} already exists. Aborting.")
    #     sys.exit(1)
    log.info(f"Cloning from {template_url}")
    Repo.clone_from(url=template_url, to_path=project_path)

def init_module(module_path, top_level_dir, name):
    # Module-specific initialization logic
    new_repo_url = f"{MODULES_BASE_URL}/{name}.git"

    # Add dependency to ato.yaml
    add_dependency_to_ato_yaml(top_level_dir, name)

    # Add to projects gitignore
    with open(top_level_dir / '.gitignore', 'a') as gitignore:
        gitignore.write(f'\n{name}/\n')

    return module_path, new_repo_url

def init_project(project_path, top_level_dir, name):
    """
    Initialize a new project.
    """
    project_name = kebabcase(name)

    # Create project directory and any necessary files
    project_path.mkdir(parents=True, exist_ok=True)

    # Rename layout files

    # Mapping of old file names to new file names
    files_to_rename = {
        "atopile-project-template.kicad_pcb": f"{project_name}.kicad_pcb",
        "atopile-project-template.kicad_sch": f"{project_name}.kicad_sch",
        "atopile-project-template.kicad_pro": f"{project_name}.kicad_pro",
        "template_code.ato": f"{project_name}.ato",
    }

    # Walk through all files in the directory and its subdirectories
    for dirpath, dirnames, filenames in os.walk(project_path):
        for filename in filenames:
            if filename in files_to_rename:
                old_path = Path(dirpath) / filename
                new_name = files_to_rename[filename]
                new_path = Path(dirpath) / new_name
                old_path.rename(new_path)
                log.debug(f"Renamed {old_path} to {new_path}")

    kicad_pro_file = project_path / "elec/layout" / f"{project_name}.kicad_pro"
    with open(kicad_pro_file, 'r') as file:
        lines = file.readlines()

    with open(kicad_pro_file, 'w') as file:
        for line in lines:
            if line.strip() == '"netlist": "../../build/default/template_code.net",':
                line = f'      "netlist": "../../build/default/{project_name}.net",\n'
            file.write(line)

    # Create initial files and directories for the project
    # This might include a README, .ato configuration files, etc.
    # Example:
    with open(project_path / "README.md", "w") as file:
        file.write(f"# {project_name}\n")
        file.write("Project description goes here.\n")

    # Return the local path and the URL for the new project repository
    new_repo_url = f"git@gitlab.atopile.io:community-projects/{project_name}.git"

    # Update the ato.yaml file with the new project name
    file_path = project_path / 'ato.yaml'
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    module_name = pascalcase(name)
    data['builds']['default']['entry'] = f'elec/src/{project_name}.ato:{module_name}'

    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)


    return project_path, new_repo_url


def push_to_new_repo(local_repo_path, new_repo_url):
    """
    Push the local project to the new repository using SSH keys.
    """
    try:
        repo = Repo(local_repo_path)
        repo.git.remote("set-url", "origin", new_repo_url)
        current_branch = repo.active_branch.name
        repo.git.push("origin", current_branch, "-u")
        log.info(f"Pushed to new repository: {new_repo_url}")
        return True
    except Exception as e:
        log.error(f"Failed to push to new repository: {e}")
