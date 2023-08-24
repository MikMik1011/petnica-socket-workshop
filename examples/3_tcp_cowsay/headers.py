HEADER_LEN = 4
NAME_LEN = 32

def appendHeaders(message, name):
    return len(message).to_bytes(HEADER_LEN) + bytes(f"{name[:NAME_LEN].ljust(NAME_LEN)}" + message, "utf-8")