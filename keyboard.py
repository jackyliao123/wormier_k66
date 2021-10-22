import hid
from typing import List

class Wormier_K66():
    chunksize = 64
    vend_id = 0x0c45
    prod_id = 0x7698
    usage_page = 0xff1c
    color_mode_names = {
        0x01: "Go with the stream",
        0x02: "Clouds fly",
        0x03: "Winding paths",
        0x04: "The trial of light",
        0x05: "Breathing",
        0x06: "Normally on",
        0x07: "Pass without trace",
        0x08: "Ripple graff",
        0x09: "Fast run without trace",
        0x0a: "Snow winter jasmine",
        0x0b: "Flowers blooming",
        0x0c: "Swift action",
        0x0d: "Hurricane",
        0x0e: "Accumulate",
        0x0f: "Digital Times",
        0x10: "Both ways",
        0x11: "Surmount",
        0x12: "Fast and the Furious",
        0x14: "Coastal",
        0x15: "Off"
    }

    class Transaction:
        def __init__(self, parent):
            self.parent = parent

        def __enter__(self):
            self.parent.begin_transaction()

        def __exit__(self, type, value, traceback):
            self.parent.end_transaction()

    def open(self):
        device_info = None

        for device_dict in hid.enumerate():
            if device_dict["vendor_id"] == Wormier_K66.vend_id and device_dict["product_id"] == Wormier_K66.prod_id and device_dict["usage_page"] == Wormier_K66.usage_page:
                device_info = device_dict

        if device_info is None:
            raise Exception("Device not found")

        self.device = hid.device()
        self.device.open_path(device_info["path"]);

    def close(self):
        self.device.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def send(self, payload: bytes):
        checksum = 0
        for i in payload:
            checksum += i

        total_len = len(payload) + 3

        if total_len > Wormier_K66.chunksize:
            raise ValueError("Payload too large")

        # 04 [checksum] bytes [padding]
        bs = b"\x04" + checksum.to_bytes(2, "little") + payload + (Wormier_K66.chunksize - total_len) * b"\x00"

        # The data seems to always be sent back, so read 64 bytes to consume it
        self.device.write(bs)
        self.device.read(64)

    def begin_transaction(self):
        self.send(b"\x01")

    def end_transaction(self):
        self.send(b"\x02")

    def transaction(self):
        return self.Transaction(self)

    def raw_setting(self, setting_id: int, data: bytes):
        self.send(bytes([0x06, len(data), setting_id, 0x00, 0x00]) + data)

    def raw_key_rgb(self, key_offset: int, colors: List[int]):
        offset = key_offset * 3
        ba = bytearray([0x11, len(colors) * 3])
        ba += offset.to_bytes(2, "little")
        ba += b"\x00"
        for color in colors:
            ba += color.to_bytes(3, "big")
        self.send(ba)

    def set_mode(self, mode: int):
        assert 1 <= mode <= 0x21
        self.raw_setting(0, bytes([mode]))

    def set_brightness(self, brightness: int):
        assert 0 <= brightness <= 3
        self.raw_setting(1, bytes([brightness]))

    def set_speed(self, speed: int):
        assert 0 <= speed <= 3
        self.raw_setting(2, bytes([speed]))

    def set_direction(self, direction: bool):
        self.raw_setting(3, bytes([0x01 if direction else 0xff]))

    def set_colorful(self, colorful: bool):
        self.raw_setting(4, bytes([int(colorful)]))

    def set_color(self, rgb: int):
        assert 0 <= rgb <= 0xffffff
        self.raw_setting(5, rgb.to_bytes(3, "big"))

    def set_polling_rate(self, rate: int):
        assert 0 <= rate <= 3
        self.raw_setting(15, bytes([rate]))

    def set_gradient(self, gradient: int):
        assert 0 <= gradient <= 3
        self.raw_setting(17, bytes([gradient]))

