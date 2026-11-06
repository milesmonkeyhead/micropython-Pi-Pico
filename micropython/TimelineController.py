import network, socket, time

ssid = 'TFS Students'
password = 'Fultoneagles'

serverIP = '10.1.0.151'
serverPort = 80

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
   
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected ')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

addr = socket.getaddrinfo(serverIP, serverPort)[0][-1]

s = socket.socket()
s.settimeout(3.0)
print('Connecting to server:', addr)
s.connect(addr)

confirm = 0.0
date = -3500

try:
    while True:
        confirm += 1
        date = "date from encoder"
        print(confirm)
        
        if confirm >= 10:
            try:
                http_request = (
                    f"GET /submit?date={date} HTTP/1.1\r\n"
                    f"Host: {serverIP}\r\n"
                    "Connection: keep-alive\r\n\r\n"
                )

                s.send(bytes(http_request, 'utf8'))
                        
                print('waiting for response')
                response = s.recv(1024)
                print(response.decode('utf8'))
                
                confirm = 0
                continue

            except OSError as e:
                print('communication error:', e, "reconnecting...")
                try:
                    s.close()
                except:
                    pass
                
                s = socket.socket()
                s.settimeout(3.0)
                s.connect(addr)
                print('reconnected successsfully')
                          
        time.sleep(0.1)
        
finally:
    s.close()
    print('socket closed successfully')