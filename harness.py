#!/usr/bin/env python3

from struct import unpack_from

from XeCrypt import *

# RSA
rsa_test_hash = bytes.fromhex("7A71F234F5EBF720C84A13A3C586478DCDE402B8")
rsa_test_salt = b"XBOX_HAXXS"

# RC4 ECB
rc4_1_round = bytes.fromhex("74285FBF1D46410B22435798B996F947")
rc4_100_round = bytes.fromhex("0B5D42406B73070ACB785F8CFE58C130")

# AES ECB
aes_ecb_1_round = bytes.fromhex("59AF4143F1C4722C6EA0FA3FF80EAA9B")
aes_ecb_100_round = bytes.fromhex("A1AD9CE67C736D10668ABCA1B12CDB30")

# AES CBC
aes_cbc_1_round = bytes.fromhex("E4F23DBF19C99213E08EBE0067DF23F1")
aes_cbc_1_round_feed = bytes.fromhex("44D49CC606E7146A7571D15537D46D55")
aes_cbc_100_round = bytes.fromhex("977DCE8A2DF1E38702B475BCB29B5337")
aes_cbc_100_round_feed = bytes.fromhex("6C88B3349984F7A0D959FCBA864AFAEC")

# DES CBC
des_1_round = bytes.fromhex("EECA54C48ED8256F")
des_100_round = bytes.fromhex("09FA9615CBEC1128")
des_cbc_round = bytes.fromhex("4C26B20B7BE8F24031A54D933133793FC82CADA9DFD98D6A337338C377DC695564A41B0C61B545F523A14A6E8831BFC4E5A72B65F8DF522362E42DE80399BA6D")

# DES3 CBC
des3_1_round = bytes.fromhex("5EF685A69F187826")
des3_100_round = bytes.fromhex("DAD66BC1E20B2489")
des3_cbc_round = bytes.fromhex("B5AF523195020615337338C377DC695564A41B0C61B545F523A14A6E8831BFC4E5A72B65F8DF522362E42DE80399BA6DA4609C63F30D4B3B9445B7DBAC5BDDAB")

# MD5
md5_digest = bytes.fromhex("DE0137D93167B099A9C766D57C45E8DB")

# SHA-1
sha_digest = bytes.fromhex("7A71F234F5EBF720C84A13A3C586478DCDE402B8")
rotsumsha_digest = bytes.fromhex("C551302CE570CACA246D060E3478C52D8F5A8A45")
hmac_1_digest = bytes.fromhex("CEC5F44ADE23C6F21A42C43171D76407A3A30E1D")
hmac_2_digest = bytes.fromhex("7EC867712FB02FBE1792C8F019B01D5025698357")

# RotSum
rotsum_digest = bytes.fromhex("0000000000000001F83FB03F944C2298FFFFFFFFFFFFFFFEBFF676A5849C071F")

# CPU keys
valid_cpu_key = bytes.fromhex("0F17D09D89EA12B1716E5D134F8266FF")
invalid_cpu_key = bytes.fromhex("12345678901234567890123456789010")

def sig_create_verify_test(prv_key: (bytes, bytearray)) -> bool:
	sig = XeCryptBnQwBeSigCreate(rsa_test_hash, rsa_test_salt, prv_key)
	print("        RSA signature created OK")
	sig = XeCryptBnQwNeRsaPrvCrypt(sig, prv_key)
	print("        RSA signature encrypted OK")
	if XeCryptBnQwBeSigVerify(sig, rsa_test_hash, rsa_test_salt, prv_key[:XECRYPT_RSAPUB_2048_SIZE]):
		print("        RSA signature verified OK")
		return True
	else:
		print("        RSA signature verify FAILED")
	return False

def do_rsa_test() -> bool:
	rsa_pass = True
	rsa_test_key = read_file("Data/rsa_test_key.bin")

	print("starting RSA tests...")
	print("    testing RSA signature creation and verification with static key....")
	if sig_create_verify_test(rsa_test_key):
		print("    RSA test OK")
	else:
		print("    RSA test FAILED")
		rsa_pass = False

	print("    testing PKCS1 signature creation and verification with static key....")

	sig_buf = XeKeysPkcs1Create(rsa_test_hash, rsa_test_key)
	print("        PKCS1 signature created OK")
	if XeKeysPkcs1Verify(sig_buf, rsa_test_hash, rsa_test_key[:XECRYPT_RSAPUB_2048_SIZE]):
		print("        PKCS1 signature verified OK")
	else:
		print("        PKCS1 signature verify FAILED")
		rsa_pass = False

	return rsa_pass

def do_rc4_test() -> bool:
	rc4_pass = True

	(rc4_key, rc4_data) = unpack_from(f"<{0x10}s {0x10}s", test_data, 0)

	print("starting RC4 tests...")
	XeCryptRc4EcbKey(rc4_key)
	rc4_data = XeCryptRc4(rc4_data)
	print("    RC4 first round - ")
	if rc4_data == rc4_1_round:
		print("OK")
	else:
		print("FAILED")
		rc4_pass = False

	for cnt in range(99):
		rc4_data = XeCryptRc4(rc4_data)
	print("    RC4 hundred round - ")
	if rc4_data == rc4_100_round:
		print("OK")
	else:
		print("FAILED")
		rc4_pass = False

	print("RC4 %s" % ("OK" if rc4_pass else "FAILED!"))

	return rc4_pass

def do_aes_test() -> bool:
	aes_pass = True

	(aes_key, aes_data) = unpack_from(f"<{XECRYPT_AES_KEY_SIZE}s {XECRYPT_AES_BLOCK_SIZE}s", test_data, 0)

	print("starting AES tests...")
	aes_data = XeCryptAesEcb(aes_key, aes_data, False)
	print("    AES-ECB first round - ")
	if aes_data == aes_ecb_1_round:
		print("OK")
	else:
		print("FAILED")
		aes_pass = False

	for cnt in range(99):
		aes_data = XeCryptAesEcb(aes_key, aes_data, False)
	print("    AES-ECB hundred round - ")
	if aes_data == aes_ecb_100_round:
		print("OK")
	else:
		print("FAILED")
		aes_pass = False

	(aes_key, aes_data, aes_feed) = unpack_from(f"<{XECRYPT_AES_KEY_SIZE}s {XECRYPT_AES_BLOCK_SIZE}s {XECRYPT_AES_FEED_SIZE}s", test_data, 0)

	XeCryptAesCbcKey(aes_key, aes_feed)
	aes_data = XeCryptAes(aes_data, False)
	print("    AES-CBC first round - ")
	if aes_data == aes_cbc_1_round:
		print("OK")
	else:
		print("FAILED")
		aes_pass = False

	XeCryptAesCbcKey(aes_key, aes_cbc_1_round_feed)
	for cnt in range(99):
		aes_data = XeCryptAes(aes_data, False)
	print("    AES-CBC hundred round - ")
	if aes_data == aes_cbc_100_round:
		print("OK")
	else:
		print("FAILED")
		aes_pass = False

	print("AES %s" % ("OK" if aes_pass else "FAILED!"))

	return aes_pass

def do_des_test() -> bool:
	des_pass = True

	(des_key, des_data) = unpack_from(f"<{XECRYPT_DES_KEY_SIZE}s {XECRYPT_DES_BLOCK_SIZE}s", test_data, 0)
	print("starting DES tests...")
	des_data = XeCryptDesEcb(des_key, des_data, False)
	print("    DES-ECB first round - ")
	if des_data == des_1_round:
		print("OK")
	else:
		print("FAILED")
		des_pass = False

	for cnt in range(99):
		des_data = XeCryptDesEcb(des_key, des_data, False)
	print("    DES-ECB hundred round - ")
	if des_data == des_100_round:
		print("OK")
	else:
		print("FAILED")
		des_pass = False

	(des_key, des_feed, des_data) = unpack_from(f"<{XECRYPT_DES_KEY_SIZE}s {XECRYPT_DES_BLOCK_SIZE}s {XECRYPT_DES_BLOCK_SIZE * 8}s", test_data, 0)

	des_data = XeCryptDesCbc(des_key, des_feed, des_data, False)
	# print("    DES-CBC - ")
	# if des_data == des_cbc_round:
	#     print("OK")
	# else:
	#     print("FAILED")
	#     des_pass = False

	(des_key, des_data) = unpack_from(f"<{XECRYPT_DES3_KEY_SIZE}s {XECRYPT_DES3_BLOCK_SIZE}s", test_data, 0)

	des_data = XeCryptDes3Ecb(des_key, des_data, False)
	print("    DES3-ECB first round - ")
	if des_data == des3_1_round:
		print("OK")
	else:
		print("FAILED")
		des_pass = False

	for cnt in range(99):
		des_data = XeCryptDes3Ecb(des_key, des_data, False)
	print("    DES3-ECB hundred round - ")
	if des_data == des3_100_round:
		print("OK")
	else:
		print("FAILED")
		des_pass = False

	#des_key = unpack_from("<%ss" % (XECRYPT_DES3_KEY_SIZE), test_data, 0)[0]
	#des_feed = unpack_from("<%ss" % (XECRYPT_DES3_BLOCK_SIZE), test_data, XECRYPT_DES3_BLOCK_SIZE)[0]
	#des_data = unpack_from("<%ss" % (XECRYPT_DES3_BLOCK_SIZE * 8), test_data, XECRYPT_DES3_KEY_SIZE + XECRYPT_DES3_BLOCK_SIZE)[0]

	#des_data = XeCryptDes3Cbc(des_key, des_data, des_feed, False)
	#print("    DES3-CBC - ")
	#if des_data == des3_cbc_round:
	#    print("OK")
	#else:
	#    print("FAILED")
	#    des_pass = False

	print("DES %s" % ("OK" if des_pass else "FAILED!"))

	return des_pass

def do_md5_test() -> bool:
	md5_pass = True

	print("starting MD5 tests...")

	md5_val = XeCryptMd5(test_data)
	print("    MD5 first round - ")
	if md5_val == md5_digest:
		print("OK")
	else:
		print("FAILED")
		md5_pass = False

	print("MD5 %s" % ("OK" if md5_pass else "FAILED!"))

	return md5_pass

def do_sha_test() -> bool:
	sha_pass = True

	print("starting SHA tests...")

	sha_val = XeCryptSha(test_data)
	print("    SHA first round - ")
	if sha_val == sha_digest:
		print("OK")
	else:
		print("FAILED")
		sha_pass = False

	sha_val = XeCryptRotSumSha(test_data)
	print("    SHA second round (ROTSUMSHA) - ")
	if sha_val == rotsumsha_digest:
		print("OK")
	else:
		print("FAILED")
		sha_pass = False

	sha_val = XeCryptHmacSha(test_data[:0x10], test_data[0x10:])
	print("    SHA third round (HMAC) - ")
	if sha_val == hmac_1_digest:
		print("OK")
	else:
		print("FAILED")
		sha_pass = False

	sha_val = XeCryptHmacSha(test_data[:0x40], *unpack_from(f"<{0x20000}s {0x20000}s {6}s", test_data, 0))
	print("    SHA fourth round (HMAC) - ")
	if sha_val == hmac_2_digest:
		print("OK")
	else:
		print("FAILED")
		sha_pass = False

	print("SHA %s" % ("OK" if sha_pass else "FAILED!"))

	return sha_pass

def do_misc_test() -> bool:
	misc_pass = True

	print("starting Miscellaneous tests...")

	print("    testing RotSum")

	if XeCryptRotSum(test_data[:0x20]) == rotsum_digest:
		print("OK")
	else:
		print("FAILED")
		misc_pass = False

	print("    testing valid CPU key")
	if XeCryptCpuKeyValid(valid_cpu_key):
		print("OK")
	else:
		print("FAILED")
		misc_pass = False

	print("    testing invalid CPU key")
	if not XeCryptCpuKeyValid(invalid_cpu_key):
		print("OK")
	else:
		print("FAILED")
		misc_pass = False

	print("    testing CPU key generation")
	if all([XeCryptCpuKeyValid(XeCryptCpuKeyGen()) for i in range(20)]):
		print("OK")
	else:
		print("FAILED")
		misc_pass = False

	print("Miscellaneous %s" % ("OK" if misc_pass else "FAILED!"))

	return misc_pass

if __name__ == "__main__":
	test_pass = True

	# test data
	test_data = read_file("Data/test_data.bin")

	# RSA tests
	if not do_rsa_test():
		test_pass = False
	print()

	# RC4 tests
	if not do_rc4_test():
		test_pass = False
	print()

	# AES tests
	if not do_aes_test():
		test_pass = False
	print()

	# DES tests
	if not do_des_test():
		test_pass = False
	print()

	# MD5 tests
	if not do_md5_test():
		test_pass = False
	print()

	# SHA-1, RotSumSha, and HMAC-SHA-1 tests
	if not do_sha_test():
		test_pass = False
	print()

	# misc. tests
	if not do_misc_test():
		test_pass = False
	print()

	# results
	if test_pass:
		print("SUCCESS! All tests passed!")
	else:
		print("ERROR! One or more tests failed!")