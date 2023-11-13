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
from atopile.dev.parse import parse_file
from atopile.dev.dm1_vis import Wendy

dizzy = Dizzy("test.ato")
tree = dizzy.visitFile_input(parse_file(ato))

wendy = Wendy()
wendy.print_tree(tree)
