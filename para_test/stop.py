import serial


move_serial = serial.Serial("COM1",baudrate=152000)
k210_serial = serial.Serial("COM3",baudrate=152000)

while True:
    data_k2l0 = k210_serial.readline().decode()
    data_move = move_serial.readline().decode()
    print("data_k2l0",data_k2l0)
    print("data_move",data_move)
    if data_k2l0 == "ok":
        arr = "@|5|" + str(0) + "|" + str(0) + "|" + str(0) + "#"
        move_serial.write(arr.encode("ascii"))
        break