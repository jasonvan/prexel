import hashlib


"""
TODO - Full develop tests for this

"""


def generate_hashcode(value):
    return hashlib.md5(value.strip().encode('utf-8')).hexdigest()


def save_pretty_printed(hashcode, value, filename):
    with open(filename, "a") as file:
        file.write("{}:{}\n".format(hashcode, value))


def load_easy_entry(hashcode, filename):
    with open(filename) as file:
        for line in file:
            if hashcode in line:
                return line.split(":")[1]
