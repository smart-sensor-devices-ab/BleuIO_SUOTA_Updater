# BleuIO SUOTA Updater Instructions

## Requirements

Python >= 3.5<br>
Python library [bleuio](https://pypi.org/project/bleuio/) >= 1.3.0

## Steps

- Download the desired firmare from our [Manual page](https://www.bleuio.com/getting_started/docs/firmware/). It is recommended to place the firmware image file into the same folder as the script.
- Open a command prompt where the script is located.
- Run: python BleuIO_SUOTA_Updater.py image_file_name.img
- The script will look for any BleuIO Dongle that is advertising in SUOTA mode and start updating the first it finds.
- “**BleuIO Updated Successfully!**” message will be shown on the screen once the process is completed.
- You will then be prompted "**Update another BleuIO Dongle? (y/n)**" if you choose **y** it will try to find and update another BleuIO Dongle. Choosing **n** will exit the script.

## Arguments

|   Arguments   |                                                     Descriptions                                                      |
| :-----------: | :-------------------------------------------------------------------------------------------------------------------: |
|  -h, --help   |                                            Show this help message and exit                                            |
|    -fw FW     |                            Requires SUOTA firmware img file to update BleuIO Dongle with.                             |
| -dbg, --debug |                                                 Shows debug messages                                                  |
|  -p, --port   | Choose port used by dongle used to update. If note choosen the first port found used by a BleuIO Dongle will be used. |

## Example

```cmd
python BleuIO_SUOTA_Updater.py -fw bleuio.2.4.1-release.img -p COM6

-BleuIO_SUOTA_SSD00X_Updater.py
-Version: 1.0.0
-Created: 2023-09-26

-=:Welcome to Smart Sensor Devices Script for Updating the BleuIO Dongle Firmware (SUOTA):=-


Looking to update BleuIO Dongle with fw: bleuio.2.4.1-release.img


#


Found BleuIO Dongle (00:00:00:00:00:28).


Connecting to BleuIO Dongle:  (MAC Addr: 00:00:00:00:00:28)

#####


Connected to [0]00:00:00:00:00:28

Connect Success!

Current Firmware Version of BleuIO Dongle: 2.4.0


SUOTA Version : 1.3

Device support SUOTA.

MTU_SIZE: 512

PD_CHAR_SIZE: 244

Update started: 10 (SUOTA_STATUS_IMG_STARTED)
Uploading : 0.3 %
Uploading : 0.5 %
Uploading : 0.8 %
Uploading : 1.0 %
Uploading : 1.3 %
Uploading : 1.5 %
Uploading : 1.8 %
Uploading : 2.0 %
Uploading : 2.3 %
Uploading : 2.5 %
Uploading : 2.8 %
Uploading : 3.0 %
Uploading : 3.3 %
Uploading : 3.5 %
Uploading : 3.8 %
Uploading : 4.0 %
Uploading : 4.3 %
Uploading : 4.5 %
Uploading : 4.8 %
Uploading : 5.0 %
Uploading : 5.3 %
Uploading : 5.5 %
Uploading : 5.8 %
Uploading : 6.0 %
Uploading : 6.3 %
Uploading : 6.5 %
Uploading : 6.8 %
Uploading : 7.0 %
Uploading : 7.3 %
Uploading : 7.5 %
Uploading : 7.8 %
Uploading : 8.0 %
Uploading : 8.3 %
Uploading : 8.5 %
Uploading : 8.8 %
Uploading : 9.0 %
Uploading : 9.3 %
Uploading : 9.5 %
Uploading : 9.8 %
Uploading : 10.0 %
Uploading : 10.3 %
Uploading : 10.5 %
Uploading : 10.8 %
Uploading : 11.0 %
Uploading : 11.3 %
Uploading : 11.5 %
Uploading : 11.8 %
Uploading : 12.0 %
Uploading : 12.3 %
Uploading : 12.5 %
Uploading : 12.8 %
Uploading : 13.0 %
Uploading : 13.3 %
Uploading : 13.5 %
Uploading : 13.8 %
Uploading : 14.0 %
Uploading : 14.3 %
Uploading : 14.5 %
Uploading : 14.8 %
Uploading : 15.0 %
Uploading : 15.3 %
Uploading : 15.5 %
Uploading : 15.8 %
Uploading : 16.0 %
Uploading : 16.3 %
Uploading : 16.5 %
Uploading : 16.8 %
Uploading : 17.0 %
Uploading : 17.3 %
Uploading : 17.5 %
Uploading : 17.8 %
Uploading : 18.0 %
Uploading : 18.3 %
Uploading : 18.5 %
Uploading : 18.8 %
Uploading : 19.0 %
Uploading : 19.3 %
Uploading : 19.5 %
Uploading : 19.8 %
Uploading : 20.0 %
Uploading : 20.3 %
Uploading : 20.5 %
Uploading : 20.8 %
Uploading : 21.1 %
Uploading : 21.3 %
Uploading : 21.6 %
Uploading : 21.8 %
Uploading : 22.1 %
Uploading : 22.3 %
Uploading : 22.6 %
Uploading : 22.8 %
Uploading : 23.1 %
Uploading : 23.3 %
Uploading : 23.6 %
Uploading : 23.8 %
Uploading : 24.1 %
Uploading : 24.3 %
Uploading : 24.6 %
Uploading : 24.8 %
Uploading : 25.1 %
Uploading : 25.3 %
Uploading : 25.6 %
Uploading : 25.8 %
Uploading : 26.1 %
Uploading : 26.3 %
Uploading : 26.6 %
Uploading : 26.8 %
Uploading : 27.1 %
Uploading : 27.3 %
Uploading : 27.6 %
Uploading : 27.8 %
Uploading : 28.1 %
Uploading : 28.3 %
Uploading : 28.6 %
Uploading : 28.8 %
Uploading : 29.1 %
Uploading : 29.3 %
Uploading : 29.6 %
Uploading : 29.8 %
Uploading : 30.1 %
Uploading : 30.3 %
Uploading : 30.6 %
Uploading : 30.8 %
Uploading : 31.1 %
Uploading : 31.3 %
Uploading : 31.6 %
Uploading : 31.8 %
Uploading : 32.1 %
Uploading : 32.3 %
Uploading : 32.6 %
Uploading : 32.8 %
Uploading : 33.1 %
Uploading : 33.3 %
Uploading : 33.6 %
Uploading : 33.8 %
Uploading : 34.1 %
Uploading : 34.3 %
Uploading : 34.6 %
Uploading : 34.8 %
Uploading : 35.1 %
Uploading : 35.3 %
Uploading : 35.6 %
Uploading : 35.8 %
Uploading : 36.1 %
Uploading : 36.3 %
Uploading : 36.6 %
Uploading : 36.8 %
Uploading : 37.1 %
Uploading : 37.3 %
Uploading : 37.6 %
Uploading : 37.8 %
Uploading : 38.1 %
Uploading : 38.3 %
Uploading : 38.6 %
Uploading : 38.8 %
Uploading : 39.1 %
Uploading : 39.3 %
Uploading : 39.6 %
Uploading : 39.8 %
Uploading : 40.1 %
Uploading : 40.3 %
Uploading : 40.6 %
Uploading : 40.8 %
Uploading : 41.1 %
Uploading : 41.3 %
Uploading : 41.6 %
Uploading : 41.9 %
Uploading : 42.1 %
Uploading : 42.4 %
Uploading : 42.6 %
Uploading : 42.9 %
Uploading : 43.1 %
Uploading : 43.4 %
Uploading : 43.6 %
Uploading : 43.9 %
Uploading : 44.1 %
Uploading : 44.4 %
Uploading : 44.6 %
Uploading : 44.9 %
Uploading : 45.1 %
Uploading : 45.4 %
Uploading : 45.6 %
Uploading : 45.9 %
Uploading : 46.1 %
Uploading : 46.4 %
Uploading : 46.6 %
Uploading : 46.9 %
Uploading : 47.1 %
Uploading : 47.4 %
Uploading : 47.6 %
Uploading : 47.9 %
Uploading : 48.1 %
Uploading : 48.4 %
Uploading : 48.6 %
Uploading : 48.9 %
Uploading : 49.1 %
Uploading : 49.4 %
Uploading : 49.6 %
Uploading : 49.9 %
Uploading : 50.1 %
Uploading : 50.4 %
Uploading : 50.6 %
Uploading : 50.9 %
Uploading : 51.1 %
Uploading : 51.4 %
Uploading : 51.6 %
Uploading : 51.9 %
Uploading : 52.1 %
Uploading : 52.4 %
Uploading : 52.6 %
Uploading : 52.9 %
Uploading : 53.1 %
Uploading : 53.4 %
Uploading : 53.6 %
Uploading : 53.9 %
Uploading : 54.1 %
Uploading : 54.4 %
Uploading : 54.6 %
Uploading : 54.9 %
Uploading : 55.1 %
Uploading : 55.4 %
Uploading : 55.6 %
Uploading : 55.9 %
Uploading : 56.1 %
Uploading : 56.4 %
Uploading : 56.6 %
Uploading : 56.9 %
Uploading : 57.1 %
Uploading : 57.4 %
Uploading : 57.6 %
Uploading : 57.9 %
Uploading : 58.1 %
Uploading : 58.4 %
Uploading : 58.6 %
Uploading : 58.9 %
Uploading : 59.1 %
Uploading : 59.4 %
Uploading : 59.6 %
Uploading : 59.9 %
Uploading : 60.1 %
Uploading : 60.4 %
Uploading : 60.6 %
Uploading : 60.9 %
Uploading : 61.1 %
Uploading : 61.4 %
Uploading : 61.6 %
Uploading : 61.9 %
Uploading : 62.1 %
Uploading : 62.4 %
Uploading : 62.7 %
Uploading : 62.9 %
Uploading : 63.2 %
Uploading : 63.4 %
Uploading : 63.7 %
Uploading : 63.9 %
Uploading : 64.2 %
Uploading : 64.4 %
Uploading : 64.7 %
Uploading : 64.9 %
Uploading : 65.2 %
Uploading : 65.4 %
Uploading : 65.7 %
Uploading : 65.9 %
Uploading : 66.2 %
Uploading : 66.4 %
Uploading : 66.7 %
Uploading : 66.9 %
Uploading : 67.2 %
Uploading : 67.4 %
Uploading : 67.7 %
Uploading : 67.9 %
Uploading : 68.2 %
Uploading : 68.4 %
Uploading : 68.7 %
Uploading : 68.9 %
Uploading : 69.2 %
Uploading : 69.4 %
Uploading : 69.7 %
Uploading : 69.9 %
Uploading : 70.2 %
Uploading : 70.4 %
Uploading : 70.7 %
Uploading : 70.9 %
Uploading : 71.2 %
Uploading : 71.4 %
Uploading : 71.7 %
Uploading : 71.9 %
Uploading : 72.2 %
Uploading : 72.4 %
Uploading : 72.7 %
Uploading : 72.9 %
Uploading : 73.2 %
Uploading : 73.4 %
Uploading : 73.7 %
Uploading : 73.9 %
Uploading : 74.2 %
Uploading : 74.4 %
Uploading : 74.7 %
Uploading : 74.9 %
Uploading : 75.2 %
Uploading : 75.4 %
Uploading : 75.7 %
Uploading : 75.9 %
Uploading : 76.2 %
Uploading : 76.4 %
Uploading : 76.7 %
Uploading : 76.9 %
Uploading : 77.2 %
Uploading : 77.4 %
Uploading : 77.7 %
Uploading : 77.9 %
Uploading : 78.2 %
Uploading : 78.4 %
Uploading : 78.7 %
Uploading : 78.9 %
Uploading : 79.2 %
Uploading : 79.4 %
Uploading : 79.7 %
Uploading : 79.9 %
Uploading : 80.2 %
Uploading : 80.4 %
Uploading : 80.7 %
Uploading : 80.9 %
Uploading : 81.2 %
Uploading : 81.4 %
Uploading : 81.7 %
Uploading : 81.9 %
Uploading : 82.2 %
Uploading : 82.4 %
Uploading : 82.7 %
Uploading : 82.9 %
Uploading : 83.2 %
Uploading : 83.5 %
Uploading : 83.7 %
Uploading : 84.0 %
Uploading : 84.2 %
Uploading : 84.5 %
Uploading : 84.7 %
Uploading : 85.0 %
Uploading : 85.2 %
Uploading : 85.5 %
Uploading : 85.7 %
Uploading : 86.0 %
Uploading : 86.2 %
Uploading : 86.5 %
Uploading : 86.7 %
Uploading : 87.0 %
Uploading : 87.2 %
Uploading : 87.5 %
Uploading : 87.7 %
Uploading : 88.0 %
Uploading : 88.2 %
Uploading : 88.5 %
Uploading : 88.7 %
Uploading : 89.0 %
Uploading : 89.2 %
Uploading : 89.5 %
Uploading : 89.7 %
Uploading : 90.0 %
Uploading : 90.2 %
Uploading : 90.5 %
Uploading : 90.7 %
Uploading : 91.0 %
Uploading : 91.2 %
Uploading : 91.5 %
Uploading : 91.7 %
Uploading : 92.0 %
Uploading : 92.2 %
Uploading : 92.5 %
Uploading : 92.7 %
Uploading : 93.0 %
Uploading : 93.2 %
Uploading : 93.5 %
Uploading : 93.7 %
Uploading : 94.0 %
Uploading : 94.2 %
Uploading : 94.5 %
Uploading : 94.7 %
Uploading : 95.0 %
Uploading : 95.2 %
Uploading : 95.5 %
Uploading : 95.7 %
Uploading : 96.0 %
Uploading : 96.2 %
Uploading : 96.5 %
Uploading : 96.7 %
Uploading : 97.0 %
Uploading : 97.2 %
Uploading : 97.5 %
Uploading : 97.7 %
Uploading : 98.0 %
Uploading : 98.2 %
Uploading : 98.5 %
Uploading : 98.7 %
Uploading : 99.0 %
Uploading : 99.2 %
Uploading : 99.5 %
Uploading : 99.7 %
Uploading : 100.0 %
Uploading : 100 %%
Done!
Upload complete.
Update Successful: 02 SUOTA_STATUS_CMP_OK

Image sent in 87.75s
Rebooting BleuIO.
BleuIO rebooted.
Disconnected from BleuIO Dongle.
BleuIO Updated Successfully!

Update another BleuIO Dongle? (y/n)
>>n
Script done. Shutting down...
```
