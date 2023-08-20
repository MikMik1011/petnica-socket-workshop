HEADER_SIZE_BODY_LEN = 10
HEADER_SIZE_NAME_LEN = 30

def appendHeaders(message, name):
    return bytes(f"{len(message):<{HEADER_SIZE_BODY_LEN}}" + f"{name[:HEADER_SIZE_NAME_LEN].ljust(HEADER_SIZE_NAME_LEN)}" + message, "utf-8")