import pyvisa, time
import sys, os, io

rm = pyvisa.ResourceManager('@py')

for r in rm.list_resources():
    if 'DS1Z' in r:
        print('Connecting over USB')
        rig = rm.open_resource(r)
        break

rig.timeout = 3000
rig.chunk_size = 32

print('device =', rig.query('*IDN?'))
time.sleep(0.1)

rig.write(':DISP:DATA? ON,OFF,PNG')
time.sleep(0.1)
buff = rig.read_raw()

open('scr.png', 'wb').write(buff[11:len(buff)-1])

rig.close()
