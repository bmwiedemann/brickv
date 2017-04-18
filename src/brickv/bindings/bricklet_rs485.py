# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2017-04-18.      #
#                                                           #
# Python Bindings Version 2.1.11                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

ReadLowLevel = namedtuple('ReadLowLevel', ['stream_total_length', 'stream_chunk_offset', 'stream_chunk_data'])
GetRS485Configuration = namedtuple('RS485Configuration', ['baudrate', 'parity', 'stopbits', 'wordlength', 'duplex'])
GetModbusConfiguration = namedtuple('ModbusConfiguration', ['slave_address', 'master_request_timeout'])
GetBufferConfig = namedtuple('BufferConfig', ['send_buffer_size', 'receive_buffer_size'])
GetBufferStatus = namedtuple('BufferStatus', ['send_buffer_used', 'receive_buffer_used'])
GetErrorCount = namedtuple('ErrorCount', ['overrun_error_count', 'parity_error_count'])
GetModbusCommonErrorCount = namedtuple('ModbusCommonErrorCount', ['timeout_error_count', 'checksum_error_count', 'frame_too_big_error_count', 'illegal_function_error_count', 'illegal_data_address_error_count', 'illegal_data_value_error_count', 'slave_device_failure_error_count'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletRS485(Device):
    """
    Communicates with RS485 devices with full- or half-duplex
    """

    DEVICE_IDENTIFIER = 277
    DEVICE_DISPLAY_NAME = 'RS485 Bricklet'

    CALLBACK_READ_LOW_LEVEL = 41
    CALLBACK_ERROR_COUNT = 42
    CALLBACK_MODBUS_SLAVE_READ_COILS_REQUEST = 43
    CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE_LOW_LEVEL = 44
    CALLBACK_MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST = 45
    CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE_LOW_LEVEL = 46
    CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST = 47
    CALLBACK_MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE = 48
    CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST = 49
    CALLBACK_MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE = 50
    CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST_LOW_LEVEL = 51
    CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE = 52
    CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST_LOW_LEVEL = 53
    CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE = 54
    CALLBACK_MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST = 55
    CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE_LOW_LEVEL = 56
    CALLBACK_MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST = 57
    CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE_LOW_LEVEL = 58

    CALLBACK_READ = -41
    CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE = -44
    CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE = -46
    CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST = -51
    CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST = -53
    CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE = -56
    CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE = -58

    FUNCTION_WRITE_LOW_LEVEL = 1
    FUNCTION_READ_LOW_LEVEL = 2
    FUNCTION_ENABLE_READ_CALLBACK = 3
    FUNCTION_DISABLE_READ_CALLBACK = 4
    FUNCTION_IS_READ_CALLBACK_ENABLED = 5
    FUNCTION_SET_RS485_CONFIGURATION = 6
    FUNCTION_GET_RS485_CONFIGURATION = 7
    FUNCTION_SET_MODBUS_CONFIGURATION = 8
    FUNCTION_GET_MODBUS_CONFIGURATION = 9
    FUNCTION_SET_MODE = 10
    FUNCTION_GET_MODE = 11
    FUNCTION_SET_COMMUNICATION_LED_CONFIG = 12
    FUNCTION_GET_COMMUNICATION_LED_CONFIG = 13
    FUNCTION_SET_ERROR_LED_CONFIG = 14
    FUNCTION_GET_ERROR_LED_CONFIG = 15
    FUNCTION_SET_BUFFER_CONFIG = 16
    FUNCTION_GET_BUFFER_CONFIG = 17
    FUNCTION_GET_BUFFER_STATUS = 18
    FUNCTION_ENABLE_ERROR_COUNT_CALLBACK = 19
    FUNCTION_DISABLE_ERROR_COUNT_CALLBACK = 20
    FUNCTION_IS_ERROR_COUNT_CALLBACK_ENABLED = 21
    FUNCTION_GET_ERROR_COUNT = 22
    FUNCTION_GET_MODBUS_COMMON_ERROR_COUNT = 23
    FUNCTION_MODBUS_SLAVE_REPORT_EXCEPTION = 24
    FUNCTION_MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL = 25
    FUNCTION_MODBUS_MASTER_READ_COILS = 26
    FUNCTION_MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL = 27
    FUNCTION_MODBUS_MASTER_READ_HOLDING_REGISTERS = 28
    FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST = 29
    FUNCTION_MODBUS_MASTER_WRITE_SINGLE_COIL = 30
    FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST = 31
    FUNCTION_MODBUS_MASTER_WRITE_SINGLE_REGISTER = 32
    FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST = 33
    FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL = 34
    FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST = 35
    FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL = 36
    FUNCTION_MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL = 37
    FUNCTION_MODBUS_MASTER_READ_DISCRETE_INPUTS = 38
    FUNCTION_MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL = 39
    FUNCTION_MODBUS_MASTER_READ_INPUT_REGISTERS = 40
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

    PARITY_NONE = 0
    PARITY_ODD = 1
    PARITY_EVEN = 2
    STOPBITS_1 = 1
    STOPBITS_2 = 2
    WORDLENGTH_5 = 5
    WORDLENGTH_6 = 6
    WORDLENGTH_7 = 7
    WORDLENGTH_8 = 8
    DUPLEX_HALF = 0
    DUPLEX_FULL = 1
    MODE_RS485 = 0
    MODE_MODBUS_SLAVE_RTU = 1
    MODE_MODBUS_MASTER_RTU = 2
    COMMUNICATION_LED_CONFIG_OFF = 0
    COMMUNICATION_LED_CONFIG_ON = 1
    COMMUNICATION_LED_CONFIG_SHOW_HEARTBEAT = 2
    COMMUNICATION_LED_CONFIG_SHOW_COMMUNICATION = 3
    ERROR_LED_CONFIG_OFF = 0
    ERROR_LED_CONFIG_ON = 1
    ERROR_LED_CONFIG_SHOW_HEARTBEAT = 2
    ERROR_LED_CONFIG_SHOW_ERROR = 3
    EXCEPTION_CODE_TIMEOUT = -1
    EXCEPTION_CODE_SUCCESS = 0
    EXCEPTION_CODE_ILLEGAL_FUNCTION = 1
    EXCEPTION_CODE_ILLEGAL_DATA_ADDRESS = 2
    EXCEPTION_CODE_ILLEGAL_DATA_VALUE = 3
    EXCEPTION_CODE_SLAVE_DEVICE_FAILURE = 4
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

        self.response_expected[BrickletRS485.FUNCTION_WRITE_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_READ_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_ENABLE_READ_CALLBACK] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_DISABLE_READ_CALLBACK] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_IS_READ_CALLBACK_ENABLED] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_RS485_CONFIGURATION] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_RS485_CONFIGURATION] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_MODBUS_CONFIGURATION] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_MODBUS_CONFIGURATION] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_MODE] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_MODE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_COMMUNICATION_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_COMMUNICATION_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_ERROR_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_ERROR_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_BUFFER_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_BUFFER_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_BUFFER_STATUS] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_ENABLE_ERROR_COUNT_CALLBACK] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_DISABLE_ERROR_COUNT_CALLBACK] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_IS_ERROR_COUNT_CALLBACK_ENABLED] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_ERROR_COUNT] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_MODBUS_COMMON_ERROR_COUNT] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_REPORT_EXCEPTION] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_READ_COILS] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_READ_HOLDING_REGISTERS] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_SINGLE_COIL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_SINGLE_REGISTER] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_READ_DISCRETE_INPUTS] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRS485.FUNCTION_MODBUS_MASTER_READ_INPUT_REGISTERS] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.CALLBACK_READ_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_ERROR_COUNT] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_COILS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE_LOW_LEVEL] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_BOOTLOADER_MODE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_BOOTLOADER_MODE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_WRITE_FIRMWARE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_RESET] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_WRITE_UID] = BrickletRS485.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRS485.FUNCTION_READ_UID] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRS485.FUNCTION_GET_IDENTITY] = BrickletRS485.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletRS485.CALLBACK_READ_LOW_LEVEL] = 'H H 60c'
        self.callback_formats[BrickletRS485.CALLBACK_ERROR_COUNT] = 'I I'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_COILS_REQUEST] = 'B H H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE_LOW_LEVEL] = 'B b H H 464!'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST] = 'B H H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE_LOW_LEVEL] = 'B b H H 29H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST] = 'B H !'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE] = 'B b'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST] = 'B H H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE] = 'B b'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST_LOW_LEVEL] = 'B H H H H 440!'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE] = 'B b'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST_LOW_LEVEL] = 'B H H H H 27H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE] = 'B b'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST] = 'B H H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE_LOW_LEVEL] = 'B b H H 464!'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST] = 'B H H'
        self.callback_formats[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE_LOW_LEVEL] = 'B b H H 29H'

        self.low_level_callbacks[BrickletRS485.CALLBACK_READ_LOW_LEVEL] = [BrickletRS485.CALLBACK_READ, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_MASTER_READ_COILS_RESPONSE, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE, {'stream': {'fixed_total_length': None}}, None]
        self.low_level_callbacks[BrickletRS485.CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE_LOW_LEVEL] = [BrickletRS485.CALLBACK_MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE, {'stream': {'fixed_total_length': None}}, None]

    def write_low_level(self, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        Writes characters to the RS485 interface. The characters can be binary data,
        ASCII or similar is not necessary.

        The return value is the number of characters that were written.

        See :func:`Set RS485 Configuration` for configuration possibilities
        regarding baudrate, parity and so on.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_WRITE_LOW_LEVEL, (stream_total_length, stream_chunk_offset, stream_chunk_data), 'H H 59c', 'B')

    def read_low_level(self, length):
        """
        Returns up to *length* characters from receive buffer.

        Instead of polling with this function, you can also use
        callbacks. See :func:`Enable Read Callback` and :cb:`Read` callback.
        """
        return ReadLowLevel(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_READ_LOW_LEVEL, (length,), 'H', 'H H 60c'))

    def enable_read_callback(self):
        """
        Enables the :cb:`Read` callback.

        By default the callback is disabled.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_ENABLE_READ_CALLBACK, (), '', '')

    def disable_read_callback(self):
        """
        Disables the :cb:`Read` callback.

        By default the callback is disabled.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_DISABLE_READ_CALLBACK, (), '', '')

    def is_read_callback_enabled(self):
        """
        Returns *true* if the :cb:`Read` callback is enabled,
        *false* otherwise.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_IS_READ_CALLBACK_ENABLED, (), '', '!')

    def set_rs485_configuration(self, baudrate, parity, stopbits, wordlength, duplex):
        """
        Sets the configuration for the RS485 communication. Available options:

        * Baudrate between 100 and 2000000 baud.
        * Parity of none, odd or even.
        * Stopbits can be 1 or 2.
        * Word length of 5 to 8.
        * Half- or Full-Duplex.

        The default is: 115200 baud, parity none, 1 stop bit, word length 8, half duplex.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_RS485_CONFIGURATION, (baudrate, parity, stopbits, wordlength, duplex), 'I B B B B', '')

    def get_rs485_configuration(self):
        """
        Returns the configuration as set by :func:`Set RS485 Configuration`.
        """
        return GetRS485Configuration(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_RS485_CONFIGURATION, (), '', 'I B B B B'))

    def set_modbus_configuration(self, slave_address, master_request_timeout):
        """
        Sets the configuration for the RS485 Modbus communication. Available options:

        * Slave Address: Address to be used as the Modbus slave address in Modbus slave mode. Valid Modbus slave address range is 0 to 247.
        * Master Request Timeout: Specifies how long the master should wait for a response from a slave in milliseconds when in Modbus master mode.

        The default is: Slave Address = 1 and Master Request Timeout = 1000 milliseconds (1 second).
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_MODBUS_CONFIGURATION, (slave_address, master_request_timeout), 'B I', '')

    def get_modbus_configuration(self):
        """
        Returns the configuration as set by :func:`Set Modbus Configuration`.
        """
        return GetModbusConfiguration(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_MODBUS_CONFIGURATION, (), '', 'B I'))

    def set_mode(self, mode):
        """
        Sets the mode of the Bricklet in which it operates. Available options are

        * RS485,
        * Modbus Slave RTU and
        * Modbus Master RTU.

        The default is: RS485 mode.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_MODE, (mode,), 'B', '')

    def get_mode(self):
        """
        Returns the configuration as set by :func:`Set Mode`.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_MODE, (), '', 'B')

    def set_communication_led_config(self, config):
        """
        Sets the communication LED configuration. By default the LED shows
        communication traffic, it flickers once for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_COMMUNICATION_LED_CONFIG, (config,), 'B', '')

    def get_communication_led_config(self):
        """
        Returns the configuration as set by :func:`Set Communication LED Config`
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_COMMUNICATION_LED_CONFIG, (), '', 'B')

    def set_error_led_config(self, config):
        """
        Sets the error LED configuration.

        By default the error LED turns on if there is any error (see :cb:`Error Count`
        callback). If you call this function with the SHOW ERROR option again, the LED
        will turn off until the next error occurs.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_ERROR_LED_CONFIG, (config,), 'B', '')

    def get_error_led_config(self):
        """
        Returns the configuration as set by :func:`Set Error LED Config`.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_ERROR_LED_CONFIG, (), '', 'B')

    def set_buffer_config(self, send_buffer_size, receive_buffer_size):
        """
        Sets the send and receive buffer size in byte. In sum there is
        10240 byte (10kb) buffer available and the minimum buffer size
        is 1024 byte (1kb) for both.

        The current buffer content is lost if this function is called.

        The send buffer holds data that is given by :func:`Write` and
        can not be written yet. The receive buffer holds data that is
        received through RS485 but could not yet be send to the
        user, either by :func:`Read` or through :cb:`Read` callback.

        The default configuration is 5120 byte (5kb) per buffer.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_BUFFER_CONFIG, (send_buffer_size, receive_buffer_size), 'H H', '')

    def get_buffer_config(self):
        """
        Returns the buffer configuration as set by :func:`Set Buffer Config`.
        """
        return GetBufferConfig(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_BUFFER_CONFIG, (), '', 'H H'))

    def get_buffer_status(self):
        """
        Returns the currently used bytes for the send and received buffer.

        See :func:`Set Buffer Config` for buffer size configuration.
        """
        return GetBufferStatus(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_BUFFER_STATUS, (), '', 'H H'))

    def enable_error_count_callback(self):
        """
        Enables the :cb:`Error Count` callback.

        By default the callback is disabled.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_ENABLE_ERROR_COUNT_CALLBACK, (), '', '')

    def disable_error_count_callback(self):
        """
        Disables the :cb:`Error Count` callback.

        By default the callback is disabled.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_DISABLE_ERROR_COUNT_CALLBACK, (), '', '')

    def is_error_count_callback_enabled(self):
        """
        Returns *true* if the :cb:`Error Count` callback is enabled,
        *false* otherwise.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_IS_ERROR_COUNT_CALLBACK_ENABLED, (), '', '!')

    def get_error_count(self):
        """
        Returns the current number of overrun and parity errors.
        """
        return GetErrorCount(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_ERROR_COUNT, (), '', 'I I'))

    def get_modbus_common_error_count(self):
        """
        Returns the current number of errors occurred in Modbus mode.

        * Timeout Error Count: Number of timeouts occurred.
        * Checksum Error Count: Number of failures due to Modbus frame CRC16 checksum mismatch.
        * Frame Too Big Error Count: Number of times frames were rejected because they exceeded maximum Modbus frame size which is 256 bytes.
        * Illegal Function Error Count: Number of errors when an unimplemented or illegal function is requested. This corresponds to Modbus exception code 1.
        * Illegal Data Address Error Count: Number of errors due to invalid data address. This corresponds to Modbus exception code 2.
        * Illegal Data Value Error Count: Number of errors due to invalid data value. This corresponds to Modbus exception code 3.
        * Slave Device Failure Error Count: Number of errors occurred on the slave device which were unrecoverable. This corresponds to Modbus exception code 4.
        """
        return GetModbusCommonErrorCount(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_MODBUS_COMMON_ERROR_COUNT, (), '', 'I I I I I I I'))

    def modbus_slave_report_exception(self, request_id, exception_code):
        """
        In Modbus slave mode this function can be used to report a Modbus exception for
        a Modbus master request.

        * Request ID: Request ID of the request received by the slave.
        * Exception Code: Modbus exception code to report to the Modbus master.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_REPORT_EXCEPTION, (request_id, exception_code), 'B b', '')

    def modbus_slave_answer_read_coils_request_low_level(self, request_id, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus slave mode this function can be used to answer a master request to
        read coils.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Data: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :cb:`Modbus Slave Read Coils Request` callback
        with the Request ID as provided by the argument of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL, (request_id, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H 472!', '')

    def modbus_master_read_coils(self, slave_address, starting_address, count):
        """
        In Modbus master mode this function can be used to read coils from a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting address of the read.
        * Count: Number of coils to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Read Coils Response`
        callback. In this callback the Request ID provided by the callback argument must be
        matched with the Request ID returned from this function to verify that the callback
        is indeed for a particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_READ_COILS, (slave_address, starting_address, count), 'B H H', 'B')

    def modbus_slave_answer_read_holding_registers_request_low_level(self, request_id, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus slave mode this function can be used to answer a master request to
        read holding registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Data: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :cb:`Modbus Slave Read Holding Registers Request`
        callback with the Request ID as provided by the argument of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL, (request_id, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H 29H', '')

    def modbus_master_read_holding_registers(self, slave_address, starting_address, count):
        """
        In Modbus master mode this function can be used to read holding registers from a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting address of the read.
        * Count: Number of holding registers to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Read Holding Registers Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_READ_HOLDING_REGISTERS, (slave_address, starting_address, count), 'B H H', 'B')

    def modbus_slave_answer_write_single_coil_request(self, request_id):
        """
        In Modbus slave mode this function can be used to answer a master request to
        write a single coil.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :cb:`Modbus Slave Write Single Coil Request`
        callback with the Request ID, Coil Address and Coil Value as provided by the
        arguments of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST, (request_id,), 'B', '')

    def modbus_master_write_single_coil(self, slave_address, coil_address, coil_value):
        """
        In Modbus master mode this function can be used to write a single coil of a slave.

        * Slave Address: Address of the target Modbus slave.
        * Coil Address: Address of the coil.
        * Coil Value: Value to be written.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Write Single Coil Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_SINGLE_COIL, (slave_address, coil_address, coil_value), 'B H !', 'B')

    def modbus_slave_answer_write_single_register_request(self, request_id):
        """
        In Modbus slave mode this function can be used to answer a master request to
        write a single register.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :cb:`Modbus Slave Write Single Register Request`
        callback with the Request ID, Register Address and Register Value as provided by
        the arguments of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST, (request_id,), 'B', '')

    def modbus_master_write_single_register(self, slave_address, register_address, register_value):
        """
        In Modbus master mode this function can be used to write a single register of a
        slave.

        * Slave Address: Address of the target Modbus slave.
        * Register Address: Address of the register.
        * Register Value: Value to be written.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Write Single Register Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_SINGLE_REGISTER, (slave_address, register_address, register_value), 'B H H', 'B')

    def modbus_slave_answer_write_multiple_coils_request(self, request_id):
        """
        In Modbus slave mode this function can be used to answer a master request to
        write multiple coils.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :cb:`Modbus Slave Write Multiple Coils Request`
        callback with the Request ID, Starting Address and Count as provided by the
        arguments of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST, (request_id,), 'B', '')

    def modbus_master_write_multiple_coils_low_level(self, slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus master mode this function can be used to write multiple coils of a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting address of the write.
        * Count: Number of coils to write.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Write Multiple Coils Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL, (slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H H H 432!', 'B')

    def modbus_slave_answer_write_multiple_registers_request(self, request_id):
        """
        In Modbus slave mode this function can be used to answer a master request to
        write multiple registers.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :cb:`Modbus Slave Write Multiple Registers Request`
        callback with the Request ID, Starting Address and Count as provided by the
        arguments of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST, (request_id,), 'B', '')

    def modbus_master_write_multiple_registers_low_level(self, slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus master mode this function can be used to write multiple registers of a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting Address of the write.
        * Count: Number of registers to write.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Write Multiple Registers Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL, (slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H H H 27H', 'B')

    def modbus_slave_answer_read_discrete_inputs_request_low_level(self, request_id, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus slave mode this function can be used to answer a master request to
        read discrete inputs.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Data: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :cb:`Modbus Slave Read Discrete Inputs Request`
        callback with the Request ID as provided by the argument of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL, (request_id, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H 472!', '')

    def modbus_master_read_discrete_inputs(self, slave_address, starting_address, count):
        """
        In Modbus master mode this function can be used to read discrete inputs from a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting address of the read.
        * Count: Number of discrete inputs to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Read Discrete Inputs Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_READ_DISCRETE_INPUTS, (slave_address, starting_address, count), 'B H H', 'B')

    def modbus_slave_answer_read_input_registers_request_low_level(self, request_id, stream_total_length, stream_chunk_offset, stream_chunk_data):
        """
        In Modbus slave mode this function can be used to answer a master request to
        read input registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Data: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :cb:`Modbus Slave Read Input Registers Request` callback
        with the Request ID as provided by the argument of the callback.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL, (request_id, stream_total_length, stream_chunk_offset, stream_chunk_data), 'B H H 29H', '')

    def modbus_master_read_input_registers(self, slave_address, starting_address, count):
        """
        In Modbus master mode this function can be used to read input registers from a slave.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Starting address of the read.
        * Count: Number of input registers to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :cb:`Modbus Master Read Input Registers Response`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_MODBUS_MASTER_READ_INPUT_REGISTERS, (slave_address, starting_address, count), 'B H H', 'B')

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ack checksum errors,
        * message checksum errors,
        * frameing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier und crc are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for func:`WriteFirmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        self.ipcon.send_request(self, BrickletRS485.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletRS485.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletRS485.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def write(self, data):
        stream_extra = ()
        stream_total_written = 0
        stream_total_length = len(data)
        stream_chunk_offset = 0

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 59]

                if len(stream_chunk_data) < 59:
                    stream_chunk_data.extend(['\x00']*(59 - len(stream_chunk_data)))

                stream_result = self.write_low_level(stream_total_length, stream_chunk_offset, stream_chunk_data)
                stream_extra = stream_result[:-1] # FIXME: validate that the extra of all the low-level calls is identical
                stream_chunk_written = stream_result[-1]
                stream_total_written += stream_chunk_written

                # either last chunk or short write
                if stream_chunk_written < 59:
                    break

                stream_chunk_offset += 59

        if len(stream_extra) > 0:
            return stream_extra + (stream_total_written,) # FIXME: need to return this as a namedtuple
        else:
            return stream_total_written

    def read(self, length):
        stream_extra = ()
        stream_total_length = None
        stream_chunk_offset = 0
        stream_result = None
        stream_data = ()
        stream_out_of_sync = False

        STREAM_CHUNK_OFFSET_NO_DATA = (1 << 16) - 1 # FIXME: make this depend on the stream_chunk_offset type

        with self.stream_lock:
            if stream_total_length == None: # no fixed-stream-length
                stream_result = self.read_low_level(length)
                stream_extra = stream_result[:-3] # FIXME: validate that extra parameters are identical for all low-level getters of a stream
                stream_total_length = stream_result.stream_total_length
                stream_chunk_offset = stream_result.stream_chunk_offset
                stream_data = stream_result.stream_chunk_data

            if stream_chunk_offset == STREAM_CHUNK_OFFSET_NO_DATA:
                raise Error(Error.STREAM_NO_DATA, 'Stream has no data')
            elif stream_chunk_offset != 0: # stream out-of-sync
                # discard remaining stream to bring it back in-sync
                while stream_chunk_offset + 60 < stream_total_length:
                    # FIXME: validate that total length is identical for all low-level getters of a stream
                    stream_chunk_offset = self.read_low_level(length).stream_chunk_offset

                raise Error(Error.STREAM_OUT_OF_SYNC, 'Stream is out-of-sync')

            # FIXME: validate chunk offset < total length

            while len(stream_data) < stream_total_length:
                stream_result = self.read_low_level(length)
                stream_extra = stream_result[:-3] # FIXME: validate that extra parameters are identical for all low-level getters of a stream
                stream_chunk_offset = stream_result.stream_chunk_offset

                # FIXME: validate that total length is identical for all low-level getters of a stream

                if stream_chunk_offset != len(stream_data): # stream out-of-sync
                    # discard remaining stream to bring it back in-sync
                    while stream_chunk_offset + 60 < stream_total_length:
                        # FIXME: validate that total length is identical for all low-level getters of a stream
                        stream_chunk_offset = self.read_low_level(length).stream_chunk_offset

                    raise Error(Error.STREAM_OUT_OF_SYNC, 'Stream is out-of-sync')

                stream_data += stream_result.stream_chunk_data

        if len(stream_extra) > 0:
            return stream_extra + (stream_data[:stream_total_length],) # FIXME: need to return this as a namedtuple
        else:
            return stream_data[:stream_total_length]

    def modbus_slave_answer_read_coils_request(self, request_id, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 472]

                if len(stream_chunk_data) < 472:
                    stream_chunk_data.extend([False]*(472 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_slave_answer_read_coils_request_low_level(request_id, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 472

        return stream_result

    def modbus_slave_answer_read_holding_registers_request(self, request_id, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 29]

                if len(stream_chunk_data) < 29:
                    stream_chunk_data.extend([0]*(29 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_slave_answer_read_holding_registers_request_low_level(request_id, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 29

        return stream_result

    def modbus_master_write_multiple_coils(self, slave_address, starting_address, count, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 432]

                if len(stream_chunk_data) < 432:
                    stream_chunk_data.extend([False]*(432 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_master_write_multiple_coils_low_level(slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 432

        return stream_result

    def modbus_master_write_multiple_registers(self, slave_address, starting_address, count, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 27]

                if len(stream_chunk_data) < 27:
                    stream_chunk_data.extend([0]*(27 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_master_write_multiple_registers_low_level(slave_address, starting_address, count, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 27

        return stream_result

    def modbus_slave_answer_read_discrete_inputs_request(self, request_id, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 472]

                if len(stream_chunk_data) < 472:
                    stream_chunk_data.extend([False]*(472 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_slave_answer_read_discrete_inputs_request_low_level(request_id, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 472

        return stream_result

    def modbus_slave_answer_read_input_registers_request(self, request_id, data):
        stream_total_length = len(data)
        stream_chunk_offset = 0
        stream_result = None

        with self.stream_lock:
            while stream_chunk_offset < stream_total_length:
                stream_chunk_data = data[stream_chunk_offset:stream_chunk_offset + 29]

                if len(stream_chunk_data) < 29:
                    stream_chunk_data.extend([0]*(29 - len(stream_chunk_data)))

                # FIXME: validate that the result of all the low-level calls is identical
                stream_result = self.modbus_slave_answer_read_input_registers_request_low_level(request_id, stream_total_length, stream_chunk_offset, stream_chunk_data)

                stream_chunk_offset += 29

        return stream_result

    def register_callback(self, id_, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        if callback is None:
            self.registered_callbacks.pop(id_, None)
        else:
            self.registered_callbacks[id_] = callback

RS485 = BrickletRS485 # for backward compatibility
