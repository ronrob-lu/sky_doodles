import struct
import zlib

def create_black_png():
    width, height = 1, 1
    # IHDR
    ihdr = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = b'IHDR' + ihdr
    ihdr_crc = struct.pack("!I", zlib.crc32(ihdr_chunk) & 0xFFFFFFFF)

    # IDAT (1 pixel black)
    raw_data = b'\x00\x00\x00\x00' # filter byte + RGB
    idat = zlib.compress(raw_data)
    idat_chunk = b'IDAT' + idat
    idat_crc = struct.pack("!I", zlib.crc32(idat_chunk) & 0xFFFFFFFF)

    # IEND
    iend_chunk = b'IEND'
    iend_crc = struct.pack("!I", zlib.crc32(iend_chunk) & 0xFFFFFFFF)

    with open('sky_doodles/textures/sky_doodles_black.png', 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(struct.pack("!I", len(ihdr)) + ihdr_chunk + ihdr_crc)
        f.write(struct.pack("!I", len(idat)) + idat_chunk + idat_crc)
        f.write(struct.pack("!I", 0) + iend_chunk + iend_crc)

create_black_png()
