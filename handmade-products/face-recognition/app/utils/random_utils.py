import random
import time


def random_string(string_len=10):
    characters = [i for i in 'qwertyuiopasdfghjklzxcvbnm1234567890']
    random_characters = random.sample(characters, string_len)

    return ''.join(random_characters)


def random_string_with_datetime(string_len=10):
    string = random_string(string_len)
    milliseconds = str(int(time.time() * 1000))

    return f"{string}-{milliseconds}"
