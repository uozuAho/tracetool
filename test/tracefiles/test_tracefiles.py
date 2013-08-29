""" Specifies the test tracefile data format """


def get_checksum_sum(packet):
    """ Calculate the 'sum' checksum of the packet """
    return sum(packet[:6])


def get_checksum_xor(packet):
    """ Calculate the 'xor' checksum of the packet """
    ret = 0
    for byte in packet[:6]:
        ret ^= byte
    return ret


# Format is a tuple of tuples, each specifying
# a data name and type of data in the form:
# ('name', 'xN')
#
# where x is one of:
# u: unsigned
# s: signed
# f: floating-point
#
# and N is the number of bits
#
# an inner tuple can also contain 3 items, the
# third item being a function to calculate the
# expected value of the data in this field. This
# allows custom checksum calculations.
format = (
    ('idx', 's8'),
    ('volts', 's8'),
    ('amps', 's8'),
    ('duty', 'u16'),
    ('errors', 'u8'),
    ('checksum_sum', 'u8', get_checksum_sum),
    ('checksum_xor', 'u8', get_checksum_xor)
    # Newline (implicit)
)
