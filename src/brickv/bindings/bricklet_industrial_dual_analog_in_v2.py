# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-12-05.      #
#                                                           #
# Python Bindings Version 2.1.24                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetVoltageCallbackConfiguration = namedtuple('VoltageCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetCalibration = namedtuple('Calibration', ['offset', 'gain'])
GetChannelLEDStatusConfig = namedtuple('ChannelLEDStatusConfig', ['min', 'max', 'config'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletIndustrialDualAnalogInV2(Device):
    """
    Measures two DC voltages between -35V and +35V with 24bit resolution each
    """

    DEVICE_IDENTIFIER = 2121
    DEVICE_DISPLAY_NAME = 'Industrial Dual Analog In Bricklet 2.0'
    DEVICE_URL_PART = 'industrial_dual_analog_in_v2' # internal

    CALLBACK_VOLTAGE = 4


    FUNCTION_GET_VOLTAGE = 1
    FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION = 3
    FUNCTION_SET_SAMPLE_RATE = 5
    FUNCTION_GET_SAMPLE_RATE = 6
    FUNCTION_SET_CALIBRATION = 7
    FUNCTION_GET_CALIBRATION = 8
    FUNCTION_GET_ADC_VALUES = 9
    FUNCTION_SET_CHANNEL_LED_CONFIG = 10
    FUNCTION_GET_CHANNEL_LED_CONFIG = 11
    FUNCTION_SET_CHANNEL_LED_STATUS_CONFIG = 12
    FUNCTION_GET_CHANNEL_LED_STATUS_CONFIG = 13
    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_SET_STATUS_LED_CONFIG = 239
    FUNCTION_GET_STATUS_LED_CONFIG = 240
    FUNCTION_GET_CHIP_TEMPERATURE = 242
    FUNCTION_RESET = 243
    FUNCTION_WRITE_UID = 248
    FUNCTION_READ_UID = 249
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    SAMPLE_RATE_976_SPS = 0
    SAMPLE_RATE_488_SPS = 1
    SAMPLE_RATE_244_SPS = 2
    SAMPLE_RATE_122_SPS = 3
    SAMPLE_RATE_61_SPS = 4
    SAMPLE_RATE_4_SPS = 5
    SAMPLE_RATE_2_SPS = 6
    SAMPLE_RATE_1_SPS = 7
    CHANNEL_LED_CONFIG_OFF = 0
    CHANNEL_LED_CONFIG_ON = 1
    CHANNEL_LED_CONFIG_SHOW_HEARTBEAT = 2
    CHANNEL_LED_CONFIG_SHOW_CHANNEL_STATUS = 3
    CHANNEL_LED_STATUS_CONFIG_THRESHOLD = 0
    CHANNEL_LED_STATUS_CONFIG_INTENSITY = 1
    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4
    BOOTLOADER_STATUS_OK = 0
    BOOTLOADER_STATUS_INVALID_MODE = 1
    BOOTLOADER_STATUS_NO_CHANGE = 2
    BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3
    BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4
    BOOTLOADER_STATUS_CRC_MISMATCH = 5
    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_VOLTAGE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_SAMPLE_RATE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_SAMPLE_RATE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CALIBRATION] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CALIBRATION] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_ADC_VALUES] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CHANNEL_LED_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHANNEL_LED_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CHANNEL_LED_STATUS_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHANNEL_LED_STATUS_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_WRITE_FIRMWARE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_RESET] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_WRITE_UID] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_READ_UID] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIndustrialDualAnalogInV2.FUNCTION_GET_IDENTITY] = BrickletIndustrialDualAnalogInV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletIndustrialDualAnalogInV2.CALLBACK_VOLTAGE] = 'B i'


    def get_voltage(self, channel):
        """
        Returns the voltage for the given channel.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Voltage` callback. You can set the callback configuration
        with :func:`Set Voltage Callback Configuration`.
        """
        channel = int(channel)

        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_VOLTAGE, (channel,), 'B', 'i')

    def set_voltage_callback_configuration(self, channel, period, value_has_to_change, option, min, max):
        """
        The period is the period with which the :cb:`Voltage` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Voltage` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.
        """
        channel = int(channel)
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION, (channel, period, value_has_to_change, option, min, max), 'B I ! c i i', '')

    def get_voltage_callback_configuration(self, channel):
        """
        Returns the callback configuration as set by :func:`Set Voltage Callback Configuration`.
        """
        channel = int(channel)

        return GetVoltageCallbackConfiguration(*self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION, (channel,), 'B', 'I ! c i i'))

    def set_sample_rate(self, rate):
        """
        Sets the sample rate. The sample rate can be between 1 sample per second
        and 976 samples per second. Decreasing the sample rate will also decrease the
        noise on the data.
        """
        rate = int(rate)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_SAMPLE_RATE, (rate,), 'B', '')

    def get_sample_rate(self):
        """
        Returns the sample rate as set by :func:`Set Sample Rate`.
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_SAMPLE_RATE, (), '', 'B')

    def set_calibration(self, offset, gain):
        """
        Sets offset and gain of MCP3911 internal calibration registers.

        See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet 2.0
        is already factory calibrated by Tinkerforge. It should not be necessary
        for you to use this function
        """
        offset = list(map(int, offset))
        gain = list(map(int, gain))

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CALIBRATION, (offset, gain), '2i 2i', '')

    def get_calibration(self):
        """
        Returns the calibration as set by :func:`Set Calibration`.
        """
        return GetCalibration(*self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CALIBRATION, (), '', '2i 2i'))

    def get_adc_values(self):
        """
        Returns the ADC values as given by the MCP3911 IC. This function
        is needed for proper calibration, see :func:`Set Calibration`.
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_ADC_VALUES, (), '', '2i')

    def set_channel_led_config(self, channel, config):
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a
        heartbeat. You can also set the LED to "Channel Status". In this mode the
        LED can either be turned on with a pre-defined threshold or the intensity
        of the LED can change with the measured value.

        You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

        By default all channel LEDs are configured as "Channel Status".
        """
        channel = int(channel)
        config = int(config)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CHANNEL_LED_CONFIG, (channel, config), 'B B', '')

    def get_channel_led_config(self, channel):
        """
        Returns the channel LED configuration as set by :func:`Set Channel LED Config`
        """
        channel = int(channel)

        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHANNEL_LED_CONFIG, (channel,), 'B', 'B')

    def set_channel_led_status_config(self, channel, min, max, config):
        """
        Sets the channel LED status config. This config is used if the channel LED is
        configured as "Channel Status", see :func:`Set Channel LED Config`.

        For each channel you can choose between threshold and intensity mode.

        In threshold mode you can define a positive or a negative threshold.
        For a positive threshold set the "min" parameter to the threshold value in mV
        above which the LED should turn on and set the "max" parameter to 0. Example:
        If you set a positive threshold of 10V, the LED will turn on as soon as the
        voltage exceeds 10V and turn off again if it goes below 10V.
        For a negative threshold set the "max" parameter to the threshold value in mV
        below which the LED should turn on and set the "min" parameter to 0. Example:
        If you set a negative threshold of 10V, the LED will turn on as soon as the
        voltage goes below 10V and the LED will turn off when the voltage exceeds 10V.

        In intensity mode you can define a range in mV that is used to scale the brightness
        of the LED. Example with min=4V, max=20V: The LED is off at 4V, on at 20V
        and the brightness is linearly scaled between the values 4V and 20V. If the
        min value is greater than the max value, the LED brightness is scaled the other
        way around.
        """
        channel = int(channel)
        min = int(min)
        max = int(max)
        config = int(config)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_CHANNEL_LED_STATUS_CONFIG, (channel, min, max, config), 'B i i B', '')

    def get_channel_led_status_config(self, channel):
        """
        Returns the channel LED status configuration as set by
        :func:`Set Channel LED Status Config`.
        """
        channel = int(channel)

        return GetChannelLEDStatusConfig(*self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHANNEL_LED_STATUS_CONFIG, (channel,), 'B', 'i i B'))

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier and CRC are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        mode = int(mode)

        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c', 'd', 'e', 'f', 'g' or 'h' (Bricklet Port).
        The Raspberry Pi HAT (Zero) Brick is always at position 'i' and the Bricklet
        connected to an :ref:`Isolator Bricklet <isolator_bricklet>` is always as
        position 'z'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletIndustrialDualAnalogInV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

IndustrialDualAnalogInV2 = BrickletIndustrialDualAnalogInV2 # for backward compatibility
