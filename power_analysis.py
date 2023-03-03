import time
from pyvisa import ResourceManager
from math import ceil

# number of traces to capture
TRACES_COUNT = 2

# scope VISA address (when connecting over LAN)
IP = 'TCPIP0::169.254.145.64::INSTR'

rm = ResourceManager('@py')
for r in rm.list_resources():
    if 'DS1Z' in r:
        print('Connecting over USB')
        rig = rm.open_resource(r)
        break
else:
    print('Connecting over TCP/IP')
    rig = rm.open_resource(IP)

if not rig:
    print('Scope not found')
    exit()


rig.timeout = 1500
rig.chunk_size = 32
max_points = 250_000 # safe up to 250k

print('device:', rig.query('*IDN?'))
rig.write(':WAV:MODE RAW')
rig.write(':WAV:FORM BYTE')

mem = int(rig.query(':ACQ:MDEP?'))
if max_points > mem: max_points = mem
f = open(time.strftime('%b-%d-%Y_%H-%M-%S', time.localtime()) + '_trace.csv', 'w')

for trace in range(TRACES_COUNT):
    # single capture
    rig.write(':SING')
    print('waiting for trigger..')
    time.sleep(0.3) # STOP->WAIT transition takes a while
    while True:
        if 'STOP' in rig.query(':TRIG:STAT?'):
            break
        time.sleep(0.1)

    # deep memory read
    buf = []
    for i in range (ceil(mem / max_points)):
        start = i * max_points
        stop = start + max_points
        stop = mem if stop > mem else stop
        time.sleep(0.01)
        rig.write(f':WAV:STAR {start + 1}')
        rig.write(f':WAV:STOP {stop}')

        for retries in range(10):
            try:
                tmp = rig.query_binary_values(':WAV:DATA? CH1', datatype='B')
                if len(tmp) != stop - start:
                    print(f'got {len(tmp)}/{stop - start} bytes - retrying')
                    continue
                buf += tmp
                break
            except:
                print('retrying')
        else:
            print('too many retries - quitting')
            break
        print(f'chunk {i}: {len(buf)}')

    f.write(','.join([str(v) for v in buf]) + '\n')

f.close()
rig.close()
