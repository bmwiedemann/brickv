# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2012, 2014 Roland Dudko <roland.dudko@gmail.com>
Copyright (C) 2012, 2014 Marvin Lutz <marvin.lutz.mail@gmail.com>
Copyright (C) 2017 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

loggable_devices.py: Util classes for the data logger

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

#### skip here for brick-logger ####

import time
from collections import namedtuple

if 'merged_data_logger_modules' not in globals():
    from brickv.data_logger.event_logger import EventLogger
    from brickv.data_logger.utils import LoggerTimer, CSVData, \
                                         timestamp_to_de, timestamp_to_us, \
                                         timestamp_to_iso, timestamp_to_unix, \
                                         timestamp_to_de_msec, timestamp_to_us_msec, \
                                         timestamp_to_iso_msec, timestamp_to_unix_msec, \
                                         timestamp_to_strftime

    # Bricks
    from brickv.bindings.brick_dc import BrickDC
    from brickv.bindings.brick_imu import BrickIMU
    from brickv.bindings.brick_imu_v2 import BrickIMUV2
    from brickv.bindings.brick_master import BrickMaster
    from brickv.bindings.brick_servo import BrickServo
    from brickv.bindings.brick_silent_stepper import BrickSilentStepper
    from brickv.bindings.brick_stepper import BrickStepper

    # Bricklets
    from brickv.bindings.bricklet_accelerometer import BrickletAccelerometer
    from brickv.bindings.bricklet_accelerometer_v2 import BrickletAccelerometerV2
    from brickv.bindings.bricklet_air_quality import BrickletAirQuality
    from brickv.bindings.bricklet_ambient_light import BrickletAmbientLight
    from brickv.bindings.bricklet_ambient_light_v2 import BrickletAmbientLightV2
    from brickv.bindings.bricklet_ambient_light_v3 import BrickletAmbientLightV3
    from brickv.bindings.bricklet_analog_in import BrickletAnalogIn
    from brickv.bindings.bricklet_analog_in_v2 import BrickletAnalogInV2
    from brickv.bindings.bricklet_analog_in_v3 import BrickletAnalogInV3
    from brickv.bindings.bricklet_analog_out_v2 import BrickletAnalogOutV2
    from brickv.bindings.bricklet_analog_out_v3 import BrickletAnalogOutV3
    from brickv.bindings.bricklet_barometer import BrickletBarometer
    from brickv.bindings.bricklet_barometer_v2 import BrickletBarometerV2
    from brickv.bindings.bricklet_can import BrickletCAN #NYI FIXME: has to use frame_read callback to get all data
    from brickv.bindings.bricklet_can_v2 import BrickletCANV2 #NYI FIXME: has to use frame_read callback to get all data
    from brickv.bindings.bricklet_co2 import BrickletCO2
    from brickv.bindings.bricklet_co2_v2 import BrickletCO2V2
    from brickv.bindings.bricklet_color import BrickletColor
    from brickv.bindings.bricklet_current12 import BrickletCurrent12
    from brickv.bindings.bricklet_current25 import BrickletCurrent25
    from brickv.bindings.bricklet_distance_ir import BrickletDistanceIR
    from brickv.bindings.bricklet_distance_ir_v2 import BrickletDistanceIRV2
    from brickv.bindings.bricklet_distance_us import BrickletDistanceUS
    from brickv.bindings.bricklet_dmx import BrickletDMX
    from brickv.bindings.bricklet_dual_button import BrickletDualButton
    from brickv.bindings.bricklet_dual_button_v2 import BrickletDualButtonV2
    from brickv.bindings.bricklet_dual_relay import BrickletDualRelay
    from brickv.bindings.bricklet_dust_detector import BrickletDustDetector
    from brickv.bindings.bricklet_gps import BrickletGPS
    from brickv.bindings.bricklet_gps_v2 import BrickletGPSV2
    from brickv.bindings.bricklet_hall_effect import BrickletHallEffect
    from brickv.bindings.bricklet_hall_effect_v2 import BrickletHallEffectV2
    from brickv.bindings.bricklet_humidity import BrickletHumidity
    from brickv.bindings.bricklet_humidity_v2 import BrickletHumidityV2
    from brickv.bindings.bricklet_industrial_counter import BrickletIndustrialCounter
    from brickv.bindings.bricklet_industrial_digital_in_4 import BrickletIndustrialDigitalIn4
    from brickv.bindings.bricklet_industrial_digital_in_4_v2 import BrickletIndustrialDigitalIn4V2
    from brickv.bindings.bricklet_industrial_dual_0_20ma import BrickletIndustrialDual020mA
    from brickv.bindings.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
    from brickv.bindings.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn
    from brickv.bindings.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
    from brickv.bindings.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay
    from brickv.bindings.bricklet_industrial_quad_relay import BrickletIndustrialQuadRelay
    from brickv.bindings.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
    from brickv.bindings.bricklet_io16 import BrickletIO16
    from brickv.bindings.bricklet_io16_v2 import BrickletIO16V2
    from brickv.bindings.bricklet_io4 import BrickletIO4
    from brickv.bindings.bricklet_io4_v2 import BrickletIO4V2
    from brickv.bindings.bricklet_joystick import BrickletJoystick
    from brickv.bindings.bricklet_joystick_v2 import BrickletJoystickV2
    from brickv.bindings.bricklet_laser_range_finder import BrickletLaserRangeFinder #NYI # config: mode, FIXME: special laser handling
    from brickv.bindings.bricklet_led_strip import BrickletLEDStrip
    from brickv.bindings.bricklet_led_strip_v2 import BrickletLEDStripV2
    from brickv.bindings.bricklet_line import BrickletLine
    from brickv.bindings.bricklet_linear_poti import BrickletLinearPoti
    from brickv.bindings.bricklet_linear_poti_v2 import BrickletLinearPotiV2
    from brickv.bindings.bricklet_load_cell import BrickletLoadCell
    from brickv.bindings.bricklet_load_cell_v2 import BrickletLoadCellV2
    from brickv.bindings.bricklet_moisture import BrickletMoisture
    from brickv.bindings.bricklet_motion_detector import BrickletMotionDetector
    from brickv.bindings.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
    from brickv.bindings.bricklet_motorized_linear_poti import BrickletMotorizedLinearPoti
    from brickv.bindings.bricklet_multi_touch import BrickletMultiTouch
    from brickv.bindings.bricklet_nfc import BrickletNFC
    from brickv.bindings.bricklet_nfc_rfid import BrickletNFCRFID
    from brickv.bindings.bricklet_outdoor_weather import BrickletOutdoorWeather
    from brickv.bindings.bricklet_particulate_matter import BrickletParticulateMatter
    from brickv.bindings.bricklet_ptc import BrickletPTC
    from brickv.bindings.bricklet_ptc_v2 import BrickletPTCV2
    from brickv.bindings.bricklet_real_time_clock import BrickletRealTimeClock
    from brickv.bindings.bricklet_real_time_clock_v2 import BrickletRealTimeClockV2
    from brickv.bindings.bricklet_remote_switch import BrickletRemoteSwitch
    from brickv.bindings.bricklet_remote_switch_v2 import BrickletRemoteSwitchV2
    from brickv.bindings.bricklet_rgb_led_button import BrickletRGBLEDButton
    from brickv.bindings.bricklet_rgb_led_matrix import BrickletRGBLEDMatrix
    from brickv.bindings.bricklet_rotary_encoder import BrickletRotaryEncoder
    from brickv.bindings.bricklet_rotary_encoder_v2 import BrickletRotaryEncoderV2
    from brickv.bindings.bricklet_rotary_poti import BrickletRotaryPoti
    #from brickv.bindings.bricklet_rs232 import BrickletRS232 #NYI FIXME: has to use read_callback callback to get all data
    #from brickv.bindings.bricklet_rs232_v2 import BrickletRS232V2 #NYI FIXME: has to use read_callback callback to get all data
    from brickv.bindings.bricklet_rs485 import BrickletRS485
    from brickv.bindings.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
    from brickv.bindings.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
    from brickv.bindings.bricklet_solid_state_relay import BrickletSolidStateRelay
    from brickv.bindings.bricklet_solid_state_relay_v2 import BrickletSolidStateRelayV2
    from brickv.bindings.bricklet_sound_intensity import BrickletSoundIntensity
    from brickv.bindings.bricklet_sound_pressure_level import BrickletSoundPressureLevel
    from brickv.bindings.bricklet_temperature import BrickletTemperature
    from brickv.bindings.bricklet_temperature_v2 import BrickletTemperatureV2
    from brickv.bindings.bricklet_temperature_ir import BrickletTemperatureIR
    from brickv.bindings.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
    from brickv.bindings.bricklet_thermal_imaging import BrickletThermalImaging
    from brickv.bindings.bricklet_thermocouple import BrickletThermocouple
    from brickv.bindings.bricklet_thermocouple_v2 import BrickletThermocoupleV2
    from brickv.bindings.bricklet_tilt import BrickletTilt
    from brickv.bindings.bricklet_uv_light import BrickletUVLight
    from brickv.bindings.bricklet_uv_light_v2 import BrickletUVLightV2
    from brickv.bindings.bricklet_voltage import BrickletVoltage
    from brickv.bindings.bricklet_voltage_current import BrickletVoltageCurrent
    from brickv.bindings.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2
else:
    # Bricks
    from tinkerforge.brick_dc import BrickDC
    from tinkerforge.brick_imu import BrickIMU
    from tinkerforge.brick_imu_v2 import BrickIMUV2
    from tinkerforge.brick_master import BrickMaster
    from tinkerforge.brick_servo import BrickServo
    from tinkerforge.brick_silent_stepper import BrickSilentStepper
    from tinkerforge.brick_stepper import BrickStepper

    # Bricklets
    from tinkerforge.bricklet_accelerometer import BrickletAccelerometer
    from tinkerforge.bricklet_accelerometer_v2 import BrickletAccelerometerV2
    from tinkerforge.bricklet_air_quality import BrickletAirQuality
    from tinkerforge.bricklet_ambient_light import BrickletAmbientLight
    from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
    from tinkerforge.bricklet_ambient_light_v3 import BrickletAmbientLightV3
    from tinkerforge.bricklet_analog_in import BrickletAnalogIn
    from tinkerforge.bricklet_analog_in_v2 import BrickletAnalogInV2
    from tinkerforge.bricklet_analog_in_v3 import BrickletAnalogInV3
    from tinkerforge.bricklet_analog_out_v2 import BrickletAnalogOutV2
    from tinkerforge.bricklet_analog_out_v3 import BrickletAnalogOutV3
    from tinkerforge.bricklet_barometer import BrickletBarometer
    from tinkerforge.bricklet_barometer_v2 import BrickletBarometerV2
    from tinkerforge.bricklet_can import BrickletCAN #NYI FIXME: has to use frame_read callback to get all data
    from tinkerforge.bricklet_can_v2 import BrickletCANV2 #NYI FIXME: has to use frame_read callback to get all data
    from tinkerforge.bricklet_co2 import BrickletCO2
    from tinkerforge.bricklet_co2_v2 import BrickletCO2V2
    from tinkerforge.bricklet_color import BrickletColor
    from tinkerforge.bricklet_current12 import BrickletCurrent12
    from tinkerforge.bricklet_current25 import BrickletCurrent25
    from tinkerforge.bricklet_distance_ir import BrickletDistanceIR
    from tinkerforge.bricklet_distance_ir_v2 import BrickletDistanceIRV2
    from tinkerforge.bricklet_distance_us import BrickletDistanceUS
    from tinkerforge.bricklet_dmx import BrickletDMX
    from tinkerforge.bricklet_dual_button import BrickletDualButton
    from tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
    from tinkerforge.bricklet_dual_relay import BrickletDualRelay
    from tinkerforge.bricklet_dust_detector import BrickletDustDetector
    from tinkerforge.bricklet_gps import BrickletGPS
    from tinkerforge.bricklet_gps_v2 import BrickletGPSV2
    from tinkerforge.bricklet_hall_effect import BrickletHallEffect
    from tinkerforge.bricklet_hall_effect_v2 import BrickletHallEffectV2
    from tinkerforge.bricklet_humidity import BrickletHumidity
    from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2
    from tinkerforge.bricklet_industrial_counter import BrickletIndustrialCounter
    from tinkerforge.bricklet_industrial_digital_in_4 import BrickletIndustrialDigitalIn4
    from tinkerforge.bricklet_industrial_digital_in_4_v2 import BrickletIndustrialDigitalIn4V2
    from tinkerforge.bricklet_industrial_dual_0_20ma import BrickletIndustrialDual020mA
    from tinkerforge.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
    from tinkerforge.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn
    from tinkerforge.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
    from tinkerforge.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay
    from tinkerforge.bricklet_industrial_quad_relay import BrickletIndustrialQuadRelay
    from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
    from tinkerforge.bricklet_io16 import BrickletIO16
    from tinkerforge.bricklet_io16_v2 import BrickletIO16V2
    from tinkerforge.bricklet_io4 import BrickletIO4
    from tinkerforge.bricklet_io4_v2 import BrickletIO4V2
    from tinkerforge.bricklet_joystick import BrickletJoystick
    from tinkerforge.bricklet_joystick_v2 import BrickletJoystickV2
    from tinkerforge.bricklet_laser_range_finder import BrickletLaserRangeFinder #NYI # config: mode, FIXME: special laser handling
    from tinkerforge.bricklet_led_strip import BrickletLEDStrip
    from tinkerforge.bricklet_led_strip_v2 import BrickletLEDStripV2
    from tinkerforge.bricklet_line import BrickletLine
    from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
    from tinkerforge.bricklet_linear_poti_v2 import BrickletLinearPotiV2
    from tinkerforge.bricklet_load_cell import BrickletLoadCell
    from tinkerforge.bricklet_load_cell_v2 import BrickletLoadCellV2
    from tinkerforge.bricklet_moisture import BrickletMoisture
    from tinkerforge.bricklet_motion_detector import BrickletMotionDetector
    from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
    from tinkerforge.bricklet_motorized_linear_poti import BrickletMotorizedLinearPoti
    from tinkerforge.bricklet_multi_touch import BrickletMultiTouch
    from tinkerforge.bricklet_nfc import BrickletNFC
    from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
    from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
    from tinkerforge.bricklet_particulate_matter import BrickletParticulateMatter
    from tinkerforge.bricklet_ptc import BrickletPTC
    from tinkerforge.bricklet_ptc_v2 import BrickletPTCV2
    from tinkerforge.bricklet_real_time_clock import BrickletRealTimeClock
    from tinkerforge.bricklet_real_time_clock_v2 import BrickletRealTimeClockV2
    from tinkerforge.bricklet_remote_switch import BrickletRemoteSwitch
    from tinkerforge.bricklet_remote_switch_v2 import BrickletRemoteSwitchV2
    from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
    from tinkerforge.bricklet_rgb_led_matrix import BrickletRGBLEDMatrix
    from tinkerforge.bricklet_rotary_encoder import BrickletRotaryEncoder
    from tinkerforge.bricklet_rotary_encoder_v2 import BrickletRotaryEncoderV2
    from tinkerforge.bricklet_rotary_poti import BrickletRotaryPoti
    # from tinkerforge.bricklet_rs232 import BrickletRS232 #NYI FIXME: has to use read_callback callback to get all data
    # from tinkerforge.bricklet_rs232_v2 import BrickletRS232V2 #NYI FIXME: has to use read_callback callback to get all data
    from tinkerforge.bricklet_rs485 import BrickletRS485
    from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
    from tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
    from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
    from tinkerforge.bricklet_solid_state_relay_v2 import BrickletSolidStateRelayV2
    from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
    from tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel
    from tinkerforge.bricklet_temperature import BrickletTemperature
    from tinkerforge.bricklet_temperature_v2 import BrickletTemperatureV2
    from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
    from tinkerforge.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
    from tinkerforge.bricklet_thermal_imaging import BrickletThermalImaging
    from tinkerforge.bricklet_thermocouple import BrickletThermocouple
    from tinkerforge.bricklet_thermocouple_v2 import BrickletThermocoupleV2
    from tinkerforge.bricklet_tilt import BrickletTilt
    from tinkerforge.bricklet_uv_light import BrickletUVLight
    from tinkerforge.bricklet_uv_light_v2 import BrickletUVLightV2
    from tinkerforge.bricklet_voltage import BrickletVoltage
    from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
    from tinkerforge.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2

def value_to_bits(value, length):
    bits = []

    for i in range(length):
        if (value & (1 << i)) != 0:
            bits.append(1)
        else:
            bits.append(0)

    return bits

# special_* functions are for special Bricks/Bricklets. Some device functions can
# return different values, depending on different situations, e.g. the GPS Bricklet.
# If the GPS Bricklet does not have a fix, then the function will return an Error
# instead of the specified return values.

# BrickletColor
def special_get_get_illuminance(device):
    gain, integration_time = device.get_config()

    if gain == BrickletColor.GAIN_1X:
        gain_factor = 1
    elif gain == BrickletColor.GAIN_4X:
        gain_factor = 4
    elif gain == BrickletColor.GAIN_16X:
        gain_factor = 16
    elif gain == BrickletColor.GAIN_60X:
        gain_factor = 60

    if integration_time == BrickletColor.INTEGRATION_TIME_2MS:
        integration_time_factor = 2.4
    elif integration_time == BrickletColor.INTEGRATION_TIME_24MS:
        integration_time_factor = 24
    elif integration_time == BrickletColor.INTEGRATION_TIME_101MS:
        integration_time_factor = 101
    elif integration_time == BrickletColor.INTEGRATION_TIME_154MS:
        integration_time_factor = 154
    elif integration_time == BrickletColor.INTEGRATION_TIME_700MS:
        integration_time_factor = 700

    illuminance = device.get_illuminance()

    return int(round(illuminance * 700.0 / float(gain_factor) / float(integration_time_factor), 1) * 10)

# BrickletGPS
def special_get_gps_coordinates(device):
    if device.get_status()[0] == BrickletGPS.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_coordinates()

def special_get_gps_altitude(device):
    if device.get_status()[0] != BrickletGPS.FIX_3D_FIX:
        raise Exception('No 3D fix')
    else:
        return device.get_altitude()

def special_get_gps_motion(device):
    if device.get_status()[0] == BrickletGPS.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_motion()

# BrickletGPSV2
def special_get_gps_v2_coordinates(device):
    if device.get_satellite_system_status(BrickletGPSV2.SATELLITE_SYSTEM_GPS).fix == BrickletGPSV2.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_coordinates()

def special_get_gps_v2_altitude(device):
    if device.get_satellite_system_status(BrickletGPSV2.SATELLITE_SYSTEM_GPS).fix != BrickletGPSV2.FIX_3D_FIX:
        raise Exception('No 3D fix')
    else:
        return device.get_altitude()

def special_get_gps_v2_motion(device):
    if device.get_satellite_system_status(BrickletGPSV2.SATELLITE_SYSTEM_GPS).fix == BrickletGPSV2.FIX_NO_FIX:
        raise Exception('No fix')
    else:
        return device.get_motion()

# BrickletMultiTouch
def special_set_multi_touch_options(device, electrode0, electrode1, electrode2, electrode3,
                                    electrode4, electrode5, electrode6, electrode7,
                                    electrode8, electrode9, electrode10, electrode11,
                                    proximity, electrode_sensitivity):
    electrode_config = 0

    if electrode0:
        electrode_config |= 1 << 0

    if electrode1:
        electrode_config |= 1 << 1

    if electrode2:
        electrode_config |= 1 << 2

    if electrode3:
        electrode_config |= 1 << 3

    if electrode4:
        electrode_config |= 1 << 4

    if electrode5:
        electrode_config |= 1 << 5

    if electrode6:
        electrode_config |= 1 << 6

    if electrode7:
        electrode_config |= 1 << 7

    if electrode8:
        electrode_config |= 1 << 8

    if electrode9:
        electrode_config |= 1 << 9

    if electrode10:
        electrode_config |= 1 << 10

    if electrode11:
        electrode_config |= 1 << 11

    if proximity:
        electrode_config |= 1 << 12

    device.set_electrode_config(electrode_config)
    device.set_electrode_sensitivity(electrode_sensitivity)

# BrickletOutdoorWeather
wind_direction_names = {
    BrickletOutdoorWeather.WIND_DIRECTION_N: 'N',
    BrickletOutdoorWeather.WIND_DIRECTION_NNE: 'NNE',
    BrickletOutdoorWeather.WIND_DIRECTION_NE: 'NE',
    BrickletOutdoorWeather.WIND_DIRECTION_ENE: 'ENE',
    BrickletOutdoorWeather.WIND_DIRECTION_E: 'E',
    BrickletOutdoorWeather.WIND_DIRECTION_ESE: 'ESE',
    BrickletOutdoorWeather.WIND_DIRECTION_SE: 'SE',
    BrickletOutdoorWeather.WIND_DIRECTION_SSE: 'SSE',
    BrickletOutdoorWeather.WIND_DIRECTION_S: 'S',
    BrickletOutdoorWeather.WIND_DIRECTION_SSW: 'SSW',
    BrickletOutdoorWeather.WIND_DIRECTION_SW: 'SW',
    BrickletOutdoorWeather.WIND_DIRECTION_WSW: 'WSW',
    BrickletOutdoorWeather.WIND_DIRECTION_W: 'W',
    BrickletOutdoorWeather.WIND_DIRECTION_WNW: 'WNW',
    BrickletOutdoorWeather.WIND_DIRECTION_NW: 'NW',
    BrickletOutdoorWeather.WIND_DIRECTION_NNW: 'NNW',
    BrickletOutdoorWeather.WIND_DIRECTION_ERROR: 'Wind Direction Error',
}

GetStationData = namedtuple('StationData',
                            ['temperature',
                             'humidity',
                             'wind_speed',
                             'gust_speed',
                             'rain',
                             'wind_direction',
                             'battery_low',
                             'last_change'])

def special_get_station_data(device):
    station_ids = device.get_station_identifiers()

    if len(station_ids) < 1:
        raise Exception('No stations found')

    keyed_station_data = {}

    for station_id in station_ids:
        station_data = device.get_station_data(station_id)

        keyed_station_data[str(station_id)] = GetStationData(temperature=station_data.temperature,
                                                             humidity=station_data.humidity,
                                                             wind_speed=station_data.wind_speed,
                                                             gust_speed=station_data.gust_speed,
                                                             rain=station_data.rain,
                                                             wind_direction=wind_direction_names[station_data.wind_direction],
                                                             battery_low=station_data.battery_low,
                                                             last_change=station_data.last_change)

    return keyed_station_data

def special_get_sensor_data(device):
    sensor_ids = device.get_sensor_identifiers()

    if len(sensor_ids) < 1:
        raise Exception('No sensors found')

    keyed_sensor_data = {}

    for sensor_id in sensor_ids:
        keyed_sensor_data[str(sensor_id)] = device.get_sensor_data(sensor_id)

    return keyed_sensor_data

# BrickletPTC
def special_get_ptc_resistance(device):
    if not device.is_sensor_connected():
        raise Exception('No sensor')
    else:
        return device.get_resistance()

def special_get_ptc_temperature(device):
    if not device.is_sensor_connected():
        raise Exception('No sensor')
    else:
        return device.get_temperature()

# BrickSilentStepper
def special_get_silent_stepper_current_consumption(device):
    return device.get_all_data().current_consumption

device_specs = {
    BrickletAccelerometer.DEVICE_DISPLAY_NAME: {
        'class': BrickletAccelerometer,
        'values': [
            {
                'name': 'Acceleration',
                'getter': lambda device: device.get_acceleration(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['g/1000', 'g/1000', 'g/1000'],
                'advanced': False
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, data_rate, full_scale, filter_bandwidth: device.set_configuration(data_rate, full_scale, filter_bandwidth),
        'options': [
            {
                'name': 'Data Rate',
                'type': 'choice',
                'values': [('Off', BrickletAccelerometer.DATA_RATE_OFF),
                           ('3Hz', BrickletAccelerometer.DATA_RATE_3HZ),
                           ('6Hz', BrickletAccelerometer.DATA_RATE_6HZ),
                           ('12Hz', BrickletAccelerometer.DATA_RATE_12HZ),
                           ('25Hz', BrickletAccelerometer.DATA_RATE_25HZ),
                           ('50Hz', BrickletAccelerometer.DATA_RATE_50HZ),
                           ('100Hz', BrickletAccelerometer.DATA_RATE_100HZ),
                           ('400Hz', BrickletAccelerometer.DATA_RATE_400HZ),
                           ('800Hz', BrickletAccelerometer.DATA_RATE_800HZ),
                           ('1600Hz', BrickletAccelerometer.DATA_RATE_1600HZ)],
                'default': '100Hz'
            },
            {
                'name': 'Full Scale',
                'type': 'choice',
                'values': [('2g', BrickletAccelerometer.FULL_SCALE_2G),
                           ('4g', BrickletAccelerometer.FULL_SCALE_4G),
                           ('6g', BrickletAccelerometer.FULL_SCALE_6G),
                           ('8g', BrickletAccelerometer.FULL_SCALE_8G),
                           ('16g', BrickletAccelerometer.FULL_SCALE_16G)],
                'default': '4g'
            },
            {
                'name': 'Filter Bandwidth',
                'type': 'choice',
                'values': [('800Hz', BrickletAccelerometer.FILTER_BANDWIDTH_800HZ),
                           ('400Hz', BrickletAccelerometer.FILTER_BANDWIDTH_400HZ),
                           ('200Hz', BrickletAccelerometer.FILTER_BANDWIDTH_200HZ),
                           ('50Hz', BrickletAccelerometer.FILTER_BANDWIDTH_50HZ)],
                'default': '200Hz'
            }
        ]
    },
    BrickletAccelerometerV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletAccelerometerV2,
        'values': [
            {
                'name': 'Acceleration',
                'getter': lambda device: device.get_acceleration(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['g/10000', 'g/10000', 'g/10000'],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, data_rate, full_scale: device.set_configuration(data_rate, full_scale),
        'options': [
            {
                'name': 'Data Rate',
                'type': 'choice',
                'values': [('0.781Hz', BrickletAccelerometerV2.DATA_RATE_0_781HZ),
                           ('1.563Hz', BrickletAccelerometerV2.DATA_RATE_1_563HZ),
                           ('3.125Hz', BrickletAccelerometerV2.DATA_RATE_3_125HZ),
                           ('6.2512Hz', BrickletAccelerometerV2.DATA_RATE_6_2512HZ),
                           ('12.5Hz', BrickletAccelerometerV2.DATA_RATE_12_5HZ),
                           ('25Hz', BrickletAccelerometerV2.DATA_RATE_25HZ),
                           ('50Hz', BrickletAccelerometerV2.DATA_RATE_50HZ),
                           ('100Hz', BrickletAccelerometerV2.DATA_RATE_100HZ),
                           ('200Hz', BrickletAccelerometerV2.DATA_RATE_200HZ),
                           ('400Hz', BrickletAccelerometerV2.DATA_RATE_400HZ),
                           ('800Hz', BrickletAccelerometerV2.DATA_RATE_800HZ),
                           ('1600Hz', BrickletAccelerometerV2.DATA_RATE_1600HZ),
                           ('3200Hz', BrickletAccelerometerV2.DATA_RATE_3200HZ),
                           ('6400Hz', BrickletAccelerometerV2.DATA_RATE_6400HZ),
                           ('12800Hz', BrickletAccelerometerV2.DATA_RATE_12800HZ),
                           ('25600Hz', BrickletAccelerometerV2.DATA_RATE_25600HZ)],
                'default': '100Hz'
            },
            {
                'name': 'Full Scale',
                'type': 'choice',
                'values': [('2g', BrickletAccelerometerV2.FULL_SCALE_2G),
                           ('4g', BrickletAccelerometerV2.FULL_SCALE_4G),
                           ('8g', BrickletAccelerometerV2.FULL_SCALE_8G)],
                'default': '2g'
            }
        ]
    },
    BrickletAirQuality.DEVICE_DISPLAY_NAME: {
        'class': BrickletAirQuality,
        'values': [
            {
                'name': 'IAQ Index',
                'getter': lambda device: device.get_iaq_index(),
                'subvalues': ['Value', 'Accuracy'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Humidity',
                'getter': lambda device: device.get_humidity(),
                'subvalues': None,
                'unit': '%RH/100',
                'advanced': False
            },
            {
                'name': 'Air Pressure',
                'getter': lambda device: device.get_air_pressure(),
                'subvalues': None,
                'unit': 'mbar/100',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, temperature_offset: device.set_temperature_offset(temperature_offset),
        'options': [
            {
                'name': 'Temperature Offset',
                'type': 'int',
                'minimum': -2147483648,
                'maximum': 2147483647,
                'suffix': '°C/100',
                'default': 0
            }
        ]
    },
    BrickletAmbientLight.DEVICE_DISPLAY_NAME: {
        'class': BrickletAmbientLight,
        'values': [
            {
                'name': 'Illuminance',
                'getter': lambda device: device.get_illuminance(),
                'subvalues': None,
                'unit': 'lx/10',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletAmbientLightV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletAmbientLightV2,
        'values': [
            {
                'name': 'Illuminance',
                'getter': lambda device: device.get_illuminance(),
                'subvalues': None,
                'unit': 'lx/100',
                'advanced': False
            }
        ],
        'options_setter': lambda device, illuminance_range, integration_time: device.set_configuration(illuminance_range, integration_time),
        'options': [
            {
                'name': 'Illuminance Range',
                'type': 'choice',
                'values': [('Unlimited', 6), # FIXME: BrickletAmbientLightV2.ILLUMINANCE_RANGE_UNLIMITED
                           ('64000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_64000LUX),
                           ('32000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_32000LUX),
                           ('16000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_16000LUX),
                           ('8000Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_8000LUX),
                           ('1300Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_1300LUX),
                           ('600Lux', BrickletAmbientLightV2.ILLUMINANCE_RANGE_600LUX)],
                'default': '8000Lux'
            },
            {
                'name': 'Integration Time',
                'type': 'choice',
                'values': [('50ms', BrickletAmbientLightV2.INTEGRATION_TIME_50MS),
                           ('100ms', BrickletAmbientLightV2.INTEGRATION_TIME_100MS),
                           ('150ms', BrickletAmbientLightV2.INTEGRATION_TIME_150MS),
                           ('200ms', BrickletAmbientLightV2.INTEGRATION_TIME_200MS),
                           ('250ms', BrickletAmbientLightV2.INTEGRATION_TIME_350MS),
                           ('300ms', BrickletAmbientLightV2.INTEGRATION_TIME_300MS),
                           ('350ms', BrickletAmbientLightV2.INTEGRATION_TIME_350MS),
                           ('400ms', BrickletAmbientLightV2.INTEGRATION_TIME_400MS)],
                'default': '200ms'
            }
        ]
    },
    BrickletAmbientLightV3.DEVICE_DISPLAY_NAME: {
        'class': BrickletAmbientLightV3,
        'values': [
            {
                'name': 'Illuminance',
                'getter': lambda device: device.get_illuminance(),
                'subvalues': None,
                'unit': 'lx/100',
                'advanced': False
            }
        ],
        'options_setter': lambda device, illuminance_range, integration_time: device.set_configuration(illuminance_range, integration_time),
        'options': [
            {
                'name': 'Illuminance Range',
                'type': 'choice',
                'values': [('Unlimited', BrickletAmbientLightV3.ILLUMINANCE_RANGE_UNLIMITED),
                           ('64000Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_64000LUX),
                           ('32000Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_32000LUX),
                           ('16000Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_16000LUX),
                           ('8000Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_8000LUX),
                           ('1300Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_1300LUX),
                           ('600Lux', BrickletAmbientLightV3.ILLUMINANCE_RANGE_600LUX)],
                'default': '8000Lux'
            },
            {
                'name': 'Integration Time',
                'type': 'choice',
                'values': [('50ms', BrickletAmbientLightV3.INTEGRATION_TIME_50MS),
                           ('100ms', BrickletAmbientLightV3.INTEGRATION_TIME_100MS),
                           ('150ms', BrickletAmbientLightV3.INTEGRATION_TIME_150MS),
                           ('200ms', BrickletAmbientLightV3.INTEGRATION_TIME_200MS),
                           ('250ms', BrickletAmbientLightV3.INTEGRATION_TIME_350MS),
                           ('300ms', BrickletAmbientLightV3.INTEGRATION_TIME_300MS),
                           ('350ms', BrickletAmbientLightV3.INTEGRATION_TIME_350MS),
                           ('400ms', BrickletAmbientLightV3.INTEGRATION_TIME_400MS)],
                'default': '150ms'
            }
        ]
    },
    BrickletAnalogIn.DEVICE_DISPLAY_NAME: {
        'class': BrickletAnalogIn,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, voltage_range, average_length: [device.set_range(voltage_range), device.set_averaging(average_length)],
        'options': [
            {
                'name': 'Voltage Range',
                'type': 'choice',
                'values': [('Automatic', BrickletAnalogIn.RANGE_AUTOMATIC),
                           ('3.30V', BrickletAnalogIn.RANGE_UP_TO_3V),
                           ('6.05V', BrickletAnalogIn.RANGE_UP_TO_6V),
                           ('10.32V', BrickletAnalogIn.RANGE_UP_TO_10V),
                           ('36.30V', BrickletAnalogIn.RANGE_UP_TO_36V),
                           ('45.00V', BrickletAnalogIn.RANGE_UP_TO_45V)],
                'default': 'Automatic'
            },
            {
                'name': 'Average Length',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': None,
                'default': 50
            }
        ]
    },
    BrickletAnalogInV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletAnalogInV2,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, moving_average_length: device.set_moving_average(moving_average_length),
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 1,
                'maximum': 50,
                'suffix': None,
                'default': 50
            }
        ]
    },
    BrickletAnalogInV3.DEVICE_DISPLAY_NAME: {
        'class': BrickletAnalogInV3,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletAnalogOutV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletAnalogOutV2,
        'values': [
            {
                'name': 'Input Voltage',
                'getter': lambda device: device.get_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletAnalogOutV3.DEVICE_DISPLAY_NAME: {
        'class': BrickletAnalogOutV3,
        'values': [
            {
                'name': 'Input Voltage',
                'getter': lambda device: device.get_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletBarometer.DEVICE_DISPLAY_NAME: {
        'class': BrickletBarometer,
        'values': [
            {
                'name': 'Air Pressure',
                'getter': lambda device: device.get_air_pressure(),
                'subvalues': None,
                'unit': 'mbar/1000',
                'advanced': False
            },
            {
                'name': 'Altitude',
                'getter': lambda device: device.get_altitude(),
                'subvalues': None,
                'unit': 'cm',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': True
            }
        ],
        'options_setter': lambda device, reference_air_pressure, moving_average_length_air_pressure, \
                                         average_length_air_pressure, average_length_temperature: \
                          [device.set_reference_air_pressure(reference_air_pressure),
                           device.set_averaging(moving_average_length_air_pressure,
                                                average_length_air_pressure,
                                                average_length_temperature)],
        'options': [
            {
                'name': 'Reference Air Pressure',
                'type': 'int',
                'minimum': 10000,
                'maximum': 1200000,
                'suffix': ' mbar/1000',
                'default': 1013250
            },
            {
                'name': 'Moving Average Length (Air Pressure)',
                'type': 'int',
                'minimum': 0,
                'maximum': 25,
                'suffix': None,
                'default': 25
            },
            {
                'name': 'Average Length (Air Pressure)',
                'type': 'int',
                'minimum': 0,
                'maximum': 10,
                'suffix': None,
                'default': 10
            },
            {
                'name': 'Average Length (Temperature)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': None,
                'default': 10
            }
        ]
    },
    BrickletBarometerV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletBarometerV2,
        'values': [
            {
                'name': 'Air Pressure',
                'getter': lambda device: device.get_air_pressure(),
                'subvalues': None,
                'unit': 'mbar/1000',
                'advanced': False
            },
            {
                'name': 'Altitude',
                'getter': lambda device: device.get_altitude(),
                'subvalues': None,
                'unit': 'mm',
                'advanced': False
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, reference_air_pressure, \
                                         moving_average_length_air_pressure, \
                                         moving_average_length_temperature,
                                         data_rate,
                                         air_pressure_low_pass_filter: \
                          [device.set_reference_air_pressure(reference_air_pressure),
                           device.set_moving_average_configuration(moving_average_length_air_pressure,
                                                                   moving_average_length_temperature),
                           device.set_sensor_configuration(data_rate, air_pressure_low_pass_filter)],
        'options': [
            {
                'name': 'Reference Air Pressure',
                'type': 'int',
                'minimum': 10000,
                'maximum': 1200000,
                'suffix': ' mbar/1000',
                'default': 1013250
            },
            {
                'name': 'Moving Average Length (Air Pressure)',
                'type': 'int',
                'minimum': 1,
                'maximum': 1000,
                'suffix': None,
                'default': 100
            },
            {
                'name': 'Moving Average Length (Temperature)',
                'type': 'int',
                'minimum': 1,
                'maximum': 1000,
                'suffix': None,
                'default': 100
            },
            {
                'name': 'Data Rate',
                'type': 'choice',
                'values': [('Off', BrickletBarometerV2.DATA_RATE_OFF),
                           ('1 Hz', BrickletBarometerV2.DATA_RATE_1HZ),
                           ('10 Hz', BrickletBarometerV2.DATA_RATE_10HZ),
                           ('25 Hz', BrickletBarometerV2.DATA_RATE_25HZ),
                           ('50 Hz', BrickletBarometerV2.DATA_RATE_50HZ),
                           ('75 Hz', BrickletBarometerV2.DATA_RATE_75HZ)],
                'default': '50 Hz'
            },
            {
                'name': 'Air Pressure Low Pass Filter',
                'type': 'choice',
                'values': [('Off', BrickletBarometerV2.LOW_PASS_FILTER_OFF),
                           ('1/9th', BrickletBarometerV2.LOW_PASS_FILTER_1_9TH),
                           ('1/20th', BrickletBarometerV2.LOW_PASS_FILTER_1_20TH)],
                'default': '1/9th'
            }
        ]
    },
    BrickletCAN.DEVICE_DISPLAY_NAME: {
        'class': BrickletCAN,
        'values': [
            {
                'name': 'Error Log',
                'getter': lambda device: device.get_error_log(),
                'subvalues': ['Write Error Level',
                              'Read Error Level',
                              'Transceiver Disabled',
                              'Write Timeout Count',
                              'Read Register Overflow Count',
                              'Read Buffer Overflow Count'],
                'unit': [None, None, None, None, None, None],
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletCANV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletCANV2,
        'values': [
            {
                'name': 'Error Log',
                'getter': lambda device: device.get_error_log(),
                'subvalues': ['Transceiver State',
                              'Transceiver Write Error Level',
                              'Transceiver Read Error Level',
                              'Transceiver Stuffing Error Count',
                              'Transceiver Format Error Count',
                              'Transceiver ACK Error Count',
                              'Transceiver Bit1 Error Count',
                              'Transceiver Bit0 Error Count',
                              'Transceiver CRC Error Count',
                              'Write Buffer Timeout Error Count',
                              'Read Buffer Overflow Error Count',
                              #'Read Buffer Overflow Error Occurred Length',
                              'Read Buffer Overflow Error Occurred',
                              'Read Backlog Overflow Error Count'],
                'unit': [None, None, None, None, None, None, None, None, None, None, None, None, None],
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletCO2.DEVICE_DISPLAY_NAME: {
        'class': BrickletCO2,
        'values': [
            {
                'name': 'CO2 Concentration',
                'getter': lambda device: device.get_co2_concentration(),
                'subvalues': None,
                'unit': 'ppm',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletCO2V2.DEVICE_DISPLAY_NAME: {
        'class': BrickletCO2V2,
        'values': [
            {
                'name': 'CO2 Concentration',
                'getter': lambda device: device.get_co2_concentration(),
                'subvalues': None,
                'unit': 'ppm',
                'advanced': False
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Humidity',
                'getter': lambda device: device.get_humidity(),
                'subvalues': None,
                'unit': '%RH/100',
                'advanced': False
            },
            {
                'name': 'All Values',
                'getter': lambda device: device.get_all_values(),
                'subvalues': ['CO2 Concentration', 'Temperature', 'Humidity'],
                'unit': ['ppm', '°C/100', '%RH/100'],
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletColor.DEVICE_DISPLAY_NAME: {
        'class': BrickletColor,
        'values': [
            {
                'name': 'Color',
                'getter': lambda device: device.get_color(),
                'subvalues': ['Red', 'Green', 'Blue', 'Clear'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Color Temperature',
                'getter': lambda device: device.get_color_temperature(), # FIXME: saturation handling is missing
                'subvalues': None,
                'unit': 'K',
                'advanced': False
            },
            {
                'name': 'Illuminance',
                'getter': special_get_get_illuminance, # FIXME: saturation handling is missing
                'subvalues': None,
                'unit': 'lx/10',
                'advanced': False
            }
        ],
        'options_setter': lambda device, gain, integration_time: device.set_config(gain, integration_time),
        'options': [
            {
                'name': 'Gain',
                'type': 'choice',
                'values': [('1x', BrickletColor.GAIN_1X),
                           ('4x', BrickletColor.GAIN_4X),
                           ('16x', BrickletColor.GAIN_16X),
                           ('60x', BrickletColor.GAIN_60X)],
                'default': '60x'
            },
            {
                'name': 'Integration Time',
                'type': 'choice',
                'values': [('2.4ms', BrickletColor.INTEGRATION_TIME_2MS),
                           ('24ms', BrickletColor.INTEGRATION_TIME_24MS),
                           ('101ms', BrickletColor.INTEGRATION_TIME_101MS),
                           ('154ms', BrickletColor.INTEGRATION_TIME_154MS),
                           ('700ms', BrickletColor.INTEGRATION_TIME_700MS)],
                'default': '154ms'
            }
        ]
    },
    BrickletCurrent12.DEVICE_DISPLAY_NAME: {
        'class': BrickletCurrent12,
        'values': [
            {
                'name': 'Current',
                'getter': lambda device: device.get_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletCurrent25.DEVICE_DISPLAY_NAME: {
        'class': BrickletCurrent25,
        'values': [
            {
                'name': 'Current',
                'getter': lambda device: device.get_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDistanceIR.DEVICE_DISPLAY_NAME: {
        'class': BrickletDistanceIR,
        'values': [
            {
                'name': 'Distance',
                'getter': lambda device: device.get_distance(),
                'subvalues': None,
                'unit': 'mm',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDistanceIRV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletDistanceIRV2,
        'values': [
            {
                'name': 'Distance',
                'getter': lambda device: device.get_distance(),
                'subvalues': None,
                'unit': 'mm',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, moving_average_length: device.set_moving_average_configuration(moving_average_length),
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 0,
                'maximum': 1000,
                'suffix': None,
                'default': 25
            }
        ]
    },
    BrickletDistanceUS.DEVICE_DISPLAY_NAME: {
        'class': BrickletDistanceUS,
        'values': [
            {
                'name': 'Distance Value',
                'getter': lambda device: device.get_distance_value(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': lambda device, moving_average_length: device.set_moving_average(moving_average_length),
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 0,
                'maximum': 100,
                'suffix': None,
                'default': 20
            }
        ]
    },
    BrickletDualButton.DEVICE_DISPLAY_NAME: {
        'class': BrickletDualButton,
        'values': [
            {
                'name': 'Button State',
                'getter': lambda device: device.get_button_state(),
                'subvalues': ['Left', 'Right'],
                'unit': [None, None], # FIXME: constants?
                'advanced': False
            },
            {
                'name': 'LED State',
                'getter': lambda device: device.get_led_state(),
                'subvalues': ['Left', 'Right'],
                'unit': [None, None], # FIXME: constants?
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDualButtonV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletDualButtonV2,
        'values': [
            {
                'name': 'Button State',
                'getter': lambda device: device.get_button_state(),
                'subvalues': ['Left', 'Right'],
                'unit': [None, None], # FIXME: constants?
                'advanced': False
            },
            {
                'name': 'LED State',
                'getter': lambda device: device.get_led_state(),
                'subvalues': ['Left', 'Right'],
                'unit': [None, None], # FIXME: constants?
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDualRelay.DEVICE_DISPLAY_NAME: {
        'class': BrickletDualRelay,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_state(),
                'subvalues': ['Relay1', 'Relay2'],
                'unit': [None, None],
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDustDetector.DEVICE_DISPLAY_NAME: {
        'class': BrickletDustDetector,
        'values': [
            {
                'name': 'Dust Density',
                'getter': lambda device: device.get_dust_density(),
                'subvalues': None,
                'unit': 'µg/m³',
                'advanced': False
            }
        ],
        'options_setter': lambda device, moving_average_length: device.set_moving_average(moving_average_length),
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 0,
                'maximum': 100,
                'suffix': None,
                'default': 100
            }
        ]
    },
    BrickletGPS.DEVICE_DISPLAY_NAME: {
        'class': BrickletGPS,
        'values': [
            {
                'name': 'Coordinates',
                'getter': special_get_gps_coordinates,
                'subvalues': ['Latitude', 'NS', 'Longitude', 'EW', 'PDOP', 'HDOP', 'VDOP', 'EPE'],
                'unit': ['deg/1000000', None, 'deg/1000000', None, '1/100', '1/100', '1/100', 'cm'],
                'advanced': False
            },
            {
                'name': 'Altitude',
                'getter': special_get_gps_altitude,
                'subvalues': ['Altitude', 'Geoidal Separation'],
                'unit': ['cm', 'cm'],
                'advanced': False
            },
            {
                'name': 'Motion',
                'getter': special_get_gps_motion,
                'subvalues': ['Course', 'Speed'],
                'unit': ['deg/100', '10m/h'],
                'advanced': False
            },
            {
                'name': 'Date Time',
                'getter': lambda device: device.get_date_time(),
                'subvalues': ['Date', 'Time'],
                'unit': ['ddmmyy', 'hhmmss|sss'],
                'advanced': False
            },
            {
                'name': 'Status',
                'getter': lambda device: device.get_status(),
                'subvalues': ['Fix', 'Satellites View', 'Satellites Used'],
                'unit': [None, None, None], # FIXME: fix constants?
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletGPSV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletGPSV2,
        'values': [
            {
                'name': 'Coordinates',
                'getter': special_get_gps_v2_coordinates,
                'subvalues': ['Latitude', 'NS', 'Longitude', 'EW'],
                'unit': ['deg/1000000', None, 'deg/1000000', None],
                'advanced': False
            },
            {
                'name': 'Altitude',
                'getter': special_get_gps_v2_altitude,
                'subvalues': ['Altitude', 'Geoidal Separation'],
                'unit': ['cm', 'cm'],
                'advanced': False
            },
            {
                'name': 'Motion',
                'getter': special_get_gps_v2_motion,
                'subvalues': ['Course', 'Speed'],
                'unit': ['deg/100', '10m/h'],
                'advanced': False
            },
            {
                'name': 'Date Time',
                'getter': lambda device: device.get_date_time(),
                'subvalues': ['Date', 'Time'],
                'unit': ['ddmmyy', 'hhmmss|sss'],
                'advanced': False
            },
            {
                'name': 'Status',
                'getter': lambda device: device.get_status(),
                'subvalues': ['Fix', 'Satellites View'],
                'unit': [None, None], # FIXME: fix constants?
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletHallEffect.DEVICE_DISPLAY_NAME: {
        'class': BrickletHallEffect,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_value(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Edge Count',
                'getter': lambda device: device.get_edge_count(False),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': lambda device, edge_count_type, edge_count_debounce: device.set_edge_count_config(edge_count_type, edge_count_debounce),
        'options': [
            {
                'name': 'Edge Count Type',
                'type': 'choice',
                'values': [('Rising', BrickletHallEffect.EDGE_TYPE_RISING),
                           ('Falling', BrickletHallEffect.EDGE_TYPE_FALLING),
                           ('Both', BrickletHallEffect.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletHallEffectV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletHallEffectV2,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_magnetic_flux_density(),
                'subvalues': None,
                'unit': 'uT',
                'advanced': False
            },
            {
                'name': 'Count',
                'getter': lambda device: device.get_counter(False),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': lambda device, high_threshold, low_threshold, debounce: device.set_counter_config(high_threshold, low_threshold, debounce),
        'options': [
            {
                'name': 'High Threshold',
                'type': 'int',
                'minimum': -7000,
                'maximum': 7000,
                'suffix': ' uT',
                'default': 2000
            },
            {
                'name': 'Low Threshold',
                'type': 'int',
                'minimum': -7000,
                'maximum': 7000,
                'suffix': ' uT',
                'default': -2000
            },
            {
                'name': ' Debounce',
                'type': 'int',
                'minimum': 0,
                'maximum': 2147483647,
                'suffix': ' us',
                'default': 100000
            }
        ]
    },
    BrickletHumidity.DEVICE_DISPLAY_NAME: {
        'class': BrickletHumidity,
        'values': [
            {
                'name': 'Humidity',
                'getter': lambda device: device.get_humidity(),
                'subvalues': None,
                'unit': '%RH/10',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletHumidityV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletHumidityV2,
        'values': [
            {
                'name': 'Humidity',
                'getter': lambda device: device.get_humidity(),
                'subvalues': None,
                'unit': '%RH/100',
                'advanced': False
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletIndustrialCounter.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialCounter,
        'values': [
            {
                'name': 'Count',
                'getter': lambda device: device.get_all_counter(),
                'subvalues': ['Channel0', 'Channel1', 'Channel2', 'Channel3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Signal Data (Channel0)',
                'getter': lambda device: device.get_signal_data(0),
                'subvalues': ['Duty Cycle', 'Period', 'Frequency', 'Value'],
                'unit': ['1/100%', 'ns', 'mHz', None],
                'advanced': False
            },
            {
                'name': 'Signal Data (Channel1)',
                'getter': lambda device: device.get_signal_data(1),
                'subvalues': ['Duty Cycle', 'Period', 'Frequency', 'Value'],
                'unit': ['1/100%', 'ns', 'mHz', None],
                'advanced': False
            },
            {
                'name': 'Signal Data (Channel2)',
                'getter': lambda device: device.get_signal_data(2),
                'subvalues': ['Duty Cycle', 'Period', 'Frequency', 'Value'],
                'unit': ['1/100%', 'ns', 'mHz', None],
                'advanced': False
            },
            {
                'name': 'Signal Data (Channel3)',
                'getter': lambda device: device.get_signal_data(3),
                'subvalues': ['Duty Cycle', 'Period', 'Frequency', 'Value'],
                'unit': ['1/100%', 'ns', 'mHz', None],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletIndustrialDigitalIn4.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDigitalIn4,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: value_to_bits(device.get_value(), 4),
                'subvalues': ['Pin 0', 'Pin 1', 'Pin 2', 'Pin 3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Pin 0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 2)',
                'getter': lambda device: device.get_edge_count(2, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 3)',
                'getter': lambda device: device.get_edge_count(3, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, edge_count_type_pin0, edge_count_debounce_pin0, \
                                         edge_count_type_pin1, edge_count_debounce_pin1, \
                                         edge_count_type_pin2, edge_count_debounce_pin2, \
                                         edge_count_type_pin3, edge_count_debounce_pin3: \
                          [device.set_edge_count_config(0b0001, edge_count_type_pin0, edge_count_debounce_pin0),
                           device.set_edge_count_config(0b0010, edge_count_type_pin1, edge_count_debounce_pin1),
                           device.set_edge_count_config(0b0100, edge_count_type_pin2, edge_count_debounce_pin2),
                           device.set_edge_count_config(0b1000, edge_count_type_pin3, edge_count_debounce_pin3)],
        'options': [
            {
                'name': 'Edge Count Type (Pin 0)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 0)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 1)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 1)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 2)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 2)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 3)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 3)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletIndustrialDigitalIn4V2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDigitalIn4V2,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_value(),
                'subvalues': ['Channel0', 'Channel1', 'Channel2', 'Channel3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Channel0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel2)',
                'getter': lambda device: device.get_edge_count(2, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel3)',
                'getter': lambda device: device.get_edge_count(3, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, edge_count_type_channel0, edge_count_debounce_channel0, \
                                         edge_count_type_channel1, edge_count_debounce_channel1, \
                                         edge_count_type_channel2, edge_count_debounce_channel2, \
                                         edge_count_type_channel3, edge_count_debounce_channel3: \
                          [device.set_edge_count_configuration(0, edge_count_type_channel0, edge_count_debounce_channel0),
                           device.set_edge_count_configuration(1, edge_count_type_channel1, edge_count_debounce_channel1),
                           device.set_edge_count_configuration(2, edge_count_type_channel2, edge_count_debounce_channel2),
                           device.set_edge_count_configuration(3, edge_count_type_channel3, edge_count_debounce_channel3)],
        'options': [
            {
                'name': 'Edge Count Type (Channel0)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel0)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel1)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel1)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel2)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel2)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel3)',
                'type': 'choice',
                'values': [('Rising', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIndustrialDigitalIn4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel3)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletIndustrialDual020mA.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDual020mA,
        'values': [
            {
                'name': 'Current (Sensor 0)',
                'getter': lambda device: device.get_current(0),
                'subvalues': None,
                'unit': 'nA',
                'advanced': False
            },
            {
                'name': 'Current (Sensor 1)',
                'getter': lambda device: device.get_current(1),
                'subvalues': None,
                'unit': 'nA',
                'advanced': False
            }
        ],
        'options_setter': lambda device, sample_rate: device.set_sample_rate(sample_rate),
        'options': [
            {
                'name': 'Sample Rate',
                'type': 'choice',
                'values': [('240 SPS', BrickletIndustrialDual020mA.SAMPLE_RATE_240_SPS),
                           ('60 SPS', BrickletIndustrialDual020mA.SAMPLE_RATE_60_SPS),
                           ('15 SPS', BrickletIndustrialDual020mA.SAMPLE_RATE_15_SPS),
                           ('4 SPS', BrickletIndustrialDual020mA.SAMPLE_RATE_4_SPS)],
                'default': '4 SPS'
            }
        ]
    },
    BrickletIndustrialDual020mAV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDual020mAV2,
        'values': [
            {
                'name': 'Current (Sensor 0)',
                'getter': lambda device: device.get_current(0),
                'subvalues': None,
                'unit': 'nA',
                'advanced': False
            },
            {
                'name': 'Current (Sensor 1)',
                'getter': lambda device: device.get_current(1),
                'subvalues': None,
                'unit': 'nA',
                'advanced': False
            }
        ],
        'options_setter': lambda device, sample_rate, gain: [device.set_sample_rate(sample_rate), device.set_gain(gain)],
        'options': [
            {
                'name': 'Sample Rate',
                'type': 'choice',
                'values': [('240 SPS', BrickletIndustrialDual020mAV2.SAMPLE_RATE_240_SPS),
                           ('60 SPS', BrickletIndustrialDual020mAV2.SAMPLE_RATE_60_SPS),
                           ('15 SPS', BrickletIndustrialDual020mAV2.SAMPLE_RATE_15_SPS),
                           ('4 SPS', BrickletIndustrialDual020mAV2.SAMPLE_RATE_4_SPS)],
                'default': '4 SPS'
            },
            {
                'name': 'Gain',
                'type': 'choice',
                'values': [('1x', BrickletIndustrialDual020mAV2.GAIN_1X),
                           ('2x', BrickletIndustrialDual020mAV2.GAIN_2X),
                           ('4x', BrickletIndustrialDual020mAV2.GAIN_4X),
                           ('8x', BrickletIndustrialDual020mAV2.GAIN_8X)],
                'default': '1x'
            }
        ]
    },
    BrickletIndustrialDualAnalogInV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDualAnalogInV2,
        'values': [
            {
                'name': 'Voltage (Channel0)',
                'getter': lambda device: device.get_voltage(0),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Voltage (Channel1)',
                'getter': lambda device: device.get_voltage(1),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'ADC Values',
                'getter': lambda device: device.get_adc_values(),
                'subvalues': ['Channel0', 'Channel1'],
                'unit': [None, None],
                'advanced': True
            }
        ],
        'options_setter': lambda device, sample_rate: device.set_sample_rate(sample_rate),
        'options': [
            {
                'name': 'Sample Rate',
                'type': 'choice',
                'values': [('976 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_976_SPS),
                           ('488 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_488_SPS),
                           ('244 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_244_SPS),
                           ('122 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_122_SPS),
                           ('61 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_61_SPS),
                           ('4 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_4_SPS),
                           ('2 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_2_SPS),
                           ('1 SPS', BrickletIndustrialDualAnalogInV2.SAMPLE_RATE_1_SPS)],
                'default': '2 SPS'
            }
        ]
    },
    BrickletIndustrialDualAnalogIn.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDualAnalogIn,
        'values': [
            {
                'name': 'Voltage (Channel0)',
                'getter': lambda device: device.get_voltage(0),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Voltage (Channel1)',
                'getter': lambda device: device.get_voltage(1),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'ADC Values',
                'getter': lambda device: device.get_adc_values(),
                'subvalues': ['Channel0', 'Channel1'],
                'unit': [None, None],
                'advanced': True
            }
        ],
        'options_setter': lambda device, sample_rate: device.set_sample_rate(sample_rate),
        'options': [
            {
                'name': 'Sample Rate',
                'type': 'choice',
                'values': [('976 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_976_SPS),
                           ('488 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_488_SPS),
                           ('244 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_244_SPS),
                           ('122 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_122_SPS),
                           ('61 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_61_SPS),
                           ('4 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_4_SPS),
                           ('2 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_2_SPS),
                           ('1 SPS', BrickletIndustrialDualAnalogIn.SAMPLE_RATE_1_SPS)],
                'default': '2 SPS'
            }
        ]
    },
    BrickletIndustrialDualRelay.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialDualRelay,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_value(),
                'subvalues': ['Channel0', 'Channel1'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletIndustrialQuadRelay.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialQuadRelay,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: value_to_bits(device.get_value(), 4),
                'subvalues': ['Relay1', 'Relay2', 'Relay3', 'Relay4'],
                'unit': [None, None, None, None],
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletIndustrialQuadRelayV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIndustrialQuadRelayV2,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_value(),
                'subvalues': ['Channel0', 'Channel1', 'Channel2', 'Channel3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletIO16.DEVICE_DISPLAY_NAME: {
        'class': BrickletIO16,
        'values': [
            {
                'name': 'Port A',
                'getter': lambda device: value_to_bits(device.get_port('a'), 8),
                'subvalues': ['Pin 0', 'Pin 1', 'Pin 2', 'Pin 3', 'Pin 4', 'Pin 5', 'Pin 6', 'Pin 7'],
                'unit': [None, None, None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Port B',
                'getter': lambda device: value_to_bits(device.get_port('b'), 8),
                'subvalues': ['Pin 0', 'Pin 1', 'Pin 2', 'Pin 3', 'Pin 4', 'Pin 5', 'Pin 6', 'Pin 7'],
                'unit': [None, None, None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Pin A0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin A1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, pinA0, pinA1, pinA2, pinA3, pinA4, pinA5, pinA6, pinA7,
                                         pinB0, pinB1, pinB2, pinB3, pinB4, pinB5, pinB6, pinB7,
                                         edge_count_type_pinA0, edge_count_debounce_pinA0, \
                                         edge_count_type_pinA1, edge_count_debounce_pinA1: \
                          [device.set_port_configuration(*pinA0),
                           device.set_port_configuration(*pinA1),
                           device.set_port_configuration(*pinA2),
                           device.set_port_configuration(*pinA3),
                           device.set_port_configuration(*pinA4),
                           device.set_port_configuration(*pinA5),
                           device.set_port_configuration(*pinA6),
                           device.set_port_configuration(*pinA7),
                           device.set_port_configuration(*pinB0),
                           device.set_port_configuration(*pinB1),
                           device.set_port_configuration(*pinB2),
                           device.set_port_configuration(*pinB3),
                           device.set_port_configuration(*pinB4),
                           device.set_port_configuration(*pinB5),
                           device.set_port_configuration(*pinB6),
                           device.set_port_configuration(*pinB7),
                           device.set_edge_count_config(0, edge_count_type_pinA0, edge_count_debounce_pinA0),
                           device.set_edge_count_config(1, edge_count_type_pinA1, edge_count_debounce_pinA1)],
        'options': [
            {
                'name': 'Pin A0',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00000001, 'i', True)),
                           ('Input', ('a', 0b00000001, 'i', False)),
                           ('Output High', ('a', 0b00000001, 'o', True)),
                           ('Output Low', ('a', 0b00000001, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A1',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00000010, 'i', True)),
                           ('Input', ('a', 0b00000010, 'i', False)),
                           ('Output High', ('a', 0b00000010, 'o', True)),
                           ('Output Low', ('a', 0b00000010, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A2',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00000100, 'i', True)),
                           ('Input', ('a', 0b00000100, 'i', False)),
                           ('Output High', ('a', 0b00000100, 'o', True)),
                           ('Output Low', ('a', 0b00000100, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A3',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00001000, 'i', True)),
                           ('Input', ('a', 0b00001000, 'i', False)),
                           ('Output High', ('a', 0b00001000, 'o', True)),
                           ('Output Low', ('a', 0b00001000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A4',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00010000, 'i', True)),
                           ('Input', ('a', 0b00010000, 'i', False)),
                           ('Output High', ('a', 0b00010000, 'o', True)),
                           ('Output Low', ('a', 0b00010000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A5',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b00100000, 'i', True)),
                           ('Input', ('a', 0b00100000, 'i', False)),
                           ('Output High', ('a', 0b00100000, 'o', True)),
                           ('Output Low', ('a', 0b00100000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A6',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b01000000, 'i', True)),
                           ('Input', ('a', 0b01000000, 'i', False)),
                           ('Output High', ('a', 0b01000000, 'o', True)),
                           ('Output Low', ('a', 0b01000000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin A7',
                'type': 'choice',
                'values': [('Input Pull-Up', ('a', 0b10000000, 'i', True)),
                           ('Input', ('a', 0b10000000, 'i', False)),
                           ('Output High', ('a', 0b10000000, 'o', True)),
                           ('Output Low', ('a', 0b10000000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B0',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00000001, 'i', True)),
                           ('Input', ('b', 0b00000001, 'i', False)),
                           ('Output High', ('b', 0b00000001, 'o', True)),
                           ('Output Low', ('b', 0b00000001, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B1',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00000010, 'i', True)),
                           ('Input', ('b', 0b00000010, 'i', False)),
                           ('Output High', ('b', 0b00000010, 'o', True)),
                           ('Output Low', ('b', 0b00000010, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B2',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00000100, 'i', True)),
                           ('Input', ('b', 0b00000100, 'i', False)),
                           ('Output High', ('b', 0b00000100, 'o', True)),
                           ('Output Low', ('b', 0b00000100, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B3',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00001000, 'i', True)),
                           ('Input', ('b', 0b00001000, 'i', False)),
                           ('Output High', ('b', 0b00001000, 'o', True)),
                           ('Output Low', ('b', 0b00001000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B4',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00010000, 'i', True)),
                           ('Input', ('b', 0b00010000, 'i', False)),
                           ('Output High', ('b', 0b00010000, 'o', True)),
                           ('Output Low', ('b', 0b00010000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B5',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b00100000, 'i', True)),
                           ('Input', ('b', 0b00100000, 'i', False)),
                           ('Output High', ('b', 0b00100000, 'o', True)),
                           ('Output Low', ('b', 0b00100000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B6',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b01000000, 'i', True)),
                           ('Input', ('b', 0b01000000, 'i', False)),
                           ('Output High', ('b', 0b01000000, 'o', True)),
                           ('Output Low', ('b', 0b01000000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin B7',
                'type': 'choice',
                'values': [('Input Pull-Up', ('b', 0b10000000, 'i', True)),
                           ('Input', ('b', 0b10000000, 'i', False)),
                           ('Output High', ('b', 0b10000000, 'o', True)),
                           ('Output Low', ('b', 0b10000000, 'o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Edge Count Type (Pin A0)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin A0)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin A1)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin A1)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletIO16V2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIO16V2,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_value(),
                'subvalues': ['Channel0', 'Channel1', 'Channel2', 'Channel3', 'Channel4', 'Channel5', 'Channel6', 'Channel7', 'Channel8', 'Channel9', 'Channel10', 'Channel11', 'Channel12', 'Channel13', 'Channel14', 'Channel15'],
                'unit': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Channel0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel2)',
                'getter': lambda device: device.get_edge_count(2, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel3)',
                'getter': lambda device: device.get_edge_count(3, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel4)',
                'getter': lambda device: device.get_edge_count(4, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel5)',
                'getter': lambda device: device.get_edge_count(5, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel6)',
                'getter': lambda device: device.get_edge_count(6, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel7)',
                'getter': lambda device: device.get_edge_count(7, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel8)',
                'getter': lambda device: device.get_edge_count(8, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel9)',
                'getter': lambda device: device.get_edge_count(9, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel10)',
                'getter': lambda device: device.get_edge_count(10, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel11)',
                'getter': lambda device: device.get_edge_count(11, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel12)',
                'getter': lambda device: device.get_edge_count(12, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel13)',
                'getter': lambda device: device.get_edge_count(13, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel14)',
                'getter': lambda device: device.get_edge_count(14, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel15)',
                'getter': lambda device: device.get_edge_count(15, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device,
                                 channel0,
                                 channel1,
                                 channel2,
                                 channel3,
                                 channel4,
                                 channel5,
                                 channel6,
                                 channel7,
                                 channel8,
                                 channel9,
                                 channel10,
                                 channel11,
                                 channel12,
                                 channel13,
                                 channel14,
                                 channel15,
                                 edge_count_type_channel0,
                                 edge_count_debounce_channel0,
                                 edge_count_type_channel1,
                                 edge_count_debounce_channel1,
                                 edge_count_type_channel2,
                                 edge_count_debounce_channel2,
                                 edge_count_type_channel3,
                                 edge_count_debounce_channel3,
                                 edge_count_type_channel4,
                                 edge_count_debounce_channel4,
                                 edge_count_type_channel5,
                                 edge_count_debounce_channel5,
                                 edge_count_type_channel6,
                                 edge_count_debounce_channel6,
                                 edge_count_type_channel7,
                                 edge_count_debounce_channel7,
                                 edge_count_type_channel8,
                                 edge_count_debounce_channel8,
                                 edge_count_type_channel9,
                                 edge_count_debounce_channel9,
                                 edge_count_type_channel10,
                                 edge_count_debounce_channel10,
                                 edge_count_type_channel11,
                                 edge_count_debounce_channel11,
                                 edge_count_type_channel12,
                                 edge_count_debounce_channel12,
                                 edge_count_type_channel13,
                                 edge_count_debounce_channel13,
                                 edge_count_type_channel14,
                                 edge_count_debounce_channel14,
                                 edge_count_type_channel15,
                                 edge_count_debounce_channel15:
                          [device.set_configuration(0, *channel0),
                           device.set_configuration(1, *channel1),
                           device.set_configuration(2, *channel2),
                           device.set_configuration(3, *channel3),
                           device.set_configuration(4, *channel4),
                           device.set_configuration(5, *channel5),
                           device.set_configuration(6, *channel6),
                           device.set_configuration(7, *channel7),
                           device.set_configuration(8, *channel8),
                           device.set_configuration(9, *channel9),
                           device.set_configuration(10, *channel10),
                           device.set_configuration(11, *channel11),
                           device.set_configuration(12, *channel12),
                           device.set_configuration(13, *channel13),
                           device.set_configuration(14, *channel14),
                           device.set_configuration(15, *channel15),
                           device.set_edge_count_configuration(0, edge_count_type_channel0, edge_count_debounce_channel0),
                           device.set_edge_count_configuration(1, edge_count_type_channel1, edge_count_debounce_channel1),
                           device.set_edge_count_configuration(2, edge_count_type_channel2, edge_count_debounce_channel2),
                           device.set_edge_count_configuration(3, edge_count_type_channel3, edge_count_debounce_channel3),
                           device.set_edge_count_configuration(4, edge_count_type_channel4, edge_count_debounce_channel4),
                           device.set_edge_count_configuration(5, edge_count_type_channel5, edge_count_debounce_channel5),
                           device.set_edge_count_configuration(6, edge_count_type_channel6, edge_count_debounce_channel6),
                           device.set_edge_count_configuration(7, edge_count_type_channel7, edge_count_debounce_channel7),
                           device.set_edge_count_configuration(8, edge_count_type_channel8, edge_count_debounce_channel8),
                           device.set_edge_count_configuration(9, edge_count_type_channel9, edge_count_debounce_channel9),
                           device.set_edge_count_configuration(10, edge_count_type_channel10, edge_count_debounce_channel10),
                           device.set_edge_count_configuration(11, edge_count_type_channel11, edge_count_debounce_channel11),
                           device.set_edge_count_configuration(12, edge_count_type_channel12, edge_count_debounce_channel12),
                           device.set_edge_count_configuration(13, edge_count_type_channel13, edge_count_debounce_channel13),
                           device.set_edge_count_configuration(14, edge_count_type_channel14, edge_count_debounce_channel14),
                           device.set_edge_count_configuration(15, edge_count_type_channel15, edge_count_debounce_channel15)],
        'options': [
            {
                'name': 'Channel0',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel1',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel2',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel3',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel4',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel5',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel6',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel7',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel8',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel9',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel10',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel11',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel12',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel13',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel14',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel15',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Edge Count Type (Channel0)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel0)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel1)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel1)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel2)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel2)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel3)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel3)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel4)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel4)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel5)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel5)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel6)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel6)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel7)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel7)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel8)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel8)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel9)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel9)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel10)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel10)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel11)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel11)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel12)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel12)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel13)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel13)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel14)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel14)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Channel15)',
                'type': 'choice',
                'values': [('Rising', BrickletIO16V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO16V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO16V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Channel15)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletIO4.DEVICE_DISPLAY_NAME: {
        'class': BrickletIO4,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: value_to_bits(device.get_value(), 4),
                'subvalues': ['Pin 0', 'Pin 1', 'Pin 2', 'Pin 3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Pin 0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 2)',
                'getter': lambda device: device.get_edge_count(2, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Pin 3)',
                'getter': lambda device: device.get_edge_count(3, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, pin0, pin1, pin2, pin3,
                                         edge_count_type_pin0, edge_count_debounce_pin0, \
                                         edge_count_type_pin1, edge_count_debounce_pin1, \
                                         edge_count_type_pin2, edge_count_debounce_pin2, \
                                         edge_count_type_pin3, edge_count_debounce_pin3: \
                          [device.set_configuration(0b0001, *pin0),
                           device.set_configuration(0b0010, *pin1),
                           device.set_configuration(0b0100, *pin2),
                           device.set_configuration(0b1000, *pin3),
                           device.set_edge_count_config(0b0001, edge_count_type_pin0, edge_count_debounce_pin0),
                           device.set_edge_count_config(0b0010, edge_count_type_pin1, edge_count_debounce_pin1),
                           device.set_edge_count_config(0b0100, edge_count_type_pin2, edge_count_debounce_pin2),
                           device.set_edge_count_config(0b1000, edge_count_type_pin3, edge_count_debounce_pin3)],
        'options': [
            {
                'name': 'Pin 0',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin 1',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin 2',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Pin 3',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Edge Count Type (Pin 0)',
                'type': 'choice',
                'values': [('Rising', BrickletIO4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 0)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 1)',
                'type': 'choice',
                'values': [('Rising', BrickletIO4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 1)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 2)',
                'type': 'choice',
                'values': [('Rising', BrickletIO4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 2)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type (Pin 3)',
                'type': 'choice',
                'values': [('Rising', BrickletIO4.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce (Pin 3)',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletIO4V2.DEVICE_DISPLAY_NAME: {
        'class': BrickletIO4V2,
        'values': [
            {
                'name': 'Value',
                'getter': lambda device: device.get_value(),
                'subvalues': ['Channel0', 'Channel1', 'Channel2', 'Channel3'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Edge Count (Channel0)',
                'getter': lambda device: device.get_edge_count(0, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel1)',
                'getter': lambda device: device.get_edge_count(1, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel2)',
                'getter': lambda device: device.get_edge_count(2, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Edge Count (Channel3)',
                'getter': lambda device: device.get_edge_count(3, False),
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device,
                                 channel0,
                                 channel1,
                                 channel2,
                                 channel3,
                                 edge_count_type_channel0,
                                 edge_count_debounce_channel0,
                                 edge_count_type_channel1,
                                 edge_count_debounce_channel1,
                                 edge_count_type_channel2,
                                 edge_count_debounce_channel2,
                                 edge_count_type_channel3,
                                 edge_count_debounce_channel3:
                          [device.set_configuration(0, *channel0),
                           device.set_configuration(1, *channel1),
                           device.set_configuration(2, *channel2),
                           device.set_configuration(3, *channel3),
                           device.set_edge_count_configuration(0, edge_count_type_channel0, edge_count_debounce_channel0),
                           device.set_edge_count_configuration(1, edge_count_type_channel1, edge_count_debounce_channel1),
                           device.set_edge_count_configuration(2, edge_count_type_channel2, edge_count_debounce_channel2),
                           device.set_edge_count_configuration(3, edge_count_type_channel3, edge_count_debounce_channel3)],
        'options': [
            {
                'name': 'Channel0',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel1',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel2',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Channel3',
                'type': 'choice',
                'values': [('Input Pull-Up', ('i', True)),
                           ('Input', ('i', False)),
                           ('Output High', ('o', True)),
                           ('Output Low', ('o', False))],
                'default': 'Input Pull-Up'
            },
            {
                'name': 'Edge Count Type Channel0',
                'type': 'choice',
                'values': [('Rising', BrickletIO4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce Channel0',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type Channel1',
                'type': 'choice',
                'values': [('Rising', BrickletIO4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce Channel1',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type Channel2',
                'type': 'choice',
                'values': [('Rising', BrickletIO4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce Channel2',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            },
            {
                'name': 'Edge Count Type Channel3',
                'type': 'choice',
                'values': [('Rising', BrickletIO4V2.EDGE_TYPE_RISING),
                           ('Falling', BrickletIO4V2.EDGE_TYPE_FALLING),
                           ('Both', BrickletIO4V2.EDGE_TYPE_BOTH)],
                'default': 'Rising'
            },
            {
                'name': 'Edge Count Debounce Channel3',
                'type': 'int',
                'minimum': 0,
                'maximum': 255,
                'suffix': ' ms',
                'default': 100
            }
        ]
    },
    BrickletJoystick.DEVICE_DISPLAY_NAME: {
        'class': BrickletJoystick,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': ['X', 'Y'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Pressed',
                'getter': lambda device: device.is_pressed(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': ['X', 'Y'],
                'unit': [None, None],
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletJoystickV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletJoystickV2,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': ['X', 'Y'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Pressed',
                'getter': lambda device: device.is_pressed(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLEDStrip.DEVICE_DISPLAY_NAME: {
        'class': BrickletLEDStrip,
        'values': [
            {
                'name': 'Supply Voltage',
                'getter': lambda device: device.get_supply_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLEDStripV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletLEDStripV2,
        'values': [
            {
                'name': 'Supply Voltage',
                'getter': lambda device: device.get_supply_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLine.DEVICE_DISPLAY_NAME: {
        'class': BrickletLine,
        'values': [
            {
                'name': 'Reflectivity',
                'getter': lambda device: device.get_reflectivity(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLinearPoti.DEVICE_DISPLAY_NAME: {
        'class': BrickletLinearPoti,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLinearPotiV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletLinearPotiV2,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletMotorizedLinearPoti.DEVICE_DISPLAY_NAME: {
        'class': BrickletMotorizedLinearPoti,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLoadCell.DEVICE_DISPLAY_NAME: {
        'class': BrickletLoadCell,
        'values': [
            {
                'name': 'Weight',
                'getter': lambda device: device.get_weight(),
                'subvalues': None,
                'unit': 'gram',
                'advanced': False
            }
        ],
        'options_setter': lambda device, moving_average_length, rate, gain: \
                          [device.set_moving_average(moving_average_length), device.set_configuration(rate, gain)],
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 1,
                'maximum': 40,
                'suffix': None,
                'default': 4
            },
            {
                'name': 'Rate',
                'type': 'choice',
                'values': [('10Hz', BrickletLoadCell.RATE_10HZ),
                           ('80Hz', BrickletLoadCell.RATE_80HZ)],
                'default': '10Hz'
            },
            {
                'name': 'Gain',
                'type': 'choice',
                'values': [('128x', BrickletLoadCell.GAIN_128X),
                           ('64x', BrickletLoadCell.GAIN_64X),
                           ('32x', BrickletLoadCell.GAIN_32X)],
                'default': '128x'
            }
        ]
    },
    BrickletLoadCellV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletLoadCellV2,
        'values': [
            {
                'name': 'Weight',
                'getter': lambda device: device.get_weight(),
                'subvalues': None,
                'unit': 'gram',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, moving_average_length, rate, gain: \
                          [device.set_moving_average(moving_average_length),
                           device.set_configuration(rate, gain)],
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 1,
                'maximum': 100,
                'suffix': None,
                'default': 4
            },
            {
                'name': 'Rate',
                'type': 'choice',
                'values': [('10Hz', BrickletLoadCellV2.RATE_10HZ),
                           ('80Hz', BrickletLoadCellV2.RATE_80HZ)],
                'default': '10Hz'
            },
            {
                'name': 'Gain',
                'type': 'choice',
                'values': [('128x', BrickletLoadCellV2.GAIN_128X),
                           ('64x', BrickletLoadCellV2.GAIN_64X),
                           ('32x', BrickletLoadCellV2.GAIN_32X)],
                'default': '128x'
            }
        ]
    },
    BrickletMoisture.DEVICE_DISPLAY_NAME: {
        'class': BrickletMoisture,
        'values': [
            {
                'name': 'Moisture Value',
                'getter': lambda device: device.get_moisture_value(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': lambda device, moving_average_length: device.set_moving_average(moving_average_length),
        'options': [
            {
                'name': 'Moving Average Length',
                'type': 'int',
                'minimum': 0,
                'maximum': 100,
                'suffix': None,
                'default': 100
            }
        ]
    },
    BrickletMotionDetector.DEVICE_DISPLAY_NAME: {
        'class': BrickletMotionDetector,
        'values': [
            {
                'name': 'Motion Detected',
                'getter': lambda device: device.get_motion_detected(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletMotionDetectorV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletMotionDetectorV2,
        'values': [
            {
                'name': 'Motion Detected',
                'getter': lambda device: device.get_motion_detected(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletMultiTouch.DEVICE_DISPLAY_NAME: {
        'class': BrickletMultiTouch,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: value_to_bits(device.get_touch_state(), 13),
                'subvalues': ['Electrode 0', 'Electrode 1', 'Electrode 2', 'Electrode 3', 'Electrode 4', 'Electrode 5',
                              'Electrode 6', 'Electrode 7', 'Electrode 8', 'Electrode 9', 'Electrode 10', 'Electrode 11', 'Proximity'],
                'unit': [None, None, None, None, None, None, None, None, None, None, None, None, None],
                'advanced': False
            }
        ],
        'options_setter': special_set_multi_touch_options,
        'options': [
            {
                'name': 'Electrode 0',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 1',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 2',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 3',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 4',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 5',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 6',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 7',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 8',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 9',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 10',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode 11',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Proximity',
                'type': 'bool',
                'default': True
            },
            {
                'name': 'Electrode Sensitivity',
                'type': 'int',
                'minimum': 5,
                'maximum': 201,
                'suffix': None,
                'default': 181
            }
        ]
    },
    BrickletNFC.DEVICE_DISPLAY_NAME: {
        'class': BrickletNFC,
        'values': [
            {
                'name': 'Mode',
                'getter': lambda device: device.get_mode(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Reader State',
                'getter': lambda device: device.reader_get_state(),
                'subvalues': ['State', 'Idle'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Cardemu State',
                'getter': lambda device: device.cardemu_get_state(),
                'subvalues': ['State', 'Idle'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'P2P State',
                'getter': lambda device: device.p2p_get_state(),
                'subvalues': ['State', 'Idle'],
                'unit': [None, None],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletNFCRFID.DEVICE_DISPLAY_NAME: {
        'class': BrickletNFCRFID,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_state(),
                'subvalues': ['State', 'Idle'],
                'unit': [None, None],
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletOutdoorWeather.DEVICE_DISPLAY_NAME: {
        'class': BrickletOutdoorWeather,
        'values': [
            {
                'name': 'Station Data',
                'getter': special_get_station_data,
                'subvalues': ['Temperature', 'Humidity', 'Wind Speed', 'Gust Speed', 'Rain', 'Wind Direction', 'Battery Low', 'Last Change'],
                'unit': ['°C/10', '%RH', 'm/10s', 'm/10s', 'mm/10', None , None, 's'],
                'advanced': False
            },
            {
                'name': 'Sensor Data',
                'getter': special_get_sensor_data,
                'subvalues': ['Temperature', 'Humidity', 'Last Change'],
                'unit': ['°C/10', '%RH', 's'],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletParticulateMatter.DEVICE_DISPLAY_NAME: {
        'class': BrickletParticulateMatter,
        'values': [
            {
                'name': 'Get PM Concentration',
                'getter': lambda device: device.get_pm_concentration(),
                'subvalues': ['PM10', 'PM25', 'PM100'],
                'unit': ['µg/m³', 'µg/m³', 'µg/m³'],
                'advanced': False
            },
            {
                'name': 'Get PM Count',
                'getter': lambda device: device.get_pm_count(),
                'subvalues': ['Greater03um', 'Greater05um', 'Greater10um', 'Greater25um', 'Greater50um', 'Greater100um'],
                'unit': [None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletPTC.DEVICE_DISPLAY_NAME: {
        'class': BrickletPTC,
        'values': [
            {
                'name': 'Temperature',
                'getter': special_get_ptc_temperature,
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Resistance',
                'getter': special_get_ptc_resistance,
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': lambda device, wire_mode: device.set_wire_mode(wire_mode),
        'options': [
            {
                'name': 'Wire Mode',
                'type': 'choice',
                'values': [('2-Wire', BrickletPTC.WIRE_MODE_2),
                           ('3-Wire', BrickletPTC.WIRE_MODE_3),
                           ('4-Wire', BrickletPTC.WIRE_MODE_4)],
                'default': '2-Wire'
            }
        ]
    },
    BrickletPTCV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletPTCV2,
        'values': [
            {
                'name': 'Temperature',
                'getter': special_get_ptc_temperature,
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Resistance',
                'getter': special_get_ptc_resistance,
                'subvalues': None,
                'unit': None,
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, wire_mode: device.set_wire_mode(wire_mode),
        'options': [
            {
                'name': 'Wire Mode',
                'type': 'choice',
                'values': [('2-Wire', BrickletPTCV2.WIRE_MODE_2),
                           ('3-Wire', BrickletPTCV2.WIRE_MODE_3),
                           ('4-Wire', BrickletPTCV2.WIRE_MODE_4)],
                'default': '2-Wire'
            }
        ]
    },
    BrickletRotaryEncoder.DEVICE_DISPLAY_NAME: {
        'class': BrickletRotaryEncoder,
        'values': [
            {
                'name': 'Count',
                'getter': lambda device: device.get_count(False),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Pressed',
                'getter': lambda device: device.is_pressed(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRotaryEncoderV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletRotaryEncoderV2,
        'values': [
            {
                'name': 'Count',
                'getter': lambda device: device.get_count(False),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Pressed',
                'getter': lambda device: device.is_pressed(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRotaryPoti.DEVICE_DISPLAY_NAME: {
        'class': BrickletRotaryPoti,
        'values': [
            {
                'name': 'Position',
                'getter': lambda device: device.get_position(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRS485.DEVICE_DISPLAY_NAME: {
        'class': BrickletRS485,
        'values': [
            {
                'name': 'Error Count',
                'getter': lambda device: device.get_error_count(),
                'subvalues': ['Overrun Error Count', 'Parity Error Count'],
                'unit': [None, None],
                'advanced': True
            },
            {
                'name': 'Modbus Common Error Count',
                'getter': lambda device: device.get_modbus_common_error_count(),
                'subvalues': ['Timeout Error Count',
                              'Checksum Error Count',
                              'Frame Too Big Error Count',
                              'Illegal Function Error Count',
                              'Illegal Data Address Error Count',
                              'Illegal Data Value Error Count',
                              'Slave Device Failure Error Count'],
                'unit': [None, None, None, None, None, None, None],
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSegmentDisplay4x7.DEVICE_DISPLAY_NAME: {
        'class': BrickletSegmentDisplay4x7,
        'values': [
            {
                'name': 'Counter Value',
                'getter': lambda device: device.get_counter_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSegmentDisplay4x7V2.DEVICE_DISPLAY_NAME: {
        'class': BrickletSegmentDisplay4x7V2,
        'values': [
            {
                'name': 'Counter Value',
                'getter': lambda device: device.get_counter_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSolidStateRelay.DEVICE_DISPLAY_NAME: {
        'class': BrickletSolidStateRelay,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSolidStateRelayV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletSolidStateRelayV2,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSoundIntensity.DEVICE_DISPLAY_NAME: {
        'class': BrickletSoundIntensity,
        'values': [
            {
                'name': 'Intensity',
                'getter': lambda device: device.get_intensity(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletSoundPressureLevel.DEVICE_DISPLAY_NAME: {
        'class': BrickletSoundPressureLevel,
        'values': [
            {
                'name': 'Decibel',
                'getter': lambda device: device.get_decibel(),
                'subvalues': None,
                'unit': 'dB/10',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, fft_size, weighting: device.set_configuration(fft_size, weighting),
        'options': [
            {
                'name': 'FFT Range',
                'type': 'choice',
                'values': [('128', BrickletSoundPressureLevel.FFT_SIZE_128),
                           ('256', BrickletSoundPressureLevel.FFT_SIZE_256),
                           ('512', BrickletSoundPressureLevel.FFT_SIZE_512),
                           ('1024', BrickletSoundPressureLevel.FFT_SIZE_1024)],
                'default': '1024'
            },
            {
                'name': 'Weighting',
                'type': 'choice',
                'values': [('A', BrickletSoundPressureLevel.WEIGHTING_A),
                           ('B', BrickletSoundPressureLevel.WEIGHTING_B),
                           ('C', BrickletSoundPressureLevel.WEIGHTING_C),
                           ('D', BrickletSoundPressureLevel.WEIGHTING_D),
                           ('Z', BrickletSoundPressureLevel.WEIGHTING_Z),
                           ('ITU R 468', BrickletSoundPressureLevel.WEIGHTING_ITU_R_468)],
                'default': 'A'
            }
        ]
    },
    BrickletTemperature.DEVICE_DISPLAY_NAME: {
        'class': BrickletTemperature,
        'values': [
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            }
        ],
        'options_setter': lambda device, i2c_mode: device.set_i2c_mode(i2c_mode),
        'options': [
            {
                'name': 'I2C Mode',
                'type': 'choice',
                'values': [('400kHz', BrickletTemperature.I2C_MODE_FAST),
                           ('100kHz', BrickletTemperature.I2C_MODE_SLOW)],
                'default': '400kHz'
            }
        ]
    },
    BrickletTemperatureV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletTemperatureV2,
        'values': [
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletThermalImaging.DEVICE_DISPLAY_NAME: {
        'class': BrickletThermalImaging,
        'values': [
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletThermocouple.DEVICE_DISPLAY_NAME: {
        'class': BrickletThermocouple,
        'values': [
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Error State',
                'getter': lambda device: device.get_error_state(),
                'subvalues': ['Over/Under Voltage', 'Open Circuit'],
                'unit': [None, None],
                'advanced': True
            }
        ],
        'options_setter': lambda device, averaging, thermocouple_type, filter: \
                          device.set_configuration(averaging, thermocouple_type, filter),
        'options': [
            {
                'name': 'Averaging',
                'type': 'choice',
                'values': [('1', BrickletThermocouple.AVERAGING_1),
                           ('2', BrickletThermocouple.AVERAGING_2),
                           ('4', BrickletThermocouple.AVERAGING_4),
                           ('8', BrickletThermocouple.AVERAGING_8),
                           ('16', BrickletThermocouple.AVERAGING_16)],
                'default': '16'
            },
            {
                'name': 'Thermocouple Type',
                'type': 'choice',
                'values': [('B', BrickletThermocouple.TYPE_B),
                           ('E', BrickletThermocouple.TYPE_E),
                           ('J', BrickletThermocouple.TYPE_J),
                           ('K', BrickletThermocouple.TYPE_K),
                           ('N', BrickletThermocouple.TYPE_N),
                           ('R', BrickletThermocouple.TYPE_R),
                           ('S', BrickletThermocouple.TYPE_S),
                           ('T', BrickletThermocouple.TYPE_T),
                           ('G8', BrickletThermocouple.TYPE_G8),
                           ('G32', BrickletThermocouple.TYPE_G32)],
                'default': 'K'
            },
            {
                'name': 'Filter',
                'type': 'choice',
                'values': [('50Hz', BrickletThermocouple.FILTER_OPTION_50HZ),
                           ('60Hz', BrickletThermocouple.FILTER_OPTION_60HZ)],
                'default': '50Hz'
            }
        ]
    },
    BrickletThermocoupleV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletThermocoupleV2,
        'values': [
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': False
            },
            {
                'name': 'Error State',
                'getter': lambda device: device.get_error_state(),
                'subvalues': ['Over/Under Voltage', 'Open Circuit'],
                'unit': [None, None],
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }

        ],
        'options_setter': lambda device, averaging, thermocouple_type, filter: \
                          device.set_configuration(averaging, thermocouple_type, filter),
        'options': [
            {
                'name': 'Averaging',
                'type': 'choice',
                'values': [('1', BrickletThermocouple.AVERAGING_1),
                           ('2', BrickletThermocouple.AVERAGING_2),
                           ('4', BrickletThermocouple.AVERAGING_4),
                           ('8', BrickletThermocouple.AVERAGING_8),
                           ('16', BrickletThermocouple.AVERAGING_16)],
                'default': '16'
            },
            {
                'name': 'Thermocouple Type',
                'type': 'choice',
                'values': [('B', BrickletThermocouple.TYPE_B),
                           ('E', BrickletThermocouple.TYPE_E),
                           ('J', BrickletThermocouple.TYPE_J),
                           ('K', BrickletThermocouple.TYPE_K),
                           ('N', BrickletThermocouple.TYPE_N),
                           ('R', BrickletThermocouple.TYPE_R),
                           ('S', BrickletThermocouple.TYPE_S),
                           ('T', BrickletThermocouple.TYPE_T),
                           ('G8', BrickletThermocouple.TYPE_G8),
                           ('G32', BrickletThermocouple.TYPE_G32)],
                'default': 'K'
            },
            {
                'name': 'Filter',
                'type': 'choice',
                'values': [('50Hz', BrickletThermocouple.FILTER_OPTION_50HZ),
                           ('60Hz', BrickletThermocouple.FILTER_OPTION_60HZ)],
                'default': '50Hz'
            }
        ]
    },
    BrickletTemperatureIR.DEVICE_DISPLAY_NAME: {
        'class': BrickletTemperatureIR,
        'values': [
            {
                'name': 'Ambient Temperature',
                'getter': lambda device: device.get_ambient_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': False
            },
            {
                'name': 'Object Temperature',
                'getter': lambda device: device.get_object_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': False
            }
        ],
        'options_setter': lambda device, emissivity: device.set_emissivity(emissivity),
        'options': [
            {
                'name': 'Emissivity',
                'type': 'int',
                'minimum': 6553,
                'maximum': 65535,
                'suffix': None,
                'default': 65535
            }
        ]
    },
    BrickletTemperatureIRV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletTemperatureIRV2,
        'values': [
            {
                'name': 'Ambient Temperature',
                'getter': lambda device: device.get_ambient_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': False
            },
            {
                'name': 'Object Temperature',
                'getter': lambda device: device.get_object_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': lambda device, emissivity: device.set_emissivity(emissivity),
        'options': [
            {
                'name': 'Emissivity',
                'type': 'int',
                'minimum': 6553,
                'maximum': 65535,
                'suffix': None,
                'default': 65535
            }
        ]
    },
    BrickletTilt.DEVICE_DISPLAY_NAME: {
        'class': BrickletTilt,
        'values': [
            {
                'name': 'State',
                'getter': lambda device: device.get_tilt_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletUVLight.DEVICE_DISPLAY_NAME: {
        'class': BrickletUVLight,
        'values': [
            {
                'name': 'UV Light',
                'getter': lambda device: device.get_uv_light(),
                'subvalues': None,
                'unit': 'µW/cm²',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletUVLightV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletUVLightV2,
        'values': [
            {
                'name': 'UVA',
                'getter': lambda device: device.get_uva(),
                'subvalues': None,
                'unit': '1/10 mW/m²',
                'advanced': False
            },
            {
                'name': 'UVB',
                'getter': lambda device: device.get_uvb(),
                'subvalues': None,
                'unit': '1/10 mW/m²',
                'advanced': False
            },
            {
                'name': 'UVI',
                'getter': lambda device: device.get_uvi(),
                'subvalues': None,
                'unit': '1/10',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, integration_time: device.set_configuration(integration_time),
        'options': [
            {
                'name': 'Integration Time',
                'type': 'choice',
                'values': [('50ms', BrickletUVLightV2.INTEGRATION_TIME_50MS),
                           ('100ms', BrickletUVLightV2.INTEGRATION_TIME_100MS),
                           ('200ms', BrickletUVLightV2.INTEGRATION_TIME_200MS),
                           ('400ms', BrickletUVLightV2.INTEGRATION_TIME_400MS),
                           ('800ms', BrickletUVLightV2.INTEGRATION_TIME_800MS)],
                'default': '400ms'
            }
        ]
    },
    BrickletVoltage.DEVICE_DISPLAY_NAME: {
        'class': BrickletVoltage,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Analog Value',
                'getter': lambda device: device.get_analog_value(),
                'subvalues': None,
                'unit': None,
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletVoltageCurrent.DEVICE_DISPLAY_NAME: {
        'class': BrickletVoltageCurrent,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Current',
                'getter': lambda device: device.get_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Power',
                'getter': lambda device: device.get_power(),
                'subvalues': None,
                'unit': 'mW',
                'advanced': False
            }
        ],
        'options_setter': lambda device, average_length, voltage_conversion_time, current_conversion_time: \
                          device.set_configuration(average_length, voltage_conversion_time, current_conversion_time),
        'options': [
            {
                'name': 'Average Length',
                'type': 'choice',
                'values': [('1', BrickletVoltageCurrent.AVERAGING_1),
                           ('4', BrickletVoltageCurrent.AVERAGING_4),
                           ('16', BrickletVoltageCurrent.AVERAGING_16),
                           ('64', BrickletVoltageCurrent.AVERAGING_64),
                           ('128', BrickletVoltageCurrent.AVERAGING_128),
                           ('256', BrickletVoltageCurrent.AVERAGING_256),
                           ('512', BrickletVoltageCurrent.AVERAGING_512),
                           ('1024', BrickletVoltageCurrent.AVERAGING_1024)],
                'default': '64'
            },
            {
                'name': 'Voltage Conversion Time',
                'type': 'choice',
                'values': [('140µs', 0),
                           ('204µs', 1),
                           ('332µs', 2),
                           ('588µs', 3),
                           ('1.1ms', 4),
                           ('2.116ms', 5),
                           ('4.156ms', 6),
                           ('8.244ms', 7)],
                'default': '1.1ms'
            },
            {
                'name': 'Current Conversion Time',
                'type': 'choice',
                'values': [('140µs', 0),
                           ('204µs', 1),
                           ('332µs', 2),
                           ('588µs', 3),
                           ('1.1ms', 4),
                           ('2.116ms', 5),
                           ('4.156ms', 6),
                           ('8.244ms', 7)],
                'default': '1.1ms'
            }
        ]
    },
    BrickletVoltageCurrentV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletVoltageCurrentV2,
        'values': [
            {
                'name': 'Voltage',
                'getter': lambda device: device.get_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Current',
                'getter': lambda device: device.get_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Power',
                'getter': lambda device: device.get_power(),
                'subvalues': None,
                'unit': 'mW',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': lambda device, average_length, voltage_conversion_time, current_conversion_time: \
                          device.set_configuration(average_length, voltage_conversion_time, current_conversion_time),
        'options': [
            {
                'name': 'Average Length',
                'type': 'choice',
                'values': [('1', BrickletVoltageCurrent.AVERAGING_1),
                           ('4', BrickletVoltageCurrent.AVERAGING_4),
                           ('16', BrickletVoltageCurrent.AVERAGING_16),
                           ('64', BrickletVoltageCurrent.AVERAGING_64),
                           ('128', BrickletVoltageCurrent.AVERAGING_128),
                           ('256', BrickletVoltageCurrent.AVERAGING_256),
                           ('512', BrickletVoltageCurrent.AVERAGING_512),
                           ('1024', BrickletVoltageCurrent.AVERAGING_1024)],
                'default': '64'
            },
            {
                'name': 'Voltage Conversion Time',
                'type': 'choice',
                'values': [('140µs', 0),
                           ('204µs', 1),
                           ('332µs', 2),
                           ('588µs', 3),
                           ('1.1ms', 4),
                           ('2.116ms', 5),
                           ('4.156ms', 6),
                           ('8.244ms', 7)],
                'default': '1.1ms'
            },
            {
                'name': 'Current Conversion Time',
                'type': 'choice',
                'values': [('140µs', 0),
                           ('204µs', 1),
                           ('332µs', 2),
                           ('588µs', 3),
                           ('1.1ms', 4),
                           ('2.116ms', 5),
                           ('4.156ms', 6),
                           ('8.244ms', 7)],
                'default': '1.1ms'
            }
        ]
    },
    BrickDC.DEVICE_DISPLAY_NAME: {
        'class': BrickDC,
        'values': [
            {
                'name': 'Stack Input Voltage',
                'getter': lambda device: device.get_stack_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'External Input Voltage',
                'getter': lambda device: device.get_external_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Current Consumption',
                'getter': lambda device: device.get_current_consumption(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickIMU.DEVICE_DISPLAY_NAME: {
        'class': BrickIMU,
        'values': [
            {
                'name': 'Orientation',
                'getter': lambda device: device.get_orientation(),
                'subvalues': ['Roll', 'Pitch', 'Yaw'],
                'unit': ['°/100', '°/100', '°/100'],
                'advanced': False
            },
            {
                'name': 'Quaternion',
                'getter': lambda device: device.get_quaternion(),
                'subvalues': ['X', 'Y', 'Z', 'W'],
                'unit': [None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Acceleration',
                'getter': lambda device: device.get_acceleration(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['g/1000', 'g/1000', 'g/1000'],
                'advanced': True
            },
            {
                'name': 'Magnetic Field',
                'getter': lambda device: device.get_magnetic_field(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['G/1000', 'G/1000', 'G/1000'],
                'advanced': True
            },
            {
                'name': 'Angular Velocity',
                'getter': lambda device: device.get_angular_velocity(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['8/115 °/s', '8/115 °/s', '8/115 °/s'],
                'advanced': True
            },
            {
                'name': 'IMU Temperature',
                'getter': lambda device: device.get_imu_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': True
            },
            {
                'name': 'All Data',
                'getter': lambda device: device.get_all_data(),
                'subvalues': ['Acceleration-X', 'Acceleration-Y', 'Acceleration-Z', 'Acceleration-X', 'Acceleration-Y', 'Acceleration-Z',
                              'Angular Velocity-X', 'Angular Velocity-Y', 'Angular Velocity-Z', 'IMU Temperature'],
                'unit': ['g/1000', 'g/1000', 'g/1000', 'G/1000', 'G/1000', 'G/1000', '8/115 °/s', '8/115 °/s', '8/115 °/s', '°C/100'],
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None # FIXME: ranges
    },
    BrickIMUV2.DEVICE_DISPLAY_NAME: {
        'class': BrickIMUV2,
        'values': [
            {
                'name': 'Orientation',
                'getter': lambda device: device.get_orientation(),
                'subvalues': ['Heading', 'Roll', 'Pitch'],
                'unit': ['°/16', '°/16', '°/16'],
                'advanced': False
            },
            {
                'name': 'Linear Acceleration',
                'getter': lambda device: device.get_linear_acceleration(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['1/100 m/s²', '1/100 m/s²', '1/100 m/s²'],
                'advanced': False
            },
            {
                'name': 'Gravity Vector',
                'getter': lambda device: device.get_gravity_vector(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['1/100 m/s²', '1/100 m/s²', '1/100 m/s²'],
                'advanced': False
            },
            {
                'name': 'Quaternion',
                'getter': lambda device: device.get_quaternion(),
                'subvalues': ['W', 'X', 'Y', 'Z'],
                'unit': ['1/16383', '1/16383', '1/16383', '1/16383'],
                'advanced': False
            },
            {
                'name': 'Acceleration',
                'getter': lambda device: device.get_acceleration(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['1/100 m/s²', '1/100 m/s²', '1/100 m/s²'],
                'advanced': True
            },
            {
                'name': 'Magnetic Field',
                'getter': lambda device: device.get_magnetic_field(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['1/16 µT ', '1/16 µT ', '1/16 µT '],
                'advanced': True
            },
            {
                'name': 'Angular Velocity',
                'getter': lambda device: device.get_angular_velocity(),
                'subvalues': ['X', 'Y', 'Z'],
                'unit': ['1/16 °/s', '1/16 °/s', '1/16 °/s'],
                'advanced': True
            },
            {
                'name': 'Temperature',
                'getter': lambda device: device.get_temperature(),
                'subvalues': None,
                'unit': '°C/100',
                'advanced': True
            },
            #{
            #    'name': 'All Data',
            #    'getter': lambda device: device.get_all_data(),
            #    'subvalues': # FIXME: nested arrays
            #    'unit': # FIXME: nested arrays
            #    'advanced': False
            #},
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None # FIXME: ranges
    },
    BrickMaster.DEVICE_DISPLAY_NAME: {
        'class': BrickMaster,
        'values': [
            {
                'name': 'Stack Voltage',
                'getter': lambda device: device.get_stack_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Stack Current',
                'getter': lambda device: device.get_stack_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickServo.DEVICE_DISPLAY_NAME: {
        'class': BrickServo,
        'values': [
            {
                'name': 'Servo Current (Servo 0)',
                'getter': lambda device: device.get_servo_current(0),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 1)',
                'getter': lambda device: device.get_servo_current(1),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 2)',
                'getter': lambda device: device.get_servo_current(2),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 3)',
                'getter': lambda device: device.get_servo_current(3),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 4)',
                'getter': lambda device: device.get_servo_current(4),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 5)',
                'getter': lambda device: device.get_servo_current(5),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Servo Current (Servo 6)',
                'getter': lambda device: device.get_servo_current(6),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Overall Current',
                'getter': lambda device: device.get_overall_current(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': False
            },
            {
                'name': 'Stack Input Voltage',
                'getter': lambda device: device.get_stack_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'External Input Voltage',
                'getter': lambda device: device.get_external_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickStepper.DEVICE_DISPLAY_NAME: {
        'class': BrickStepper,
        'values': [
            {
                'name': 'Current Velocity',
                'getter': lambda device: device.get_current_velocity(),
                'subvalues': None,
                'unit': 'steps/sec',
                'advanced': False
            },
            {
                'name': 'Current Position',
                'getter': lambda device: device.get_current_position(),
                'subvalues': None,
                'unit': 'steps',
                'advanced': True
            },
            {
                'name': 'Stack Input Voltage',
                'getter': lambda device: device.get_stack_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': True
            },
            {
                'name': 'External Input Voltage',
                'getter': lambda device: device.get_external_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': True
            },
            {
                'name': 'Current Consumption',
                'getter': lambda device: device.get_current_consumption(),
                'subvalues': None,
                'unit': 'mA',
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickSilentStepper.DEVICE_DISPLAY_NAME: {
        'class': BrickSilentStepper,
        'values': [
            {
                'name': 'Current Velocity',
                'getter': lambda device: device.get_current_velocity(),
                'subvalues': None,
                'unit': 'steps/sec',
                'advanced': False
            },
            {
                'name': 'Current Position',
                'getter': lambda device: device.get_current_position(),
                'subvalues': None,
                'unit': 'steps',
                'advanced': True
            },
            {
                'name': 'Stack Input Voltage',
                'getter': lambda device: device.get_stack_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': True
            },
            {
                'name': 'External Input Voltage',
                'getter': lambda device: device.get_external_input_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': True
            },
            {
                'name': 'Current Consumption',
                'getter': lambda device: special_get_silent_stepper_current_consumption(device),
                'subvalues': None,
                'unit': 'mA',
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C/10',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRGBLEDButton.DEVICE_DISPLAY_NAME: {
        'class': BrickletRGBLEDButton,
        'values': [
            {
                'name': 'Button State',
                'getter': lambda device: device.get_button_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRGBLEDMatrix.DEVICE_DISPLAY_NAME: {
        'class': BrickletRGBLEDMatrix,
        'values': [
            {
                'name': 'Supply Voltage',
                'getter': lambda device: device.get_supply_voltage(),
                'subvalues': None,
                'unit': 'mV',
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRealTimeClock.DEVICE_DISPLAY_NAME: {
        'class': BrickletRealTimeClock,
        'values': [
            {
                'name': 'Date Time',
                'getter': lambda device: device.get_date_time(),
                'subvalues': ['Year',
                              'Month',
                              'Day',
                              'Hour',
                              'Minute',
                              'Second',
                              'Centisecond',
                              'Weekday'],
                'unit': [None, None, None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Timestamp',
                'getter': lambda device: device.get_timestamp(),
                'subvalues': None,
                'unit': 'ms',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRealTimeClockV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletRealTimeClockV2,
        'values': [
            {
                'name': 'Date Time',
                'getter': lambda device: device.get_date_time(),
                'subvalues': ['Year',
                              'Month',
                              'Day',
                              'Hour',
                              'Minute',
                              'Second',
                              'Centisecond',
                              'Weekday'],
                'unit': [None, None, None, None, None, None, None, None],
                'advanced': False
            },
            {
                'name': 'Timestamp',
                'getter': lambda device: device.get_timestamp(),
                'subvalues': None,
                'unit': 'ms',
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRemoteSwitch.DEVICE_DISPLAY_NAME: {
        'class': BrickletRemoteSwitch,
        'values': [
            {
                'name': 'Switching State',
                'getter': lambda device: device.get_switching_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletRemoteSwitchV2.DEVICE_DISPLAY_NAME: {
        'class': BrickletRemoteSwitchV2,
        'values': [
            {
                'name': 'Switching State',
                'getter': lambda device: device.get_switching_state(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Remote Status A',
                'getter': lambda device: device.get_remote_status_a(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Remote Status B',
                'getter': lambda device: device.get_remote_status_b(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Remote Status C',
                'getter': lambda device: device.get_remote_status_c(),
                'subvalues': None,
                'unit': None,
                'advanced': False
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletLaserRangeFinder.DEVICE_DISPLAY_NAME: {
        'class': BrickletLaserRangeFinder,
        'values': [
            {
                'name': 'Distance',
                'getter': lambda device: device.get_distance(),
                'subvalues': None,
                'unit': 'cm',
                'advanced': False
            },
            {
                'name': 'Velocity',
                'getter': lambda device: device.get_velocity(),
                'subvalues': None,
                'unit': '1/100 m/s',
                'advanced': False
            }
        ],
        'options_setter': None,
        'options': None
    },
    BrickletDMX.DEVICE_DISPLAY_NAME: {
        'class': BrickletDMX,
        'values': [
            {
                'name': 'Frame Error Count',
                'getter': lambda device: device.get_frame_error_count(),
                'subvalues': ['Overrun Error Count', 'Framing Error Count'],
                'unit': [None, None],
                'advanced': True
            },
            {
                'name': 'Chip Temperature',
                'getter': lambda device: device.get_chip_temperature(),
                'subvalues': None,
                'unit': '°C',
                'advanced': True
            }
        ],
        'options_setter': None,
        'options': None
    }
}

'''
/*---------------------------------------------------------------------------
                                AbstractDevice
 ---------------------------------------------------------------------------*/
 '''

class AbstractDevice:
    """DEBUG and Inheritance only class"""

    def __init__(self, data, datalogger):
        self.datalogger = datalogger
        self.data = data

        self.__name__ = "AbstractDevice"

    def start_timer(self):
        """
        Starts all timer for all loggable variables of the devices.
        """
        EventLogger.debug(self.__str__())

    def _exception_msg(self, value, msg):
        """
        For a uniform creation of Exception messages.
        """
        return "ERROR[" + str(value) + "]: " + str(msg)

    def __str__(self):
        """
        Representation String of the class. For simple overwiev.
        """
        return "[" + str(self.__name__) + "]"


#---------------------------------------------------------------------------
#                               DeviceImpl
#---------------------------------------------------------------------------

class DeviceImpl(AbstractDevice):
    """
    A SimpleDevice is every device, which only has funtion with one return value.
    """

    def __init__(self, data, datalogger):
        super().__init__(data, datalogger)

        self.device_name = self.data['name']
        self.device_uid = self.data['uid']
        self.device_spec = device_specs[self.device_name]
        device_class = self.device_spec['class']
        self.device = device_class(self.device_uid, self.datalogger.ipcon)

        self.__name__ = "devices:" + str(self.device_name)

    def start_timer(self):
        AbstractDevice.start_timer(self)

        for value in self.data['values']:
            interval = self.data['values'][value]['interval']
            func_name = "_timer"
            var_name = value

            self.datalogger.timers.append(LoggerTimer(interval, func_name, var_name, self))

    def apply_options(self):
        options_setter = self.device_spec['options_setter']
        option_specs = self.device_spec['options']

        if options_setter != None and option_specs != None:
            EventLogger.debug('Applying options for "{0}" with UID "{1}"'.format(self.device_name, self.device_uid))

            args = []

            for option_spec in option_specs:
                for option_name in self.data['options']:
                    if option_name == option_spec['name']:
                        option_value = self.data['options'][option_name]['value']

                        if option_spec['type'] == 'choice':
                            for option_value_spec in option_spec['values']:
                                if option_value == option_value_spec[0]:
                                    args.append(option_value_spec[1])
                        elif option_spec['type'] == 'int':
                            args.append(option_value)
                        elif option_spec['type'] == 'bool':
                            args.append(option_value)

            try:
                options_setter(self.device, *tuple(args))
            except Exception as e:
                EventLogger.warning('Could not apply options for "{0}" with UID "{1}": {2}'
                                    .format(self.device_name, self.device_uid, e))

    def _timer(self, var_name):
        """
        This function is used by the LoggerTimer to get the variable values from the brickd.
        In SimpleDevices the get-functions only return one value.
        """

        for value_spec in self.device_spec['values']:
            if value_spec['name'] == var_name:
                break

        getter = value_spec['getter']
        subvalue_names = value_spec['subvalues']
        unit = value_spec['unit']
        now = time.time()
        time_format = self.datalogger._config['data']['time_format']
        time_format_strftime = self.datalogger._config['data']['time_format_strftime']

        if time_format == 'de':
            timestamp = timestamp_to_de(now)
        elif time_format == 'de-msec':
            timestamp = timestamp_to_de_msec(now)
        elif time_format == 'us':
            timestamp = timestamp_to_us(now)
        elif time_format == 'us-msec':
            timestamp = timestamp_to_us_msec(now)
        elif time_format == 'iso':
            timestamp = timestamp_to_iso(now)
        elif time_format == 'iso-msec':
            timestamp = timestamp_to_iso_msec(now)
        elif time_format == 'unix':
            timestamp = timestamp_to_unix(now)
        elif time_format == 'unix-msec':
            timestamp = timestamp_to_unix_msec(now)
        elif time_format == 'strftime':
            timestamp = timestamp_to_strftime(now, time_format_strftime)
        else:
            timestamp = timestamp_to_unix(now)

        try:
            value = getter(self.device)
        except Exception as e:
            value = self._exception_msg(self.device_name + "-" + var_name, e)
            self.datalogger.add_to_queue(CSVData(timestamp,
                                                 self.device_name,
                                                 self.device_uid,
                                                 var_name,
                                                 value,
                                                 ''))
            # log_exception(timestamp, value_name, e)
            return

        if not isinstance(value, dict):
            value = {None: value}

        try:
            if subvalue_names is None:
                if unit == None:
                    unit_str = ''
                else:
                    unit_str = unit

                for key, keyed_value in value.items():
                    if key != None:
                        keyed_var_name = var_name + ':' + key
                    else:
                        keyed_var_name = var_name

                    self.datalogger.add_to_queue(CSVData(timestamp,
                                                         self.device_name,
                                                         self.device_uid,
                                                         keyed_var_name,
                                                         keyed_value,
                                                         unit_str))
            else:
                subvalue_bool = self.data['values'][var_name]['subvalues']

                for key, keyed_value in value.items():
                    if key != None:
                        keyed_var_name = var_name + ':' + key
                    else:
                        keyed_var_name = var_name

                    for i in range(len(subvalue_names)):
                        if not isinstance(subvalue_names[i], list):
                            try:
                                if subvalue_bool[subvalue_names[i]]:
                                    if unit[i] == None:
                                        unit_str = ''
                                    else:
                                        unit_str = unit[i]

                                    self.datalogger.add_to_queue(CSVData(timestamp,
                                                                         self.device_name,
                                                                         self.device_uid,
                                                                         keyed_var_name + "-" + subvalue_names[i],
                                                                         keyed_value[i],
                                                                         unit_str))
                            except Exception as e:
                                err_value = self._exception_msg(self.device_name + "-" + keyed_var_name, e)
                                self.datalogger.add_to_queue(CSVData(timestamp,
                                                                     self.device_name,
                                                                     self.device_uid,
                                                                     keyed_var_name + "-" + subvalue_names[i],
                                                                     err_value,
                                                                     ''))
                                return
                        else:
                            for k in range(len(subvalue_names[i])):
                                try:
                                    if subvalue_bool[subvalue_names[i][k]]:
                                        if unit[i][k] == None:
                                            unit_str = ''
                                        else:
                                            unit_str = unit[i][k]

                                        self.datalogger.add_to_queue(CSVData(timestamp,
                                                                             self.device_name,
                                                                             self.device_uid,
                                                                             keyed_var_name + "-" + subvalue_names[i][k],
                                                                             keyed_value[i][k],
                                                                             unit_str))
                                except Exception as e:
                                    err_value = self._exception_msg(str(self.device_name) + "-" + keyed_var_name, e)
                                    self.datalogger.add_to_queue(CSVData(timestamp,
                                                                         self.device_name,
                                                                         self.device_uid,
                                                                         keyed_var_name + "-" + subvalue_names[i][k],
                                                                         err_value,
                                                                         ''))
                                    return

        except Exception as e:
            err_value = self._exception_msg(self.device_name + "-" + var_name, e)
            self.datalogger.add_to_queue(CSVData(timestamp,
                                                 self.device_name,
                                                 self.device_uid,
                                                 var_name,
                                                 err_value,
                                                 ''))
