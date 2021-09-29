import binascii
import random
import string
import time

text = "test"
dict = {}

def random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def problem3():
    print("Started")
    start = time.time()
    while True:
        random_str = random_string(random.randint(10, 1000))
        crc_result = binascii.crc32(random_str.encode('utf-8'))
        if dict.get(crc_result) is None:
            dict[crc_result] = random_str
        else:
            end = time.time()
            print("COLLISION FOUND! Time taken: ", end - start)
            print("X: ")
            print(random_str)
            print("Y:")
            print(dict.get(crc_result))
            print("CRC: ", crc_result)
            break

problem3()
