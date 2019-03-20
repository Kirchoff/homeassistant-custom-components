#!/usr/bin/python3

# home assistant imports
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

# generic imports
import json

# smartctl module
DOMAIN = 'smartctl'

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    json_file = open('/config/custom_components/sensor/smartctl.json', 'r')
    for line in json_file:
        json_line = json.loads(line)
        add_devices([SmartCtl(json_line)])
    json_file.close()

class SmartCtl(Entity):
    """Representation of a SmartCTL Sensor."""

    def __init__(self, json_line):
        """Initialize the sensor."""
        # no leading underscores - otherwise use them
        self._name = json_line["HDD"].replace('/','',1).replace('/','_')
        self._path = json_line["HDD"]
        self._temperature_celcius = json_line["Temperature_Celsius"]
        self._attributes = {"reallocated_sectors": json_line["Reallocated_Sector_Ct"],
                            "uncorrectable_errors": json_line["Uncorrectable_Error_Cnt"],
                            "current_pending_sectors": json_line["Current_Pending_Sector"],
                            "offline_uncorrectable_errors": json_line["Offline_Uncorrectable"]}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._path

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._temperature_celcius

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def update(self):
        """Fetch new state data for the sensor."""
        json_file = open('/config/custom_components/sensor/smartctl.json', 'r')
        for line in json_file:
            json_line = json.loads(line)
            if (json_line["HDD"] == self._path):
                self._temperature_celcius = json_line["Temperature_Celsius"]
                self._attributes = {"reallocated_sectors": json_line["Reallocated_Sector_Ct"],
                            "uncorrectable_errors": json_line["Uncorrectable_Error_Cnt"],
                            "current_pending_sectors": json_line["Current_Pending_Sector"],
                            "offline_uncorrectable_errors": json_line["Offline_Uncorrectable"]}
            else:
                continue
        json_file.close()

