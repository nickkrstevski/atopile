#%%
%load_ext autoreload
%autoreload 2
from atopile.parser.parser import build_model
from atopile.project.config import BuildConfig, CustomBuildConfig
from atopile.project.project import Project
from pathlib import Path
import logging

#%%
logging.basicConfig(level=logging.DEBUG)

# %%
project_root = Path("/Users/mattwildoer/Projects/atopile-workspace")
project = Project.from_path(project_root)
build_config = CustomBuildConfig(
    "default",
    project,
    project_root / "servo-drive/elec/src/spin_servo_nema17.ato",
    "servo-drive/elec/src/spin_servo_nema17.ato:SpinServoNEMA17",
    []
)

#%%
model = build_model(project, build_config)

# %%
from atopile.targets.bom.bom_jlcpcb import BomJlcpcbTarget
from atopile.targets.targets import TargetMuster

#%%
muster = TargetMuster(project, model, build_config)
bom_target = BomJlcpcbTarget(muster)
bom_target.generate()

#%%
bom_target.