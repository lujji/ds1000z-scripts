import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from threading import Thread, Event
from time import sleep
from pyvisa import ResourceManager
import numpy as np

def scope(curve, event):
    rm = ResourceManager('@py')

    def rig_open():
        for r in rm.list_resources():
            if 'DS1Z' in r:
                print('Connecting over USB')
                rig = rm.open_resource(r)
                break
        else:
            print('Scope not found')
            exit()

        rig.chunk_size = 32
        print('device =', rig.query('*IDN?'))
        rig.timeout = 100
        rig.write(':WAV:MODE RAW') # NORM/RAW
        rig.write(':WAV:SOURce CHAN1')
        rig.write(':WAV:STAR 1')
        rig.write(':WAV:STOP 1200')

        return rig

    rig = rig_open()

    while event.is_set():
        try:
            buff = rig.query_binary_values(':WAV:DATA?', datatype='B')
        except:
            print('pass')
            continue

        curve.setData(buff)
        sleep(0.01)

    print("thread is done =(")
    rig.close()

app = pg.mkQApp("scope")
pg.PlotWidget().useOpenGL(True)

win = pg.GraphicsLayoutWidget()
win.show()

plt = win.addPlot()
plt.addLegend()
plt.showGrid(x=True, y=True, alpha=1.0)
curve = plt.plot(pen='r', name='x') #symbol = 'o'
plt.setYRange(0, 256, padding=0)
plt.setXRange(0, 1200, padding=0)

e = Event()
e.set()
scope_thread = Thread(
    target=scope,
    args=(curve, e,)
)
scope_thread.start()

app.exec()

e.clear()
