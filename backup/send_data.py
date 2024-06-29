import serial
import time

# Set up the serial connection (adjust 'COMz3' to your Arduino's port)
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

# Give some time for the connection to establish
time.sleep(2)

def send_bit(bit):
    if bit in [0, 1]:
        # Convert bit to string and encode it to bytes
        arduino.write(str(bit).encode())
        print("sent bit ",bit)
    else:
        print("Invalid bit. Please send 0 or 1.")

# Example: send a bit '1' to turn on the LED

# Close the serial connection
arduino.close()
