import msgpack

HEADER_SIZE_BODY_LEN = 10

def pack(content, type, name):
    content = msgpack.packb({"content": content, "type": type, "name": name}, use_bin_type=True)
    return f"{len(content):<{HEADER_SIZE_BODY_LEN}}".encode() + content

def unpack(content):
    return msgpack.unpackb(content, raw=False)