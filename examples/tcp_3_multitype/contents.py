import msgpack

HEADER_LEN = 10

def pack(content, type, name, animal=None):
    content = msgpack.packb({"content": content, "type": type, "name": name, "animal": animal}, use_bin_type=True)
    return len(content).to_bytes(HEADER_LEN) + content

def unpack(content):
    return msgpack.unpackb(content, raw=False)