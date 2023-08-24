HEADER_LEN = 4
NAME_LEN = 32

def appendHeaders(message):
    return len(message).to_bytes(HEADER_LEN) + message.encode()