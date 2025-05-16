# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import network
import espnow
import machine
import esp


network.country("DE")
print(network.country())

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
sta.active(True)
sta.config(channel=13)

e = espnow.ESPNow()
e.active(True)
BROADCAST = const(b"\xff\xff\xff\xff\xff\xff")
peer = BROADCAST
# peer = b'4\xcd\xb0\xd0\x98\xf8'
# e.add_peer(peer)      # Must add_peer() before send()

bcast = b"\xff" * 6
e.add_peer(bcast)

led = machine.Pin(8, machine.Pin.OUT)
led.off()

pin = machine.PWM(machine.Pin(0), freq=4_000_000, duty_u16=32768)
signal = 300

while True:
    machine.idle()
    pin.duty(signal)
    if signal > 0:
        signal = signal - 1

    e.send(bcast, "Hello World!")
    host, msg = e.recv(1)
    led.on()
    if host:
        rssi, timestamp = e.peers_table[host]

        signal_strength = int(1000 * (100 + rssi) / 100)
        # print(signal_strength)
        signal_strength = min(1023, signal_strength)
        signal_strength = max(100, signal_strength)
        # print(rssi, signal_strength)
        signal = signal_strength
        led.off()


# e.send(peer , "Starting...")
# for i in range(100):
#    e.send(peer, str(i)*20, True)
# e.send(peer, b'end')

# import webrepl
# webrepl.start()
