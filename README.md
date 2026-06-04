# K2Pus-UNCURSED
UNCURSING your K2+ with config settings and Orca mods.

This is a **STEP-BY-STEP** guide for making Creality K2 Plus less cursed. 

It will:
- Speed up the calibrations.
- Make it perform Adaptive Bed Mesh instead of full Bed Mesh with Orca like it does with Creality Print.
- Heat up the bed BEFORE it probes it, so the taco bed is correctly probed.
- Other improvements.

Require changes to both Orca and the printer configs.  

My setup:  
Orca 2.3.2 RC2  
K2 Plus firmware V1.1.3.13
<br>
<br>
<br>

> [!IMPORTANT]
> There are no backups in this guide, if something goes wrong - it's easier to just factory reset the printer. 

<br>

**!!! DO IT AT YOUR OWN RISK !!!**
<br>
<br>
<br>
<br>







# Orca - Filament settings  
<br>

## Filament start G-code  

> [!TIP]
> Adjust your Z-offset in the last row, search online on how to find your z-offset, it will be different for different filaments
<br>


    ; filament start gcode
    {if (position[2] > first_layer_height) }
    M104 S[nozzle_temperature]
    {else} 
    M104 S[first_layer_temperature]
    {endif}
    SET_GCODE_OFFSET Z=0.088
<br>
<br>

## Filament end G-code  

> [!NOTE]
> Not required, it's just what I use
<br>


    ; filament end gcode 
    SET_GCODE_OFFSET Z=0
<br>
<br>
<br>

# Orca - Printer settings
## Machine G-code
    ; MINX = {first_layer_print_min[0]}
    ; MINY = {first_layer_print_min[1]}
    ; MAXX = {first_layer_print_max[0]}
    ; MAXY = {first_layer_print_max[1]}
    
    M140 S[bed_temperature_initial_layer_single]
    START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single]
    T[initial_no_support_extruder]
    M109 S[nozzle_temperature_initial_layer]
    M204 S2000
    G1 Z3 F600
    M83
    G1 X0 Y150 F12000
    G1 Z0.2 F600
    G1 X0 Y150 F6000
    G1 X0 Y0 E15 F6000
    G1 X150 Y0 E16 F6000
    G92 E0
    G1 Z1 F600


# Install Python if it's not installed on your PC 
Official website https://www.python.org/downloads
<br>
<br>

# Orca - Process panel > Others tab
Once you have Python installed Download [this Orca_fix Python script](Orca_fix.py) and place it in your preferred location

Now paste the corresponding paths into this code

    "path to python.exe" "path to Orca_fix.py";

Here's an **EXAMPLE** of how it should look like

    "C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe" "F:\3D Print\Post-processing scripts\Orca_fix.py";
<br>
<br>

Once you edited it with **YOUR** correct paths - paste it into the **"Post-processing Scripts"** input field in Orca's **Process panel > Others tab**  
<br>

> [!TIP]
> To verify it works - slice something and either send the job or save the G-Code file - it should briefly open a CMD window while the Python script modifies the G-code file.

