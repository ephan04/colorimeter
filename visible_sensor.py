from time import sleep
import board
import busio
from adafruit_as7341 import AS7341

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = AS7341(i2c)

# Set LED current in milliamps (4–258 mA, even values)
sensor.led_current = 4

# Define wavelengths
wavelengths = ["415nm", "445nm", "480nm", "515nm", "555nm", 
               "590nm", "630nm", "680nm", "Clear", "NIR"]

# Read sensor values with LED ON
def read_light():
    sensor.led = True
    sleep(0.2)  # Wait for light to stabilize
    readings = [
        sensor.channel_415nm,
        sensor.channel_445nm,
        sensor.channel_480nm,
        sensor.channel_515nm,
        sensor.channel_555nm,
        sensor.channel_590nm,
        sensor.channel_630nm,
        sensor.channel_680nm,
        sensor.channel_clear,
        sensor.channel_nir,
    ]
    sensor.led = False
    return readings

# Data storage
sample_names = []
raw_data_dict = {wl: [] for wl in wavelengths}
normalized_dict = {wl: [] for wl in wavelengths}

# Sample collection loop
while True:
    sample_id = input("Name your sample: ").strip()

    # Confirm sample is placed
    while input("Have you put the sample in properly? (yes/no) ").strip().lower() not in ["yes", "y"]:
        print("Put the sample in properly.")

    print("Measuring light...")
    readings = read_light()
    print(f"Raw Reading: {readings}")

    clear_value = readings[8] if readings[8] != 0 else 1  # Avoid divide-by-zero

    sample_names.append(sample_id)

    for i, wl in enumerate(wavelengths):
        raw_data_dict[wl].append(readings[i])
        normalized_value = readings[i] / clear_value
        normalized_dict[wl].append(round(normalized_value, 4))

    # Ask if another sample is needed
    if input("Do you want to take another sample? (yes/no) ").strip().lower() not in ["yes", "y"]:
        print("Finished data collection!")
        break

# Raw data input
print("\n Raw Intensity Data:")
output_raw = "Wavelength," + ",".join(sample_names) + "\n"
for wl in wavelengths:
    row = wl + "," + ",".join(map(str, raw_data_dict[wl])) + "\n"
    output_raw += row
print(output_raw)

# Normalized data input 
print("Normalized Data (relative to Clear):")
output_norm = "Wavelength," + ",".join(sample_names) + "\n"
for wl in wavelengths:
    row = wl + "," + ",".join(map(str, normalized_dict[wl])) + "\n"
    output_norm += row
print(output_norm)
