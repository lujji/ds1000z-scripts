# ds1000z-scripts
Collection of python scripts for communicating with Rigol DS1000Z series. USB is used by default, see wave.py for Ethernet example. More info can be found [here](https://lujji.github.io/blog/power-analysis-with-ds1000z/).

## Dependencies
```
# required for communicating with the scope
pip install pyvisa-py pyusb

# plotting and signal processing
pip install numpy scipy matplotlib
```

## Scripts
- measure.py - simple measurement example
- screenshot.py - takes a screenshot
- wave.py - real-time-plot using matplotlib
- wave_pyqt.py - real-time plot using qt (requires `pyqtgraph`)
- power_analysis.py - performs a number of single captures, uses deep memory; mem-depth has to be set manually on the scope
- align.py - aligns traces captured with previous script
