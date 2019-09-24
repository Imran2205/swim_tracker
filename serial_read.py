
import serial
import time
from time import sleep
import serial.tools.list_ports
from array import array
ser=['a']


serp = serial.tools.list_ports.comports(include_links=False)




def set_port(portno):
    print(portno)
    try:
        if str(portno) != '':
            #print("Aaa")
            portno = portno
            #print("Aaa")
        else:
            #print("Bbb")
            port = serial.tools.list_ports.comports(include_links=False)
            portno=port[0]
            #print("Bbb")


        print(portno)
        ser[0] = serial.Serial(portno.device, 9600, timeout=0.005)
        print(ser[0])

        return 1
    except:
        return 0


def ston(S):
    sum = 0
    if len(S)>=3:
        for x in range(3,len(S)):
            iv=S[x]

            if iv>=48 and iv<=57:
                sum=(sum*10)+(iv-48)


    return sum

def give_value():
    try:
        S = ser[0].readline()
        return S
    except:
        b = input("enter:")
        d= bytearray()
        d.extend(map(ord,b))
        return d


def send_value(input):
    #print('ok')
    try:
        print('ok')
        ser[0].write(input)
        print(input)
        print('ok')
        return 1
    except:
        return 0