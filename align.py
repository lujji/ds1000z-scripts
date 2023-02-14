import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.ndimage import shift

with open('trace.csv', 'r') as f:
    # process the first trace
    a = [int(i) for i in f.readline().split(',')]
    a -= np.mean(a)
    averaged_trace = a[:]

    l = f.readline()
    n = 0
    while l:
        b = [int(i) for i in l.split(',')]
        b -= np.mean(b)

        # align using cross-correlation
        cor = signal.correlate(a, b)
        px, py = signal.find_peaks(cor, height=0)
        peak_x = px[np.argmax(py['peak_heights'])]
        offset = len(a) - peak_x - 1 # a -> b offset
        b = shift(b, -offset, cval=np.median(b))

        # moving average
        averaged_trace = [(b[i] + n*averaged_trace[i])/(n + 1) for i in range(len(b))]

        n += 1
        l = f.readline()

plt.grid(True)
plt.plot(a, alpha=0.9)
plt.plot(averaged_trace)
plt.show()
