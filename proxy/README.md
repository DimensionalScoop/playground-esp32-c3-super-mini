# ESP-NOW Gateway

A simple proxy between ESP-NOW (a long-range, connectionless, low-power protocol for wifi) and the internet.
The gateway connects to a wifi access point and listens for ESP-NOW packages.
It passes all packages onto a server, probably via HTTP/POST.
