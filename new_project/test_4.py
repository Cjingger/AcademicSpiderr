# !/usr/bin/python3
# -*- coding:utf-8 -*-

res = (255) & (1 ^ 228)
print(bin(255))
print(bin(1 ^ 228))
print(bin(255 ^ 228))
print(bin(2433887204))
print(res)
print(bin(1))

#补码
def to_binary(num, bits=8):
    binary = bin(num & int("1"*bits, 2))[2:]
    return binary.zfill(bits)

#反码
def to_complement_code(binary):
    complement_code = ''
    for bit in binary:
        if bit == '0':
            complement_code += '1'
        else:
            complement_code += '0'
    return complement_code

def to_twos_complement(binary):
    complement_code = to_complement_code(binary)
    twos_complement = bin(int(complement_code, 2) + 1)[2:]
    return twos_complement.zfill(len(binary))


if __name__ == '__main__':
    # 补码
    num = 228
    binary = to_binary(num)
    print(f"{num} 的补码是: {binary}")
    # 反码
    complement_code = to_complement_code(binary)
    print(f"{num} 的反码是: {complement_code}")
    print(int("11100100", 2))
    print(255 & 2433887204)