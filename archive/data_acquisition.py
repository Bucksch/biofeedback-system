import bluetooth
import asyncio
from bleak import BleakScanner

# nearby_devices = bluetooth.discover_devices(lookup_names=True)
# print("Found {} devices.".format(len(nearby_devices)))

# for addr, name in nearby_devices:
#     print("{} - {}".format(addr, name))

# def scan():

#     print("Scanning for bluetooth devices:")

#     devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)

#     number_of_devices = len(devices)

#     print(number_of_devices,"devices found")

#     for addr, name, device_class in devices:

#         print("\n")

#         print("Device:")

#         print("Device Name: %s" % (name))

#         print("Device MAC Address: %s" % (addr))

#         print("Device Class: %s" % (device_class))

#         print("\n")

#     return

# scan()

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)


asyncio.run(main())


# def get_data_from_device(addr, port):
#     sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#     sock.connect((addr, port))

#     data = ""
#     try:
#         while True:
#             data += sock.recv(1024)
#             print("Received [%s]" % data)
#     except KeyboardInterrupt:
#         print("Disconnected")

#     sock.close()

# Replace the address and port with the address and port of your device
#get_data_from_device('00:00:00:00:00:00', 1)