#!/usr/bin/env python3

# This file takes a list of newline-separated KB/MB/GB/etc values
# and will sum them in KB.

#

import sys
import unittest

conversions = {
    'k': 1E3,  # kilo
    'm': 1E6,  # mega
    'g': 1E9,  # giga
    't': 1E12,  # tera
    'p': 1E15,  # peta
}


def normalize_si_bytes_number(num: str) -> float:
    num = num.lower().replace('b', '').strip()

    # Base number w/o SI unit
    numeric_base: float = None
    si_number: float = None

    # print("Line: " + num)

    # If the end of the line ends with an SI suffix,
    if num[-1] in list(conversions.keys()):
        # print("Wow! This line has " + num[-1] + " as a suffix!")

        number, suffix = float(num[:-1]), num[-1]

        # print(suffix,number)

        return conversions[suffix] * number

    # If the line is not k,m,g,t,etc, or digits,
    elif num[-1] not in '0123456789.':
        print("Unknown suffix '{}'".format(num[-1]))
        exit(1)
    else:
        # print("No suffix. Number is {}.".format(si_number))
        return float(num)


tc = unittest.TestCase()
tc.assertEqual(normalize_si_bytes_number('100.01'), 100.01)
tc.assertEqual(normalize_si_bytes_number('1.01k'), (1.01 * 1E3))
tc.assertEqual(normalize_si_bytes_number('12MB'), (12.0 * 1E6))

if __name__ == '__main__':

    total = 0

    for line in sys.stdin:
        total += (normalize_si_bytes_number(line))

    print(total)

# Lowercase, remove 'b', remove whitespace.
