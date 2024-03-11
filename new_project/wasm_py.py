# !/usr/bin/python3
# -*- coding:utf-8 -*-
import wasm3, base64

WASM = base64.b64decode("AGFzbQEAAAABBgFgAX4"
    "BfgMCAQAHBwEDZmliAAAKHwEdACAAQgJUBEAgAA"
    "8LIABCAn0QACAAQgF9EAB8Dws=")

env = wasm3.Environment()
rt = env.new_runtime(1024)
mod = env.parse_module(WASM)
rt.load(mod)
wasm_fib = rt.find_function("fib")
result = wasm_fib(48)
print(result) 