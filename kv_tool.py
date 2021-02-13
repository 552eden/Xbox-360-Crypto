#!/usr/bin/env python3

from enum import IntEnum
from pathlib import Path
from struct import pack_into

from XeCrypt import XeCryptKeyVaultEncrypt

class ConsoleType(IntEnum):
	RETAIL_PHAT = 0
	RETAIL_SLIM = 1
	TEST_KIT    = 2
	DEVKIT      = 3

def main() -> None:
	cpu_key = bytes.fromhex("A55F6604990DD4736DE6A0E09FC576F1")
	dvd_key = bytes.fromhex("C7F720142AB22847757398FEB4AECDD1")
	console_type = ConsoleType.DEVKIT

	print("CPU key: " + cpu_key.hex().upper())
	print("DVD key: " + dvd_key.hex().upper())

	fuse_lines = [
		"C0FFFFFFFFFFFFFF",
		"0000000000000000",  # line #2 - console type
		"0000000000000000",
		"0000000000000000",  # line #4 - CPU #1
		"0000000000000000",  # line #5 - CPU #2
		"0000000000000000",  # line #6 - CPU #3
		"0000000000000000",  # line #7 - CPU #4
		"F000000000000000",
		"0000000000000000",
		"0000000000000000",
		"0000000000000000",
		"0000000000000000"
	]
	fuse_data = bytearray(b"".join([bytes.fromhex(x) for x in fuse_lines]))

	kv_path = Path("KV/banned.bin")
	kv_data = bytearray(kv_path.read_bytes())

	fuse_path = Path("Output/Zero/fuses.bin")

	pack_into("16s", kv_data, 0x100, dvd_key)
	kv_data = XeCryptKeyVaultEncrypt(cpu_key, kv_data)

	# update console type
	pack_into("6s", fuse_data, 8, bytes.fromhex("0F0F0F0F0F0F"))
	if console_type == ConsoleType.TEST_KIT:
		pack_into("2s", fuse_data, 0xE, b"\xF0\x0F")
	elif console_type == ConsoleType.DEVKIT:
		pack_into("2s", fuse_data, 0xE, b"\x0F\x0F")
	elif console_type == ConsoleType.RETAIL_PHAT:
		pack_into("2s", fuse_data, 0xE, b"\x0F\xF0")
	elif console_type == ConsoleType.RETAIL_SLIM:
		pack_into("2s", fuse_data, 0xE, b"\xF0\xF0")

	# update CPU key in fuses
	pack_into("8s8s8s8s", fuse_data, 0x18, cpu_key[:8], cpu_key[:8], cpu_key[8:16], cpu_key[8:16])

	fuse_path.write_bytes(fuse_data)
	kv_path = Path("Output/Zero/kv_enc.bin")
	kv_path.write_bytes(kv_data)

	print()
	print("Fuses:")
	for i in range(12):
		print(fuse_data[i * 8:(i * 8) + 8].hex().upper())

	print()
	print(f"KV written to \"{str(kv_path.absolute())}\"!")
	print(f"Fuses written to \"{str(fuse_path.absolute())}\"!")

if __name__ == "__main__":
	main()