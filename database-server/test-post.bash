curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{
     "mac_address": "AA:BB:CC:DD:EE:FF",
    "rssi": -10,
     "data": "test curl"
  }'
