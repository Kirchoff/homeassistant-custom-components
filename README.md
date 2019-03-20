# homeassistant-custom-components
My custom components for home assistant.

# SmartCTL
This custom component is made up of two parts: hdd-script.py and smartctl.py

# hdd-script.py
This script is designed to use the linux package smartmontools to report SMART data from your hard drives. It will discover all available /dev/sd* drives, and poll them with the smartctl binary. If the hard drive reports SMART data, it will be written in JSON format to smartctl.json. The path to smartctl.json should be provided via command line arguement to hdd-script.py. It will need to be ran at the interval that you want updated data to be provided to home assistant. (1 hour cronjob should be satisfactory in most cases)

# smartctl.py
This script is a home assistant sensor module. It will report temperature as the main sensor state, along with SMART attributes as sensor attributes. (5, 187, 194, 197, 198). It reads data provided from hdd-script.py in the form of the smartctl.json file.
