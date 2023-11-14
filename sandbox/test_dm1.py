#%%
ato ="""
import bloop from "bloorp.ato"
module ESP32:
    interface power:
        signal vcc
        signal gnd
    interface i2c:
        signal scl
        signal sda
    interface spi:
        signal sclk
        signal mosi
        signal miso
        signal cs
    signal gpio0
    signal gpio1
    signal gpio2
module IMU:
    interface power:
        signal vcc
        signal gnd
    interface i2c:
        signal scl
        signal sda
module Button:
    signal gnd
    signal output
module sensor:
    esp32 = new ESP32
    imu = new IMU
    ESP32 -> imu
    esp32.power ~ sensor.power
    btn = new Button
    btn.gnd ~ sensor.power.gnd
    btn.output ~ sensor.gpio0
"""
test = """
    esp32.i2c ~ sensor.i2c
"""

from atopile.model2.datamodel1 import Dizzy
from atopile.dev.parse import parse_as_file
from atopile.dev.dm1_vis import Wendy

dizzy = Dizzy("test.ato")
tree = dizzy.visitFile_input(parse_as_file(ato))

wendy = Wendy()
wendy.print_tree(tree)

#%%
from atopile.deps import PathFinder
from pathlib import Path
from atopile.model2.parse import parse


# %%
# %%from pathlib import Path

# Create a Path object for the directory
servo_path = Path("/Users/narayanpowderly/Documents/atopile-workspace/servo-drive/elec/src")

# Call the glob() method with the pattern "**/*.ato"
ato_files = servo_path.glob("**/*.ato")

# Iterate over the returned generator and process each file
for ato_file in ato_files:
    print(str(ato_file))  # Replace this with your parsing code
    # print the contents of the file
    with open(ato_file) as f:
        print(f.read())

# %%
dizzy = Dizzy("test.ato")
ato = ato_files #take first file
tree = dizzy.visitFile_input(parse_as_file(ato))
wendy = Wendy()
wendy.print_tree(tree)


# %%
from pathlib import Path
import itertools

# Create a Path object for the directory
servo_path = Path("/Users/narayanpowderly/Documents/atopile-workspace/servo-drive/elec/src")

# Call the glob() method with the pattern "**/*.ato"
ato_files = servo_path.glob("**/*.ato")

# Create a Dizzy and Wendy instance
dizzy = Dizzy("test.ato")
wendy = Wendy()

# Define the index of the file you want
n = 1  # Change this to get a different file

# Get the nth file from the generator
ato_file = next(itertools.islice(ato_files, n, None))

# Print the file path
print(ato_file)

# Read the file contents
file_contents = ato_file.read_text()

# Print the file contents
print(file_contents)

# Process the file contents with your Dizzy and Wendy instances
tree = dizzy.visitFile_input(parse_as_file(file_contents))
wendy.print_tree(tree)
# %%
