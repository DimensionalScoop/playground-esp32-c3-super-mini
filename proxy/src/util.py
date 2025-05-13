import network
import time

def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
    sta = network.WLAN(network.WLAN.IF_STA)
    sta.active(False)
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    while sta.isconnected():
        time.sleep(0.1)
    return sta, ap

# micropython docs claim that this makes the wifi more reliable
# after resets
# sta, ap = wifi_reset()
