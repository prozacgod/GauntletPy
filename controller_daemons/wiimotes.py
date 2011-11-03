import sys, lightblue

WIIMOTE_DEVICE_NAME = 'Nintendo RVL-CNT-01'

devs = lightblue.finddevices(getnames=True, length=5)

wiimote = [d for d in devs if d[1] == WIIMOTE_DEVICE_NAME] and d[0] or None
if not wiimote:
    print "No wiimotes found!"
    sys.exit(1)

write_socket = lightblue.socket(lightblue.L2CAP)
write_socket.connect((wiimote, 0x11))

read_socket = lightblue.socket(lightblue.L2CAP)
read_socket.connect((wiimote, 0x13))

write_socket.send(hexbyte.HexToByte('52 12 00 33'))

while 1:
    byte = read_socket.recv(256 * 7)
    data = hexbyte.ByteToHex(byte)

    print " ".join("%02X" % ord(b) for b in data)

