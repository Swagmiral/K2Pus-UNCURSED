# K2Pus-UNCURSED

This is a **STEP-BY-STEP** guide for making Creality K2 Plus less cursed.  

It will:
- Speed up the calibrations.
- Make it perform Adaptive Bed Mesh instead of full Bed Mesh with Orca like it does with Creality Print.
- Heat up the bed BEFORE it probes it, so the taco bed is correctly probed.
- Other improvements.

Requires changes to both Orca and the printer configs.  

My setup:  
- Windows 11  
- Orca 2.3.2 RC2  
- K2 Plus firmware V1.1.3.13
<br>
<br>

> [!IMPORTANT]
> There are no backups in this guide, if something goes wrong - it's easier to just factory reset the printer. 
<br>

> [!IMPORTANT]
> <img width="118" height="118" alt="image" src="https://github.com/user-attachments/assets/f694e290-e68e-40fc-a62c-1241ab23725c" />  
> Use this button to copy all the code and commands from this guide, don't try copying it by selecting the text as it will break formatting.
<br>
<br>
<br>




### <p align="center"> !!! DO EVERYTHING AT YOUR OWN RISK !!!

</p>

<br>
<br>
<br>
<br>







# <p align="center"> Orca - Filament settings  
</p>
<br>

### Filament start G-code  
<br>

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

### Filament end G-code  
<br>

> [!NOTE]
> Not required, it's just what I use
<br>


    ; filament end gcode 
    SET_GCODE_OFFSET Z=0
<br>
<br>
<br>

# <p align="center"> Orca - Printer settings
</p>

### Machine G-code
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


# <p align="center"> Install Python if it's not installed on your PC 
Official website https://www.python.org/downloads  
<br>
Once Python is installed download [this Orca_fix Python script](Orca_fix.py) and place it in your preferred location


<br>

# <p align="center"> Orca - Process panel > Others tab
> [!IMPORTANT]
> Enable Developer mode in Orca Preferences.

<br>

Now paste the corresponding paths into this code

    "path to python.exe" "path to Orca_fix.py";
<br>

Here's an **EXAMPLE** of how it should look like

    "C:\Users\USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe" "F:\3D Print\Post-processing scripts\Orca_fix.py";
<br>
<br>

Once you edited it with **YOUR** correct paths - paste it into the **"Post-processing Scripts"** input field in Orca's **Process panel > Others tab**  
<br>

> [!TIP]
> To verify it works - slice something and either send the job or save the G-Code file - it should briefly open a CMD window while the Python script modifies the G-code file.  
<br>
<br>
<br>

# Printer configuration through SSH  
<br>

Enter SSH using command line (CMD or Command Prompt on Windows).
Replace the IP with **YOUR** printer's IP  

    ssh root@192.168.50.130

Enter password  

    creality_2024

In case of an error remove the old SSH (make sure the IP is correct)  

    ssh-keygen -R 192.168.50.130
<br>
<br>

> [!TIP]
> You can full reset the firmware to the factory settings in case you fucked something up

    echo "all" | /usr/bin/nc -U /var/run/wipe.sock
<br>

> [!TIP]
> If you fucked something up so bad the previous command doesn't work, follow this guide to reflash the firmware https://youtu.be/LVTEGkVRSwY
<br>
<br>

### Make printer always take bed temperature from the slicer for the calibrations before printing  
<br>

1. Check default bed temp (default is set to 50 С)  

        grep "default_bed_temp" /mnt/UDISK/printer_data/config/printer_params.cfg

2. Check default bed temp again (default is set to 50 С) (?)  

        grep "default_bed_temp" /usr/share/klipper/config/F008_CR0CN240319C13_1/printer_params.cfg

1. Set it to >15 С so it always takes it from the slicer.

        sed -i 's/default_bed_temp: 50/default_bed_temp: 15/' /mnt/UDISK/printer_data/config/printer_params.cfg

2. Set it to >15 С so it always takes it from the slicer (default backup?) (?)

        sed -i 's/default_bed_temp: 50/default_bed_temp: 15/' /usr/share/klipper/config/F008_CR0CN240319C13_1/printer_params.cfg

1. Check it again (should now be 15 С)

        grep "default_bed_temp" /mnt/UDISK/printer_data/config/printer_params.cfg

2. Check it again (should now be 15 С) (?)

        grep "default_bed_temp" /usr/share/klipper/config/F008_CR0CN240319C13_1/printer_params.cfg

<br>

### Always heat up the bed to the target temp before calibration
    sed -i 's/if target_temp > default_bed_temp:/if target_temp > 0:/' /usr/share/klipper/klippy/extras/virtual_sdcard.py

### Take bed temp from the first bed temp found in the gcode file before the calibrations start

    cat > /tmp/patch_bed_temp.py << 'EOF'
    path = "/usr/share/klipper/klippy/extras/virtual_sdcard.py"
    
    old = (
        "            try:\n"
        "                # 当前目标温度大于热床调平时的默认温度时,用当前目标温度调平\n"
        "                custom_macro = self.printer.lookup_object('custom_macro')\n"
        "                heater_bed = self.printer.lookup_object('heater_bed').heater\n"
        "                target_temp = heater_bed.target_temp\n"
        "                default_bed_temp = custom_macro.default_bed_temp\n"
        "                if target_temp > 0:\n"
        "                    cmd += \" BED_TEMP=%s\" % target_temp\n"
        "            except Exception as err:\n"
        "                logging.exception(\"run_bed_mesh_calibate error: %s\" % err)\n"
    )
    
    new = (
        "            try:\n"
        "                bed_temp = 0\n"
        "                with open(self.current_file.name, \"r\") as gf:\n"
        "                    for line in gf:\n"
        "                        if line.startswith(\"M140 S\"):\n"
        "                            bed_temp = int(float(line.strip().split(\"S\")[1].split()[0]))\n"
        "                            break\n"
        "                if bed_temp > 0:\n"
        "                    cmd += \" BED_TEMP=%s\" % bed_temp\n"
        "            except Exception as err:\n"
        "                logging.exception(\"bed_temp parse error: %s\" % err)\n"
    )
    
    with open(path, "r") as f:
        content = f.read()
    
    count = content.count(old)
    print("Found %d occurrences" % count)
    if count != 1:
        print("ERROR")
        exit(1)
    
    content = content.replace(old, new)
    
    with open(path, "w") as f:
        f.write(content)
    print("Done")
    EOF
    python3 /tmp/patch_bed_temp.py

<br>

### Start chamber heater before calibrations and turn off fans if the chamber heating is on

    cat > /tmp/patch_macro.py << 'EOF'
    path = "/mnt/UDISK/printer_data/config/gcode_macro.cfg"
    
    target = "  M140 S{bed_temp}  # 50\n"
    insert = (
        "  {% if 'CHAMBER_TEMP' in params|upper and params.CHAMBER_TEMP|default(0)|int > 0 %}\n"
        "    SET_TEMPERATURE_FAN_SWITCH TEMPERATURE_FAN=chamber_fan VALUE=0\n"
        "    M141 S{params.CHAMBER_TEMP}\n"
        "  {% endif %}\n"
    )
    
    with open(path, "r") as f:
        content = f.read()
    
    count = content.count(target)
    print("Found %d occurrences" % count)
    
    if count != 1:
        print("ERROR: expected 1, got %d" % count)
        exit(1)
    
    content = content.replace(target, target + insert)
    
    with open(path, "w") as f:
        f.write(content)
    
    print("Done")
    EOF
    python3 /tmp/patch_macro.py

<br>

### Take chamber temp from the first s191 found instead of the ones at the file end

    cat > /tmp/patch_chamber.py << 'EOF'
    path = "/usr/share/klipper/klippy/extras/virtual_sdcard.py"
    
    old = (
        "            try:\n"
        "                chamber_temp = 0\n"
        "                with open(self.current_file.name, \"r\") as gf:\n"
        "                    for line in gf:\n"
        "                        if line.startswith(\"; chamber_temperature\"):\n"
        "                            temps = line.split(\"=\")[1].strip().split(\",\")\n"
        "                            for t in temps:\n"
        "                                v = float(t.strip())\n"
        "                                chamber_temp = max(chamber_temp, int(v))\n"
        "                            break\n"
        "                if chamber_temp > 0:\n"
        "                    cmd += \" CHAMBER_TEMP=%s\" % chamber_temp\n"
        "            except Exception as err:\n"
        "                logging.exception(\"chamber_temp parse error: %s\" % err)\n"
    )
    
    new = (
        "            try:\n"
        "                chamber_temp = 0\n"
        "                with open(self.current_file.name, \"r\") as gf:\n"
        "                    for line in gf:\n"
        "                        if line.startswith(\"M191 S\"):\n"
        "                            chamber_temp = int(float(line.strip().split(\"S\")[1].split()[0]))\n"
        "                            break\n"
        "                if chamber_temp > 0:\n"
        "                    cmd += \" CHAMBER_TEMP=%s\" % chamber_temp\n"
        "            except Exception as err:\n"
        "                logging.exception(\"chamber_temp parse error: %s\" % err)\n"
    )
    
    with open(path, "r") as f:
        content = f.read()
    
    count = content.count(old)
    print("Found %d occurrences" % count)
    if count != 1:
        print("ERROR")
        exit(1)
    
    content = content.replace(old, new)
    
    with open(path, "w") as f:
        f.write(content)
    print("Done")
    EOF
    python3 /tmp/patch_chamber.py

<br>

### Reduce bed temp hysteresis from 10C to 5C (optional)

    sed -i '/\[verify_heater heater_bed\]/,/\[/{s/^hysteresis: 10$/hysteresis: 5/}' /mnt/UDISK/printer_data/config/printer.cfg

<br>

### **Speed up Bed mesh**  

Speed 700 (default 100), probe count 9x9, raise between probes to 3mm (default 5), speed up z homing

    F=/mnt/UDISK/printer_data/config/printer.cfg; echo -e "\033[33m=== Before ===\033[0m" && sed -n '/^\[printer\]/,/^\[/{/max_z_velocity/p}' $F && sed -n '/^\[prtouch_v3\]/,/^\[/{/lift_speed/p}' $F && sed -n '/^\[z_align\]/,/^\[/{/distance_ratio\|quick_speed\|^retries:/p}' $F && sed -n '/^\[bed_mesh\]/,/^\[/{/^speed:\|^probe_count\|^horizontal_move_z/p}' $F && sed -i '
    /\[z_align\]/,/^\[/{s/^distance_ratio:.*/distance_ratio: 0.9  # fast move distance ratio/;s/^quick_speed:.*/quick_speed: 50 # mm\/s  nozzle descent speed/;s/^retries:.*/retries: 4/}
    /^\[printer\]/,/^\[/ s/^max_z_velocity:.*/max_z_velocity: 50/
    /^\[prtouch_v3\]/,/^\[/ {/^lift_speed/d; s/^speed: 5/speed: 5\nlift_speed: 50/}
    /^\[bed_mesh\]/,/^\[/{s/^speed:.*/speed: 700/;s/^probe_count:.*/probe_count: 9,9/;s/^horizontal_move_z:.*/horizontal_move_z: 3/}
    ' $F && echo -e "\033[32m=== After ===\033[0m" && sed -n '/^\[printer\]/,/^\[/{/max_z_velocity/p}' $F && sed -n '/^\[prtouch_v3\]/,/^\[/{/lift_speed/p}' $F && sed -n '/^\[z_align\]/,/^\[/{/distance_ratio\|quick_speed\|^retries:/p}' $F && sed -n '/^\[bed_mesh\]/,/^\[/{/^speed:\|^probe_count\|^horizontal_move_z/p}' $F

<br>

### Do Adaptive Bed Mesh before each print

1. Check how many such rows are there (should be 1)  

        grep -c "bed_mesh_calibate_state == False and" /usr/share/klipper/klippy/extras/virtual_sdcard.py

<br>

2. Remove condition for skipping Adaptive Bed Mesh before each print (do Adaptive Bed Mesh always)  
<br>

        sed -i 's/self\.bed_mesh_calibate_state == False and //' /usr/share/klipper/klippy/extras/virtual_sdcard.py

<br>

3. Check if the command worked  

        sed -n '528p' /usr/share/klipper/klippy/extras/virtual_sdcard.py

<br>

4. remove.Pyc so it recompiles python  

        rm /usr/share/klipper/klippy/extras/virtual_sdcard.pyc

<br>

5. Wait for the bed to reach its target temp before homing and Bed Mesh  


        sed -i '/\[gcode_macro START_PRINT\]/,/^\[/ {/^    M190 S{params.BED_TEMP}$/d; /^    G28$/i\    M190 S{params.BED_TEMP}
        }' /mnt/UDISK/printer_data/config/gcode_macro.cfg

<br>

## Additional commands (NOT PART OF THE IMPROVEMENTS)  
<br>

Don't wait for bed temp before homing and Bed Mesh (roll back to default)  

    sed -i '/\[gcode_macro START_PRINT\]/,/^\[/ {/^    M190 S{params.BED_TEMP}$/d}' /mnt/UDISK/printer_data/config/gcode_macro.cfg

<br>
<br>
<br>

Remove camera CAMNAME from Fluidd (in case you have a bug when you can't remove it using Fluidd UI) replace it with **YOUR** camera name  

    /usr/share/moonraker-env/bin/python -c "import urllib.request,urllib.parse; name='CAMNAME'; url='http://127.0.0.1:7125/server/webcams/item?name='+urllib.parse.quote(name,safe=''); req=urllib.request.Request(url, method='DELETE'); print(urllib.request.urlopen(req, timeout=5).read().decode())"
