"""
Password generation functions
"""

import random
import string

# CONSTANTS ===================================================================

EXCLUDE_CHARS = ["\\", "/", "'", '"']
LOWER_CHARS = [char for char in string.ascii_lowercase]
UPPER_CHARS = [char for char in string.ascii_uppercase]
INTEGER_CHARS = ["%s" % i for i in range(10)]
SPECIAL_CHARS = [char for char in string.punctuation
                 if char not in EXCLUDE_CHARS]


# API =========================================================================

def generate(min_chars=6, max_chars=64, integers=1, specials=1, uppers=1):
    """
    Generate a random password based on given parameters.

    :param min_chars: minimum pw length (default 6)
    :param max_chars: maximum pw length (default 64)
    :param integers: number of integer chars (default 1)
    :param specials: number of special chars (default 1)
    :param uppers: number of uppercase chars (default 1)
    :type min_chars: integer
    :type max_chars: integer
    :type integers: integer
    :type specials: integer
    :type uppers: integer
    :return: generated password
    :rtype: string
    """

    assert min_chars <= max_chars, "max_chars must be larger than min_chars"
    constraint_length = integers + specials + uppers
    fill = fill_length(min_chars, max_chars, constraint_length)
    char_bag = \
        char_fetch(INTEGER_CHARS, integers) \
        + char_fetch(SPECIAL_CHARS, specials) \
        + char_fetch(UPPER_CHARS, uppers) \
        + char_fetch(LOWER_CHARS, fill)

    random.shuffle(char_bag)
    return string.join(char_bag, "")


# HELPERS =====================================================================

def fill_length(min_chars, max_chars, req_chars):
    min_fill = 0
    if req_chars < min_chars:
        min_fill = min_chars - req_chars
    else:
        min_chars = req_chars

    final_length = random.randint(
        min_chars,
        max_chars
    )
    delta_fill = final_length - min_chars
    return min_fill + delta_fill


def char_fetch(chars, num):
    """
    Return `num` items at random from `chars`
    """
    return [random.choice(chars) for i in range(num)]
