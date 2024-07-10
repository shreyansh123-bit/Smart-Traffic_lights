import serial
from time import sleep

arduino = serial.Serial(port='COM7', baudrate=9600,timeout=1)  #Set up the serial connection (adjust 'COM6' to your Arduino's port)
sleep(2)  # Give some time for the connection to establish

print("connection established with Arduino\n")
def sendbit(bit):
    if bit in (0, 1):
        # Convert bit to string and encode it to bytes
        arduino.write(str(bit).encode())
        print("sent bit ", bit)
    else:
        print("Invalid bit. Please send 0 or 1.")
