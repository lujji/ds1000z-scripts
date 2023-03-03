import pyvisa, time
import matplotlib.pyplot as plt
import atexit

# scope VISA address (when connecting over LAN)
IP = 'TCPIP0::169.254.145.64::INSTR'

rm = pyvisa.ResourceManager('@py')
for r in rm.list_resources():
    if 'DS1Z' in r:
        print('Connecting over USB')
        rig = rm.open_resource(r)
        break
else:
    print('Connecting over TCP/IP')
    rig = rm.open_resource(IP)

atexit.register(lambda : rig.close())

rig.timeout = 5000
rig.chunk_size = 32

print('device =', rig.query('*IDN?'))
rig.write(':WAV:MODE RAW')

fig = plt.gcf()
plt.ion()
plt.show()

while True:
    buf = rig.query_binary_values(':WAV:DATA? CH1', datatype='B')
    plt0 = fig.add_subplot(111)
    plt0.set_ylim([0,255])
    plt0.grid(True)
    plt.plot(buf)
    plt.pause(0.2)
    fig.canvas.draw()
    plt0.remove()

    fig.canvas.draw()
