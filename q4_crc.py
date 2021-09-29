import binascii
import random
import string
import time

def random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def problem4_randomstring(student_num_md5_hash):
    student_num_hash_crc = binascii.crc32(student_num_md5_hash.encode('utf-8'))
    print("Started")
    start = time.time()
    while True:
        random_str = random_string(random.randint(10, 1000))
        crc_result = binascii.crc32(random_str.encode('utf-8'))
        if crc_result == student_num_hash_crc:
            end = time.time()
            print("COLLISION FOUND! Time taken: ", end - start)
            print("Random String: ", random_str)
            print("Student Num Hash:", student_num_md5_hash)
            print("CRC: ", crc_result)
            break

def problem4_integer_iter(student_num_md5_hash):
    student_num_hash_crc = binascii.crc32(student_num_md5_hash.encode('utf-8'))
    print("Started")
    start = time.time()
    for i in range(1073741824*3, 2**32):
        print(i, end="\r")
        crc_result = binascii.crc32(i.to_bytes(4, byteorder='big'))
        if crc_result == student_num_hash_crc:
            end = time.time()
            print("COLLISION FOUND! Time taken: ", end - start)
            print("Random String: ", i)
            print("Student Num Hash:", student_num_md5_hash)
            print("CRC: ", crc_result)
            break



student_num_md5_hash = "7684EF63F4BF2D2C3AF37D7F7B61CCB8"
# problem4_randomstring(student_num_md5_hash)
# problem4_integer_iter(student_num_md5_hash)

print(binascii.crc32("㛭".encode('utf-8')))
print(binascii.crc32(student_num_md5_hash.encode('utf-8')))