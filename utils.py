import hashlib


def generate_hashcode(value):
    return hashlib.md5(value.encode()).hexdigest()