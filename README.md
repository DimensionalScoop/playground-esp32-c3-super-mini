# ESP32-C3 Playground
small experiments with a low-power, cheap microcontroller.

## Sensor to Database Architecture
Goal: Collect environmental measurements like temperature, sun intensity, soil water content, etc.

- Client: take measures and send them out measurements using ESP-NOW (protocol using wifi; compared to "normal" wifi: higher range and lower power requirements, no IP stack).
Runs on a constrained power base: A small solar-powered battery charges up a large capacitor (~10µF). This capacitor powers the ESP, as only supplies very little power. The capacitor holds enough charge to send out about 7 packages (0.2 to 2 KB) and needs to recharge for ~10s (under optimal conditions).

- Proxy: receive ESP-NOW packages and forward them over WIFI to a server. Is permanently connected to an outlet. Might also receive data via a serial interface.

- Server: A python programm that receives data via a REST-API and writes them to a off-the-shelf DB.
