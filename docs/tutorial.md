# atopile blinky tutorial

Let's setup atopile and create a blinky led project.

# Install atopile

Detailed Installation -> instructions are in the `atopile` project's (README.md)[https://gitlab.atopile.io/atopile/atopile/-/blob/main/README.md?ref_type=heads]

# Project setup

## Forking the template

The (template project)[https://gitlab.atopile.io/atopile/atopile-project-template] contains the base structure for your atopile project. Let's set it up by following those steps:

1) Navigate to the template project: https://gitlab.atopile.io/atopile/atopile-project-template
2) Fork the project
3) Rename the project to `blinky-tutorial`
4) Clone the project locally

## initializing git submodule

The project contains a git submodule with a link to existing modules. We will need to initialize the git submodule. You can do that by running the following commands:

`git submodule init`
`git submodule update --recursive`

If everything went well, the .ato/modules/modules should contain the modules found at https://gitlab.atopile.io/atopile/modules

## setting up `ato.yaml`

The `ato.yaml` file contains the build configuration for the compiler. The entry variable is currently pointing to `elec/src/template_code.ato:HelloWorld`. We will change this to `elec/src/blinky-tutorial.ato:BlinkyTutorial`. In this case `blinky-tutorial.ato` is the file that will contain the ato code and `BlinkyTutorial` is the module we will build. `:` is used to separate between the path outside of a file and inside. Notice that we standardize the module naming to CamelCase to make them easy to spot.

## Setting up the file structure

We previously modified the `ato.yaml` file. We now need to update the file structure to match. Naviate to elec/src and change the `template_code.ato` to `blinky-tutorial.ato`. Next open that same file and rename the module `HelloWorld` to `BlinkyTutorial`.

# Building the project

## Building locally

We are fully setup so let's try building the project: From the project's file root `blinky-tutorial/` run the `ato build` command. If atopile is installed, you should have the following output:

<insert image>

## Building remotely

Now that the project builds locally, let's make sure it builds in the remote repository. Follow those steps:

1) Stage your changes for git (modified `ato.yaml` and renamed `blinky-tutorial.ato` file)
2) Push to gitlab

If everything went well, all build stages should have passed.

<insert image>

# Writing ato code

Everything is setup and we can start writing ato code. First, we will want to import the modules used in this project. Those will be:

- A USB-C connector
- An LED
- A Resistor
- An RP2040 microcontroller
- A 5V to 3.3V LDO

## Importing modules from the library

First, we will import those modules in the current file. We can do this with the following lines of code:

```
# modules
import IndicatorLED from "modules/leds/indicator_led.ato"
import USBC from "modules/connectors/usbc.ato"
import LDOReg3V3 from "modules/regulators/ldo_reg.ato"
import RP2040_kit from "modules/micros/RP2040.ato"
```

Notice that those modules already contain most of the passive components for them to work idependently. For example, the RP2040_kit contains the caps, flash and oscillator. The IndicatorLED contain an LED and a resistor already connected in series.

## Importing interfaces from the library

Second, we will import interfaces in the context of the current file. Interfaces are convenient because they allow you to connect multiple signals together. In this case, we will want to use a `Power` inteface that contains a vcc and gnd signal.

```
# interfaces
import Power from "modules/generics.ato"
```

## Instantiating the modules and interfaces

Let's start by creating an instance of the microcontroller, an instance of the led, a power interface and connecting them together:

```
module BlinkyTutorial:
    power_3v3 = new Power

    microcontroller_kit = new RP2040_kit
    led_indicator = new IndicatorLED

    power_3v3 ~ microcontroller_kit.power

    microcontroller_kit.micro.gpio13 ~ led_indicator.input
    led_indicator.gnd ~ power_3v3.gnd
```

The microcontroller already has a power interface within it. We can connect the `power_3v3` we created directly to it. In the case of the led, we only want to connect to the gnd pin of the power interface. We can do that by specifying the exact pin through `led_indicator.gnd ~ power_3v3.gnd`.

## Building to KiCAD

We have made good progress connecting the elements together. Before continuing, let's try to compile to KiCAD by running the `ato build` command in a terminal rom the project's file root `blinky-tutorial/` like we did previously. This should create a build directory in the in your `blinky-tutorial/` project. In `build/default` you will find a `blinky-tutorial.net` file. This is a netlist that can be ingested into the KiCAD layout interface.

The next step is to open the KiCAD project. Navigate to `elec/layout` and open the `atopile-project-template.kicad_pro` project. Once opened, click on the PCB editor tool. From there, you should find an empty project that looks like this:

<insert image>

To load the netlist, go to file>import>netlist. A pop-up window will open. From there, select the path of the netlist that we just built in `blinky-tutorial/build/default/blinky-tutorial.net`, select the "link footprints using component tstamps (unique ids)" and click "Load and Test Netlist" and then "Update PCB". The components should pop up and look roughly like this:
<insert image>

## Finishing the circuit

To finish the circuit, we will add the usb-c and the low dropout regulator. Notice that the usb-c and the ldo also have a power interface. We will start by creating a second interface called `power_5v` and connecting the usb-c to it. Then we connect the same 5v power interface to a new instance of the ldo. Lastly, we connect the ldo power out interface to the `power_3v3` interface. That's it! Everything is connected.

The code should look like this:

```
# modules
import IndicatorLED from "modules/leds/indicator_led.ato"
import USBC from "modules/connectors/usbc.ato"
import LDOReg3V3 from "modules/regulators/ldo_reg.ato"
import RP2040_kit from "modules/micros/RP2040.ato"

# interfaces
import Power from "modules/generics.ato"

module BlinkyTutorial:
    # instantiate the power interfaces
    power_3v3 = new Power
    power_5v = new Power

    # instantiate the microcontroller and the led
    microcontroller_kit = new RP2040_kit
    led_indicator = new IndicatorLED

    # connect the 3.3v power to the microcontroller
    power_3v3 ~ microcontroller_kit.power

    # connect the led to the microcontroller and to ground
    microcontroller_kit.micro.gpio13 ~ led_indicator.input
    led_indicator.gnd ~ power_3v3.gnd

    # instantiate the usb-c and connect it to 5v power
    usb_c = new USBC
    usb_c.power ~ power_5v

    # instantiate the 3.3v ldo. Connect to power 5v and power 3.3v
    ldo_3v3 = new LDOReg3V3
    ldo_3v3.power_in ~ power_5v
    ldo_3v3.power_out ~ power_3v3

    # done!
```

# 

# Layout in KiCAD

Once again, we can build the project using `ato build` and load it into KiCAD like we did previously. The PCB can be routed as usual.

--> Skiiping to fully routed PCB


# Nice to have

- If you want to access the latest submodule