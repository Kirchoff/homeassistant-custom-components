#!/usr/bin/python3

import subprocess
import json
import argparse

HARD_DRIVE_LIST = list() # populated by discover_drives()

HARD_DRIVE_SMART_IDS = {
"Reallocated_Sector_Ct", # 5
"Uncorrectable_Error_Cnt", # 187
"Temperature_Celsius", # 194
"Current_Pending_Sector", # 197
"Offline_Uncorrectable", # 198
}

def parse_cli_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help='required for <file_path> to be used for smartctl.json output')
    return parser.parse_args()

def discover_drives():
    # Populate all the connected drives
    TEMPORARY_LIST = {}
    proc = subprocess.Popen(["ls /dev/sd* | grep \"sd[a-z]\" | awk '!/[0-9]/'"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    # If the command was sucessful, create a list of drive paths
    if (err is None):
        out = out.decode("utf-8")
        TEMPORARY_LIST = out.split("\n")

    # if we have a non-zero list of drive paths, see if smartctl can read smart data
    if (TEMPORARY_LIST is not None):
        for hdd in TEMPORARY_LIST:

            # empty path check
            if (hdd == ""):
                continue

            # check for errors in the response
            cmd_string = "smartctl -a " + str(hdd) + " | grep \"failed:\|" + str(hdd) + "\""
            proc = subprocess.Popen([cmd_string], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

            # If we have no errors, add it to our list
            if (len(out.decode("utf-8")) == 0):
                HARD_DRIVE_LIST.append(hdd)

def main():
    # Save the file path
    args = parse_cli_arguments()
    print(args.path)
    if (args.path == None):
        sys.exit(0)

    # Determine which drives are available and support smartctl
    discover_drives()

    # TODO: update to use sys.argv input
    output_file = open(str(args.path) + "smartctl.json", "w")

    # Iterate over our drive list
    for hdd in HARD_DRIVE_LIST:

        # create empty json string for this hard drive
        json_string = dict()
        # add our path as a key
        json_string.update({"HDD" : hdd})


        for smart_id in HARD_DRIVE_SMART_IDS:
            # retrieve the value for this smart ID
            proc = subprocess.Popen(["smartctl -a " + str(hdd) + " | grep " + str(smart_id) + " | awk '{print $10}'"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            # convert byte string to string & remove carriage return
            out = out.decode("utf-8").strip('\n')

            # smart_id not supported by this drive, make it zero
            if (str(out) is str("")):
                json_string.update({smart_id : "0"})
            else:
                json_string.update({smart_id : str(out)})

        # convert dictionary to JSON string and write it to our file
        json_string = json.dumps(json_string)
        output_file.write(json_string + str("\n"))

    output_file.close()

if __name__== "__main__":
  main()
