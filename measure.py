import pyvisa, time

print('opening scope..')
rm = pyvisa.ResourceManager('@py')
for i in rm.list_resources():
    if 'DS1Z' in i:
        rig = rm.open_resource(i)
        break
else:
    print('no instrument found :(')
    exit()

rig.chunk_size = 32

for i in range(100):
    q = rig.query(':MEAS:VAVG? CHAN1')
    v = float(q.split()[0])
    print(v)

rig.close()
