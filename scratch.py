import zlib
import base64

zipped_data = '7ZTPCsIwDMbfJedN0jT9s16Hb6AXxcOQgYLsMHcbe3dn8SA43VhOQi9pafsj+VLy9bBtuvZa3yEce9h3ZwhASJwrytHvFAdtgsYNsseC3QEyKKt2fN2DeobyUjVNfYsHCAEzoBh1jAxBIWdgXiuPGxyGePHBki18xO0srlCQW80V7qZhFeGpyhdntotgjCi+g16QlSTNIpLAeqVeknSZnADWkmbxMr1fYIlmYwSwlUyylWh2K78qjqJfX/aI/zI7bT2y1cnsktkls0tm9/dmdxoe'
unzipped_data = zlib.decompress(base64.b64decode(zipped_data), -zlib.MAX_WBITS)
data = unzipped_data.decode('utf-8-sig')

print(data)