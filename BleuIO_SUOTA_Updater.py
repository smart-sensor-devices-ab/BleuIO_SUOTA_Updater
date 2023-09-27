# Copyright 2023 Smart Sensor Devices in Sweden AB
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import queue
import time
import ctypes
import sys
import json
import argparse
from bleuio_lib.bleuio_funcs import BleuIO
import binascii
import os

# Check if on Windows
if os.name == "nt":
    # Used to allow coloured text (ANSI escape sequences) in Windows Terminal
    kernel32 = ctypes.WinDLL("kernel32")
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)

# Firmware verison:
fw_version = "1.0.0"
# Last modified date:
last_modified = "2023-09-27"
# Created date:
created = "2023-09-26"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


MAX_IMAGE_SIZE = 0x4B000  # 300Kb
CHECKSUM_SIZE = 1  # in bytes
DEFAULT_DATA_CHUNK_SIZE = 20
ATT_HEADER_SIZE = 3


# SUOTA_SERV_STATUS values
SUOTA_STATUS_SRV_STARTED = 0x01
SUOTA_STATUS_CMP_OK = 0x02
SUOTA_STATUS_SRV_EXIT = 0x03
SUOTA_STATUS_CRC_ERR = 0x04
SUOTA_STATUS_PATCH_LEN_ERR = 0x05
SUOTA_STATUS_EXT_MEM_ERR = 0x06
SUOTA_STATUS_INT_MEM_ERR = 0x07
SUOTA_STATUS_INVAL_MEM_TYPE = 0x08
SUOTA_STATUS_APP_ERROR = 0x09
SUOTA_STATUS_IMG_STARTED = 0x10
SUOTA_STATUS_INVALID_IMAGE_BANK = 0x11
SUOTA_STATUS_INVALID_IMAGE_HEADER = 0x12
SUOTA_STATUS_INVALID_IMAGE_SIZE = 0x13
SUOTA_STATUS_INVALID_PRODUCT_HEADER = 0x14
SUOTA_STATUS_SAME_IMAGE_ERROR = 0x15
SUOTA_STATUS_EXTERNAL_MEMORY_READ_ERROR = 0x16
# SUOTA started for downloading image (SUOTA application)

error_list = [
    "UNKNOWN_ERROR",
    "SUOTA_STATUS_SRV_STARTED",
    "SUOTA_STATUS_CMP_OK",
    "SUOTA_STATUS_SRV_EXIT",
    "SUOTA_STATUS_CRC_ERR",
    "SUOTA_STATUS_PATCH_LEN_ERR",
    "SUOTA_STATUS_EXT_MEM_ERR",
    "SUOTA_STATUS_INT_MEM_ERR",
    "SUOTA_STATUS_INVAL_MEM_TYPE",
    "SUOTA_STATUS_APP_ERROR",
    "UNKNOWN_ERROR",
    "UNKNOWN_ERROR",
    "UNKNOWN_ERROR",
    "UNKNOWN_ERROR",
    "UNKNOWN_ERROR",
    "UNKNOWN_ERROR",
    "SUOTA_STATUS_IMG_STARTED",
    "SUOTA_STATUS_INVALID_IMAGE_BANK",
    "SUOTA_STATUS_INVALID_IMAGE_HEADER",
    "SUOTA_STATUS_INVALID_IMAGE_SIZE",
    "SUOTA_STATUS_INVALID_PRODUCT_HEADER",
    "SUOTA_STATUS_SAME_IMAGE_ERROR",
    "SUOTA_STATUS_EXTERNAL_MEMORY_READ_ERROR",
]

# SUOTA service characteristic UUIDs
SUOTA_MEM_DEV_UUID = "8082caa8-41a6-4021-91c6-56f9b954cc34"
SUOTA_GPIO_MAP_UUID = "724249f0-5ec3-4b5f-8804-42345af08651"
SUOTA_MEM_INFO_UUID = "6c53db25-47a1-45fe-a022-7c92fb334fd4"
SUOTA_PATCH_LEN_UUID = "9d84b9a3-000c-49d8-9183-855b673fda31"
SUOTA_PATCH_DATA_UUID = "457871e8-d516-4ca1-9116-57d0b17b9cb2"
SUOTA_SERV_STATUS_UUID = "5f78df94-798c-46f5-990a-b3eb6a065c88"
SUOTA_VERSION_UUID = "64b4e8b5-0de5-401b-a21d-acc8db3b913a"
SUOTA_PD_CHAR_SIZE_UUID = "42c3dfdd-77be-4d9c-8454-8f875267fb3b"
SUOTA_MTU_UUID = "b7de1eea-823d-43bb-a3af-c4903dfce23c"

# Global
RETRIES_NUMBER = 3
DEFAULT_TIMEOUT = 30
BLEUIO_SUOTA_ADV_DATA = "02010603FF5B070302F5FE"
debug_msg = False
browse_complete = False
main_running = True
bleuio_found = False
indi_resp_byte_list = []
noti_resp_byte_list = []
notifications_q = queue.Queue()
indication_q = queue.Queue()
gattc_read_q = queue.Queue()
gattc_write_rsp_q = queue.Queue()
dis_fw_ver_handle = ""
suota_mem_dev_handle = ""
suota_gpio_map_handle = ""
suota_mem_info_handle = ""
suota_patch_len_handle = ""
suota_patch_data_handle = ""
suota_serv_status_handle = ""
suota_version_handle = ""
suota_pd_char_size_handle = ""
suota_mtu_handle = ""

global suota_block_size
global patch_length
global patch_data_len
global patch_data
global current_block_length
global suota_chunk_size
global block_offset
global block_length
global patch_chunck_offset
global patch_chunck_length

suota_block_size = 0
patch_length = 0  # counts bytes - must be a multiple of 4
patch_data_len = MAX_IMAGE_SIZE + CHECKSUM_SIZE
patch_data = []
current_block_length = 0
suota_chunk_size = DEFAULT_DATA_CHUNK_SIZE
block_offset = 0
block_length = 0
patch_chunck_offset = 0
patch_chunck_length = 0


def print_dbg_msg(string):
    """Print to screen if -dbg is used to run the script."""
    if debug_msg:
        print(string)


def hex_to_little_endian(hex_string):
    little_endian_hex = bytearray.fromhex(hex_string)[::-1]
    little_endian_hex = str(binascii.hexlify(little_endian_hex))
    little_endian_hex = little_endian_hex[2:]
    little_endian_hex = little_endian_hex.replace("'", "")
    little_endian_hex = little_endian_hex.upper()

    return little_endian_hex


def my_scan_callback(scan_input):
    global bleuio_found
    global mac_addr
    global suota_avalible
    print_dbg_msg("\n\nscan_evt: " + str(scan_input))
    if not bleuio_found:
        if '{"SF"' in str(scan_input) and '"data":' in str(scan_input):
            try:
                print_dbg_msg(scan_input[0])
                scan_result = json.loads(scan_input[0])
                print_dbg_msg("json loads ok")
                length = len(scan_result["data"])
                mac = scan_result["addr"]
                print_dbg_msg("length ok: " + str(length))
                bleuio_found = True
                mac_addr = mac
            except Exception as e:
                print(str(e))


def my_evt_callback(evt_input):
    global browse_complete
    global suota_avalible
    global bootloader_open
    global indi_resp_byte_list
    global noti_resp_byte_list
    global dis_fw_ver_handle
    global suota_mem_dev_handle
    global suota_gpio_map_handle
    global suota_mem_info_handle
    global suota_patch_len_handle
    global suota_patch_data_handle
    global suota_serv_status_handle
    global suota_version_handle
    global suota_pd_char_size_handle
    global suota_mtu_handle

    print_dbg_msg("\n\nevt: " + str(evt_input))
    if '"action":"connected"' in str(evt_input):
        my_dongle.status.isConnected = True
    if '"action":"disconnected"' in str(evt_input):
        print("Disconnected from BleuIO Dongle.")
        my_dongle.status.isConnected = False
        browse_complete = False
    if '"action":"browse completed"' in str(evt_input):
        browse_complete = True
    if '"serv","uuid":"0xfef5"' in str(evt_input):
        suota_avalible = True
    if ('"uuid":"' + SUOTA_MEM_DEV_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_mem_dev_char = json.loads(evt_input[0])
            suota_mem_dev_handle = suota_mem_dev_char["evt"]["handle"]
            suota_mem_dev_handle = str(suota_mem_dev_handle).upper()
        except Exception as e:
            print(str(e))
        suota_avalible = True
    if ('"uuid":"' + SUOTA_GPIO_MAP_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_gpio_map_char = json.loads(evt_input[0])
            suota_gpio_map_handle = suota_gpio_map_char["evt"]["handle"]
            suota_gpio_map_handle = str(suota_gpio_map_handle).upper()
            print_dbg_msg("SUOTA_GPIO_MAP_UUID Handle: " + suota_gpio_map_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_MEM_INFO_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_mem_info_char = json.loads(evt_input[0])
            suota_mem_info_handle = suota_mem_info_char["evt"]["handle"]
            suota_mem_info_handle = str(suota_mem_info_handle).upper()
            print_dbg_msg("SUOTA_MEM_INFO_UUID Handle: " + suota_mem_info_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_PATCH_LEN_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_patch_len_char = json.loads(evt_input[0])
            suota_patch_len_handle = suota_patch_len_char["evt"]["handle"]
            suota_patch_len_handle = str(suota_patch_len_handle).upper()
            print_dbg_msg("SUOTA_PATCH_LEN_UUID Handle: " + suota_patch_len_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_PATCH_DATA_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_patch_data_char = json.loads(evt_input[0])
            suota_patch_data_handle = suota_patch_data_char["evt"]["handle"]
            suota_patch_data_handle = str(suota_patch_data_handle).upper()
            print_dbg_msg("SUOTA_PATCH_DATA_UUID Handle: " + suota_patch_data_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_SERV_STATUS_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_serv_status_char = json.loads(evt_input[0])
            suota_serv_status_handle = suota_serv_status_char["evt"]["handle"]
            suota_serv_status_handle = str(suota_serv_status_handle).upper()
            print_dbg_msg("SUOTA_SERV_STATUS_UUID Handle: " + suota_serv_status_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_VERSION_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_version_char = json.loads(evt_input[0])
            suota_version_handle = suota_version_char["evt"]["handle"]
            suota_version_handle = str(suota_version_handle).upper()
            print_dbg_msg("SUOTA_VERSION_UUID Handle: " + suota_version_handle)
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_PD_CHAR_SIZE_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_pd_char_size_char = json.loads(evt_input[0])
            suota_pd_char_size_handle = suota_pd_char_size_char["evt"]["handle"]
            suota_pd_char_size_handle = str(suota_pd_char_size_handle).upper()
            print_dbg_msg(
                "SUOTA_PD_CHAR_SIZE_UUID Handle: " + suota_pd_char_size_handle
            )
        except Exception as e:
            print(str(e))
    if ('"uuid":"' + SUOTA_MTU_UUID) in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            suota_mtu_char = json.loads(evt_input[0])
            suota_mtu_handle = suota_mtu_char["evt"]["handle"]
            suota_mtu_handle = str(suota_mtu_handle).upper()
            print_dbg_msg("SUOTA_MTU_UUID Handle: " + suota_mtu_handle)
        except Exception as e:
            print(str(e))

    # Get DIS FW Handle
    if '"uuid":"0x2a26"' in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{768", '{"768"')
            dis_fw_ver_char = json.loads(evt_input[0])
            dis_fw_ver_handle = dis_fw_ver_char["evt"]["handle"]
            dis_fw_ver_handle = str(dis_fw_ver_handle).upper()
            print_dbg_msg("DIS FW Ver Handle: " + dis_fw_ver_handle)
        except Exception as e:
            print(str(e))
    # Get FW version
    if '{775:"0000","evt":{"handle":"' in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{775", '{"775"')
            read_obj = json.loads(evt_input[0])
            print_dbg_msg(evt_input[0])
            if read_obj["evt"]["len"] == 0:
                data = "00"
            else:
                data = read_obj["evt"]["hex"]
                data = data.replace("0x", "")
            if dis_fw_ver_handle.lower() in str(evt_input):
                byte_string = bytes.fromhex(data)
                read_data = byte_string.decode("ASCII")
            elif suota_version_handle in str(evt_input):
                read_data = str(int(data, 16) / 10)
            else:
                print_dbg_msg("read: " + data)
                data = hex_to_little_endian(data)
                print_dbg_msg("read to little endian: " + data)
                read_data = str(int(data, 16))
            gattc_read_q.put(read_data)
        except Exception as e:
            print(str(e))
    if '","writeStatus":' in str(evt_input):
        if (
            not '"handle":"0024"' in str(evt_input)
            and not '"handle":"0000"' in str(evt_input)
            and not '"handle":"0021"' in str(evt_input)
        ):
            success = 1
            if '"writeStatus":0' in str(evt_input):
                success = 0
            else:
                success = 1
            gattc_write_rsp_q.put(success)
            print_dbg_msg("Put '" + str(success) + "' in gattc_write_rsp_q")
    # Notifications
    if '777:"0000"' in str(evt_input) and '"hex":' in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{777", '{"777"')
            suota_noti = json.loads(evt_input[0])
            length = suota_noti["evt"]["len"]
            data = suota_noti["evt"]["hex"]
            data = data.replace("0x", "")
            suota_code = int(data, 16)
            notifications_q.put(suota_code)
        except Exception as e:
            print(str(e))
    # Indications
    if '778:"0000"' in str(evt_input) and '"hex":' in str(evt_input):
        try:
            evt_input[0] = str(evt_input[0]).replace("{778", '{"778"')
            suota_noti = json.loads(evt_input[0])
            length = suota_noti["evt"]["len"]
            data = suota_noti["evt"]["hex"]
            data = data.replace("0x", "")
            indi_resp_byte_list = []
            for i in range(length):
                indi_resp_byte_list.append(int(data[(i * 2) : (i * 2) + 2], 16))
            indication_q.put(indi_resp_byte_list)
            print_dbg_msg(
                "Indication: " + str(binascii.hexlify(bytearray(indi_resp_byte_list)))
            )
        except Exception as e:
            print(str(e))


def connect_to_BleuIO(mac):
    global my_dongle
    global suota_avalible
    global browse_complete
    global bootloader_open
    suota_avalible = False
    browse_complete = False
    bootloader_open = False
    my_dongle.at_gapconnect(mac)
    CONN_TIMEOUT = 30
    conn_cnt = 0
    while not my_dongle.status.isConnected and conn_cnt < CONN_TIMEOUT:
        time.sleep(0.1)
        print("#", end="", flush=True)
        conn_cnt += 0.1
        pass
    if not my_dongle.status.isConnected:
        print(
            f"\n\n{bcolors.WARNING}-:CANNOT CONNECT TO BleuIO Dongle:-\r\n{bcolors.ENDC}"
        )
        my_dongle.at_cancel_connect()
        raise Exception("Cannot connect!")
    print("\n\n")
    print("Connected to " + mac + "\n")
    time.sleep(1)


def find_BleuIO(id):
    global my_dongle
    global bleuio_found
    global main_running
    global mac_addr
    bleuio_found = False
    print_dbg_msg("find_BleuIO(%s)" % (id))

    my_dongle.at_findscandata(id)
    SCAN_TIMEOUT = 130
    scan_cnt = 0
    while not bleuio_found and scan_cnt < SCAN_TIMEOUT:
        time.sleep(1)
        scan_cnt += 1
        if scan_cnt % 2 == 0:
            print("#", end="", flush=True)
        pass
    if not bleuio_found:
        print(
            f"\n\n{bcolors.WARNING}-:CANNOT FIND ANY BLEUIO DONGLE IN SOUTA MODE:-\r\n{bcolors.ENDC}Please make sure the BleuIO Dongle is in SUOTA mode and advertising then try again."
        )
        my_dongle.stop_scan()
        raise Exception("Cannot find BleuIO!")
    print("\n\n")
    my_dongle.stop_scan()
    mac_addr = str(mac_addr).upper()

    found_mac = "[0]" + mac_addr
    print(f"Found BleuIO Dongle ({mac_addr}).\n")

    time.sleep(0.5)
    return found_mac


# /**
#  ****************************************************************************************
#  * @brief Checks if the current block is the last block of the image.
#  *
#  * @return True if the current block is the last block of the image.
#  ****************************************************************************************
#  */
def is_last_block():
    global block_offset
    global block_length
    global patch_length
    return (block_offset + block_length) == patch_length


# /**
#  ****************************************************************************************
#  * @brief Advances current block to the next block of the image.
#  *
#  * If the current block is the last block of the image then no action is taken
#  ****************************************************************************************
#  */
def next_block():
    global block_offset
    global block_length
    global patch_length
    global suota_block_size
    if is_last_block():
        return

    # // update current block offset and length
    block_offset += block_length
    if (patch_length - block_offset) > suota_block_size:
        block_length = suota_block_size
    else:
        block_length = patch_length - block_offset


# /**
#  ****************************************************************************************
#  * @brief Checks if the current chunk of the current block is the last chunk of the block.
#  *
#  * @return True if the current chunk is the last chunk of the current block.
#  ****************************************************************************************
#  */
def is_last_chunk():
    global patch_chunck_offset
    global patch_chunck_length
    global block_length
    return (patch_chunck_offset + patch_chunck_length) == block_length


# /**
#  ****************************************************************************************
#  * @brief Advances current chunk to the next chunk of the current block.
#  *
#  * If the current chunk is the last chunk of the current block then no action is taken
#  ****************************************************************************************
#  */
def next_chunk():
    global patch_chunck_offset
    global patch_chunck_length
    global block_length
    global suota_chunk_size
    if is_last_chunk():
        return

    # // update next chunk offset and length
    patch_chunck_offset += patch_chunck_length
    if (block_length - patch_chunck_offset) > suota_chunk_size:
        patch_chunck_length = suota_chunk_size
    else:
        patch_chunck_length = block_length - patch_chunck_offset


# /**
#  ****************************************************************************************
#  * @brief Writes the current block length to SUOTA_PATCH_LEN characteristic
#  ****************************************************************************************
#  */
def app_suota_write_patch_len():
    global block_length

    value1 = block_length & 0xFF
    value2 = (block_length >> 8) & 0xFF
    value_str = "%02X%02X" % (value1, value2)
    if writeToChar(suota_patch_len_handle, value_str, False):
        print_dbg_msg("write_patch_len: " + value_str)
        return True
    else:
        return False


# /**
#  ****************************************************************************************
#  * @brief Writes the current chunk to SUOTA_PATCH_DATA characteristic
#  ****************************************************************************************
#  */
def app_suota_write_current_block_chunk():
    global patch_chunck_offset
    global patch_chunck_length
    global block_offset
    global expected_write_completion_events_counter

    value_str = ""

    for x in range(
        block_offset + patch_chunck_offset,
        (block_offset + patch_chunck_offset) + patch_chunck_length,
    ):
        value_str += "%02X" % (patch_data[x])

    if writeToChar(suota_patch_data_handle, value_str, True):
        if not expected_write_completion_events_counter <= 0:
            expected_write_completion_events_counter -= 1
        else:
            print(
                "expected_write_completion_events_counter error: %d"
                % (expected_write_completion_events_counter)
            )
    else:
        print("app_suota_write_current_block_chunk ERROR!")
        print_dbg_msg(value_str)


# /**
#  ****************************************************************************************
#  * @brief  Calculates and prints current upload progress
#  ****************************************************************************************
#  */
def app_suota_show_upload_progress():
    global block_length
    global block_offset
    global patch_length
    progress = ((block_offset + block_length) * 100) / patch_length
    try:
        response = notifications_q.get(timeout=DEFAULT_TIMEOUT)
        if not response == SUOTA_STATUS_CMP_OK:
            print("Image file error: %02X (%s)" % (response, error_list[response]))
            my_dongle.at_gapdisconnectall()
            if response == SUOTA_STATUS_SAME_IMAGE_ERROR:
                raise Exception("Device is already updated")
            if response == SUOTA_STATUS_INVALID_PRODUCT_HEADER:
                raise Exception("Invalid Product Header!")
            raise Exception("Image file error.")
    except:
        raise Exception("No response or error response!")
    if progress == 100:
        print("Upload complete.")
    else:
        print("Uploading : %.1f %% " % (progress))
        print_dbg_msg(
            "block_length: %d, block_offset: %d, patch_length:%d"
            % (block_length, block_offset, patch_length)
        )


# /**
#  ****************************************************************************************
#  * @brief  Writes current block to SUOTA_PATCH_DATA  in 20 byte chunks
#  ****************************************************************************************
#  */
def app_suota_write_chunks():
    # init 1st chunk of block
    global patch_chunck_length
    global patch_chunck_offset
    global block_length
    global expected_write_completion_events_counter
    patch_chunck_offset = 0  # offset in block

    if (block_length - patch_chunck_offset) > suota_chunk_size:
        patch_chunck_length = suota_chunk_size
    else:
        patch_chunck_length = block_length - patch_chunck_offset

    expected_write_completion_events_counter = 0
    while 1:
        expected_write_completion_events_counter += 1
        app_suota_write_current_block_chunk()
        if is_last_chunk():
            break
        next_chunk()
    app_suota_show_upload_progress()


# /**
#  ****************************************************************************************
#  * @brief  Sends the SUOTA END command
#  ****************************************************************************************
#  */
def app_suota_end():
    # SUOTA END
    value3 = 0xFE
    value2 = 0
    value1 = 0
    value0 = 0
    value_str = "%02X%02X%02X%02X" % (value0, value1, value2, value3)
    print_dbg_msg("app_suota_end: " + str(value_str))
    writeToChar(suota_mem_dev_handle, value_str, False)


def app_suota_reboot():
    # reboot
    value3 = 0xFD
    value2 = 0
    value1 = 0
    value0 = 0
    value_str = "%02X%02X%02X%02X" % (value0, value1, value2, value3)
    print_dbg_msg("app_suota_reboot: " + str(value_str))
    my_dongle.at_gattcwriteb(suota_mem_dev_handle, value_str)


def checksum(data, len):
    crc_code = 0
    i = 0

    # for(i = 0; i < len; i++)
    for i in range(0, len):
        crc_code ^= data[i]

    return crc_code


def writeToChar(handle, value, noResp):
    success = False
    if noResp:
        resp = my_dongle.at_gattcwritewrb(handle, value)
        if not resp.Ack["err"] == 0:
            print("AT Command error: %02X" % (resp.Ack["err"]))
        else:
            success = True
    else:
        resp = my_dongle.at_gattcwriteb(handle, value)
        if not resp.Ack["err"] == 0:
            print("AT Command error: %02X" % (resp.Ack["err"]))
            return success
        try:
            response = gattc_write_rsp_q.get(timeout=DEFAULT_TIMEOUT)
        except:
            print("No write confirmation!")
            print_dbg_msg("Write to Char: " + value)
            return success
        if response == 0:
            print_dbg_msg("BLE Write OK: %02X" % (response))
            success = True
        else:
            print("BLE Write error: %02X" % (response))
    return success


def main():
    global main_running
    global debug_msg
    global my_dongle
    global SSD00x_ID
    global mac_addr
    global suota_firmware_name
    global suota_avalible
    global suota_dat_file
    global suota_bin_file
    global bootloader_open

    global suota_block_size
    global current_block_length
    global suota_chunk_size

    global block_offset
    global block_length

    global patch_chunck_offset
    global patch_chunck_length

    global patch_length
    global patch_data_len
    global patch_data

    parser = argparse.ArgumentParser(
        "Requires SUOTA firmware img file to update BleuIO Dongle with."
    )
    parser.add_argument(
        "-fw",
        help="Requires SUOTA firmware img file to update BleuIO Dongle with.",
        required=True,
        default=None,
    )
    parser.add_argument("-dbg", "--debug", action="store_true", help="shows debug msg")
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        default="",
        help="Choose port used by dongle used to update. If note choosen the first port found used by a BleuIO Dongle will be used.",
    )
    args = parser.parse_args()

    suota_firmware_name = args.fw
    if args.debug:
        debug_msg = True

    custom_port = args.port
    if custom_port:
        my_dongle = BleuIO(port=custom_port)
    else:
        my_dongle = BleuIO()

    try:
        f = open(suota_firmware_name, "rb")
        patch_data = f.read()
        patch_length = len(patch_data)
        if patch_length > patch_data_len:
            print("Firmare file is too big.")
            f.close
            sys.exit(1)
        f.close
    except Exception as e:
        print(e)
        sys.exit(1)

    check = checksum(patch_data, patch_length)

    patch_data += bytes([check])
    patch_length += 1

    print(
        f"\n-BleuIO_SUOTA_SSD00X_Updater.py\n-Version: {bcolors.OKCYAN}{fw_version}{bcolors.ENDC}"
    )
    print(f"-Created: {bcolors.OKCYAN}{created}\r\n{bcolors.ENDC}")
    print(
        "-=:Welcome to Smart Sensor Devices Script for Updating the BleuIO Dongle Firmware (SUOTA):=-\r\n"
    )
    print_dbg_msg("File size: %d bytes" % (patch_length))

    # Init
    my_dongle.register_evt_cb(my_evt_callback)
    my_dongle.register_scan_cb(my_scan_callback)
    my_dongle.at_cancel_connect()
    my_dongle.at_gapdisconnectall()
    my_dongle.at_dual()
    my_dongle.ata(False)
    resp = my_dongle.send_command("AT+MTU=512")
    for r in resp:
        print_dbg_msg(r.decode("ascii"))

    update_done = False
    while not update_done:
        print_dbg_msg("Entring while not update_done")
        tryingToConnect = True
        err = False
        main_running = True
        while tryingToConnect:
            print(
                f"\r\nLooking to update BleuIO Dongle with fw: {suota_firmware_name}\r\n\r\n"
            )
            print_dbg_msg("Entring while tryingToConnect:")
            try:
                bleuio_mac = find_BleuIO(BLEUIO_SUOTA_ADV_DATA)
                print(
                    f"\nConnecting to BleuIO Dongle: {bcolors.OKCYAN} (MAC Addr: {mac_addr}){bcolors.ENDC}\n"
                )
                connect_to_BleuIO(bleuio_mac)
                tryingToConnect = False
                err = False
                print("Connect Success!")
            except Exception as e:
                print_dbg_msg(e)
                err = True
                tryingToConnect = False

        # main loop
        main_running_counter = 0
        try:
            while main_running:
                if err:
                    main_running = False
                    break
                if main_running_counter >= 250:
                    my_dongle.at_cancel_connect()
                    my_dongle.at_gapdisconnectall()
                    print("Failed to connect.")
                    main_running = False
                    break

                if my_dongle.status.isConnected and browse_complete:
                    if suota_avalible:
                        suota_block_size = 0
                        current_block_length = 0
                        suota_chunk_size = DEFAULT_DATA_CHUNK_SIZE

                        block_offset = 0
                        block_length = 0

                        patch_chunck_offset = 0
                        patch_chunck_length = 0
                        while not notifications_q.qsize() == 0:
                            temp_val = notifications_q.get()
                            print_dbg_msg(
                                "Get message from notifications_q: " + str(temp_val)
                            )
                            time.sleep(0.4)
                        my_dongle.at_set_noti(suota_serv_status_handle)
                        try:
                            my_dongle.at_gattcread(dis_fw_ver_handle)
                            fw_from_dis = gattc_read_q.get(timeout=DEFAULT_TIMEOUT)
                            print(
                                f"\nCurrent Firmware Version of BleuIO Dongle: {bcolors.OKCYAN}{fw_from_dis}{bcolors.ENDC}\n"
                            )
                        except:
                            print("Cannot read firmware version!")
                            pass
                        # Read SUOTA VERSION
                        try:
                            my_dongle.at_gattcread(suota_version_handle)
                            suota_ver = gattc_read_q.get(timeout=DEFAULT_TIMEOUT)
                            print(
                                f"\nSUOTA Version : {bcolors.OKCYAN}{suota_ver}{bcolors.ENDC}\n"
                            )
                        except:
                            print("Cannot read SUOTA version!")
                            main_running = False
                            my_dongle.at_gapdisconnectall()
                            raise Exception("Cannot read SUOTA version!")
                        print("Device support SUOTA.")
                        # Read MTU_SIZE
                        try:
                            my_dongle.at_gattcread(suota_mtu_handle)
                            mtu_size = gattc_read_q.get(timeout=DEFAULT_TIMEOUT)
                            print(
                                f"\nMTU_SIZE: {bcolors.OKCYAN}{mtu_size}{bcolors.ENDC}\n"
                            )
                        except:
                            print("Cannot read MTU_SIZE!")
                            main_running = False
                            my_dongle.at_gapdisconnectall()
                            raise Exception("Cannot read MTU_SIZE!")
                        # Read RD_PD_CHAR_SIZE
                        try:
                            my_dongle.at_gattcread(suota_pd_char_size_handle)
                            rd_pd_char_size = gattc_read_q.get(timeout=DEFAULT_TIMEOUT)
                            print(
                                f"PD_CHAR_SIZE: {bcolors.OKCYAN}{rd_pd_char_size}{bcolors.ENDC}\n"
                            )
                        except:
                            print("Cannot read RD_PD_CHAR_SIZE!")
                            main_running = False
                            my_dongle.at_gapdisconnectall()
                            raise Exception("Cannot read RD_PD_CHAR_SIZE!")

                        suota_chunk_size = min(
                            int(mtu_size) - ATT_HEADER_SIZE, int(rd_pd_char_size)
                        )
                        print_dbg_msg("suota_chunk_size: " + str(suota_chunk_size))

                        # Write mem_dev info SUOTA_MEM_DEV_SPI and Bank 0
                        writeToChar(suota_mem_dev_handle, "00000013", False)
                        response = notifications_q.get(timeout=DEFAULT_TIMEOUT)
                        if not response == SUOTA_STATUS_IMG_STARTED:
                            print(
                                "SUOTA_STATUS ERROR: %02X (%s)"
                                % (response, error_list[response])
                            )
                            main_running = False
                            my_dongle.at_gapdisconnectall()
                            raise Exception("Suota error!")
                        else:
                            print(
                                "Update started: %02X (%s)"
                                % (response, error_list[response])
                            )

                        # suota_chunk_size = 244
                        # suota_block_size = 509
                        suota_block_size = int(mtu_size)
                        if suota_chunk_size > suota_block_size:
                            suota_chunk_size = suota_block_size
                        else:
                            # Set block size to the closest possible value to the user input
                            suota_block_size = (
                                suota_block_size / suota_chunk_size
                            ) * suota_chunk_size
                            suota_block_size = int(suota_block_size)

                        if (patch_length - block_offset) > suota_block_size:
                            block_length = suota_block_size
                        else:
                            block_length = patch_length - block_offset

                        print_dbg_msg(
                            "Info: suota_chunk_size: %d  suota_block_size: %d  block_length %d"
                            % (suota_chunk_size, suota_block_size, block_length)
                        )

                        if not app_suota_write_patch_len():
                            main_running = False
                            my_dongle.at_gapdisconnectall()
                            raise Exception("Cannot write patch lenght!")
                        time.sleep(0.4)

                        done = False
                        print_dbg_msg(
                            "block_length: %d, block_offset: %d, patch_length:%d"
                            % (block_length, block_offset, patch_length)
                        )
                        start_time = time.time()
                        app_suota_write_chunks()

                        while not done and my_dongle.status.isConnected:
                            if is_last_block():
                                print("Done!")
                                done = True
                            else:
                                next_block()

                                if is_last_block():
                                    # we may need a different block length for the last block
                                    # trigger next step - write SUOTA_PATCH_LEN for last block
                                    if not app_suota_write_patch_len():
                                        main_running = False
                                        my_dongle.at_gapdisconnectall()
                                        raise Exception("Cannot write patch lenght!")
                                    time.sleep(0.4)
                                else:
                                    # trigger next step - start writing the block chunks
                                    app_suota_write_chunks()
                                    time.sleep(0.01)

                        # Write Last Chunk
                        app_suota_write_chunks()
                        end_time = time.time()

                        # Clearing the notification queue
                        while not notifications_q.qsize() == 0:
                            response = notifications_q.get_nowait()
                            if not response == SUOTA_STATUS_CMP_OK:
                                print(
                                    "ERROR: %02X (%s)"
                                    % (response, error_list[response])
                                )
                                main_running = False
                                my_dongle.at_gapdisconnectall()
                                raise Exception("Suota error %02X!" % (response))
                            else:
                                print(
                                    "OK: %02X (%s)" % (response, error_list[response])
                                )

                        app_suota_end()
                        try:
                            response = notifications_q.get(timeout=DEFAULT_TIMEOUT)
                            if not response == SUOTA_STATUS_CMP_OK:
                                print(
                                    f"\nUpdate Error: {bcolors.FAIL}{error_list[response]}{bcolors.ENDC}\n"
                                )
                            else:
                                print(
                                    f"{bcolors.OKGREEN}Update Successful: %02X %s{bcolors.ENDC}\n"
                                    % (response, error_list[response])
                                )
                        except:
                            print("app_suota_end no response!")

                        print("Image sent in %.2fs" % (end_time - start_time))

                        print("Rebooting BleuIO.")
                        app_suota_reboot()
                        print("BleuIO rebooted.")

                        my_dongle.at_gapdisconnectall()
                        while my_dongle.status.isConnected:
                            pass
                        main_running = False
                        print(
                            f"{bcolors.OKGREEN}BleuIO Updated Successfully!{bcolors.ENDC}\n"
                        )
                        # Update done
                        answer = input("Update another BleuIO Dongle? (y/n)\n>>")
                        answer = answer.lower()
                        if answer[0] == "y":
                            pass
                        else:
                            update_done = True
                    else:
                        print("Device doesn't support SUOTA.")
                        main_running = False
                        my_dongle.at_gapdisconnectall()
                        # Update not possible
                        answer = input("Do you want to try again? (y/n)\n>>")
                        answer = answer.lower()
                        if answer[0] == "y":
                            pass
                        else:
                            update_done = True

                pass
        except Exception as e:
            print(e)
        except (KeyboardInterrupt, SystemExit) as d:
            print("Exiting...")
            sys.exit(1)
        pass

    print("Script done. Shutting down...")
    sys.exit(1)


if __name__ == "__main__":
    main()
