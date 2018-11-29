# samsung-vfd-python
Python driver implementation for Samsung/Samtron VFD, type 20S204DA2

# Usage
- Install `pyserial`:
```
pip install pyserial
```
- Import `samvfd` into your project
- Create a `SamVfd` instance and pass the desired COM port:
```
vfd = SamVfd("COM5")
```
If your display is configured for slower serial communication than 9600 bps, pass the `baud_rate` parameter as well.