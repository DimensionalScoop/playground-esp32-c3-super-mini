import network
import espnow
import time
from micropython import const

from secrets import WIFI_SSID, WIFI_PASSWORD

TIMEOUT = const(100)
ACK = const(True)

# Connect to the internet
sta = network.WLAN(network.WLAN.IF_STA)
sta.connect(WIFI_SSID, WIFI_PASSWORD)
while not sta.isconnected():
    time.sleep_ms(1)
# Disable power management
sta.config(pm=sta.PM_NONE)

# When connected to an existing access point, we can only use the AP's channel
# for ESP-NOW.
assert sta.config("channel") == 13, "Channel changed!"
print("Proxy running on channel:", sta.config("channel"))

now = espnow.ESPNow()
now.active(True)

while True:
    # pull next package from buffer queue
    # (or wait up to TIMEOUT for a new package if the queue is empty)
    sender, msg = now.recv(TIMEOUT)
    # sender: mac address of sender
    if msg:
        # RSSI: Signal strength in dBm
        # timestamp: local clock, package arrival time in ms since boot
        rssi, timestamp = now.peers_table[sender]
        print(sender, rssi, msg)
        if ACK:
            try:
                # to send messages to a specific address, we need to add it to the
                # peer list first
                now.add_peer(sender)
            except OSError:
                # XXX: a bit hacky, add_peer raises an exception if the peer is already registered
                pass
            # Don't sync, we don't want to wait for a response
            now.send(mac=sender, msg="ACK", sync=False)