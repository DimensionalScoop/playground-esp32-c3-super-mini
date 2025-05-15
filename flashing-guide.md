# Flashing Guide

for the ESP32-C3 (specific chip) Super Mini (board)


## Install the MicroPython interpreter

- install the esptool
  - `pacman -S esptool` for arch
  - `uv tool install esptool` on any python installation 
- https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
- download the latest MicroPython image specific to the chip (and maybe to the board)
  - https://micropython.org/resources/firmware/ESP32_GENERIC_C3-20250415-v1.25.0.bin
- connect the board via USB, flash the image
  - `esptool.py erase_flash`
  - `esptool.py --baud 460800 write_flash 0 ESP32_BOARD_NAME-DATE-VERSION.bin`
- done, a REPL is running and accesible thru the serial interface
  - e.g. `picocom -b 115200 /dev/ttyACM0`

- docs
  - https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
  - https://micropython.org/download/ESP32_GENERIC_C3/

## Run Code on the ESP32

either:
- copy your code directly to the REPL via the serial port
- use `mpremote`, a nice CLI tool for interfacing witht the ESP
- use an IDE like
  - thonny (easy, all important features are there, single-purpose)
    - autocomplete doesn't work that well
    - package installations only work in python 3.11!
  - pycharm + micro python tools plugin (powerfull, hard
    - vim plugin + helix-style vimrc are available
    - type stubs for autocomplete: https://micropython-stubs.readthedocs.io/en/main/24_pycharm.html
  - type stubs: https://pypi.org/project/micropython-esp32-esp32_generic_c3-stubs/
