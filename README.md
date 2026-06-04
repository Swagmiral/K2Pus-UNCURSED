# K2Pus-UNCURSED
UNCURSING your K2+ with config settings and Orca mods.

This is a step-by-step guide for making Creality K2 Plus less cursed. 

It will:
- Speed up the calibrations.
- Make it perform Adaptive Bed Mesh instead of full Bed Mesh with Orca like it does with Creality Print.
- Heat up the bed BEFORE it probes it, so the taco bed is correctly probed.
- Other improvements.

Require changes to both Orca and the printer configs. 

## Do it step by step!

Save backups of everything you change in Orca.
Do it at your own risk! 

My setup:  
Orca 2.3.2 RC2  
K2 Plus firmware V1.1.3.13

# Orca Filament settings
## Filament start G-code (Adjust your Z-offset in the last row, search online on how to figure out your z-offset, it will be different for different filaments)

    ; filament start gcode
    {if (position[2] > first_layer_height) }
    M104 S[nozzle_temperature]
    {else} 
    M104 S[first_layer_temperature]
    {endif}
    SET_GCODE_OFFSET Z=0.088

##Filament end G-code (Not required, it's just what I use)

    ; filament end gcode 
    SET_GCODE_OFFSET Z=0

# Orca Printer settings
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

  
