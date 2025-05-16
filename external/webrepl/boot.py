import secrets
import network
import webrepl
import machine

sta = network.WLAN()
sta.active(True)
sta.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

while not sta.isconnected():
    machine.idle()

INTERNAL_LED_PIN = const(8)
led = machine.Pin(INTERNAL_LED_PIN, machine.Pin.OUT)
led.off()  # actually turns the led on

webrepl.start()
