""" Specifies the test tracefile data format """

# Valid packets are of length 9
PACKET_LENGTH = 9

# Must include a valid test packet
TEST_PACKET = '\x01\x07\x08\x00\x05\x00\x15\x0B\n'

# Optional: specify order that data is presented
DATA_KEY_ORDER = [
    'idx',
    'volts',
    'amps',
    'duty',
    'errors',
    'checksum_sum',
    'checksum_xor'
]


def packetise(path):
    """ Generate packets from the given binary file """
    with open(path, 'rb') as infile:
        for line in infile:
            yield bytearray(line)


def parse(packet):
    """ Parse a packet extracted by packetise().
        Return a dictionary of data extracted from the
        packet.
    """
    data = {}
    if len(packet) != PACKET_LENGTH:
        _append_data_error(data, 'bad pkt len: '+str(len(packet)))
    else:
        data = {
            'idx': packet[0],
            'volts': packet[1],
            'amps': packet[2],
            'duty': packet[3]*256 + packet[4],
            'errors': packet[5],
            'checksum_sum': packet[6],
            'checksum_xor': packet[7]
        }
        if not _is_checksum_correct(packet):
            _append_data_error(data, 'checksum bad. expected ' +
                               str(_get_checksum_sum(packet)) + ', ' +
                               str(_get_checksum_xor(packet)))
    return data


def _get_checksum_sum(packet):
    """ Calculate the 'sum' checksum of the packet """
    return sum(packet[:6]) % 256


def _get_checksum_xor(packet):
    """ Calculate the 'xor' checksum of the packet """
    ret = 0
    for byte in packet[:6]:
        ret ^= byte
    return ret


def _append_data_error(data, error):
    if 'data_errors' not in data:
        data['data_errors'] = error
    else:
        data['data_errors'].append(error)


def _is_checksum_correct(packet):
    if _get_checksum_sum(packet) != packet[6]:
        return False
    if _get_checksum_xor(packet) != packet[7]:
        return False
    return True


if __name__ == '__main__':
    print parse(bytearray(TEST_PACKET))
