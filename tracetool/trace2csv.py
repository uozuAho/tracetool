""" Parse binary logging output from output control
    data logging

    TODO: put this in ss c lib, it's useful as a filter
    for fast logging, such as diagnostics
"""

import sys
import os

#--------------------------------------------------------------------
# Constants

USAGE = "usage: python log2csv.py <log file>"

LOG_PACKET_LENGTH = 9


#--------------------------------------------------------------------
# Data

class GlobalData:
    total_lines = 0
    discarded_lines = 0


#--------------------------------------------------------------------
# Functions

def main():
    infile = get_logfile_path_from_console()
    if infile is None:
        print "invalid logfile path"
    else:
        log2csv(infile, include_invalid_packets=True)

    print "Done."
    print "Total lines    :", GlobalData.total_lines
    print "Discarded lines:", GlobalData.discarded_lines


def get_logfile_path_from_console():
    if len(sys.argv) != 2:
        print USAGE
    else:
        if os.path.isfile(sys.argv[1]):
            return sys.argv[1]
    return None


def log2csv(logfile_path, include_invalid_packets=False):
    out_path = os.path.splitext(logfile_path)[0]+'.csv'

    infile = open(logfile_path, 'rb')
    outfile = open(out_path, 'w')

    column_headings = get_column_headings()
    if include_invalid_packets:
        column_headings.append('data_errors')
    outfile.write(','.join([heading for heading in column_headings]))
    outfile.write('\n')

    for line in infile:
        GlobalData.total_lines += 1
        data = parse_log_packet(line)
        if not include_invalid_packets and 'data_errors' in data:
            GlobalData.discarded_lines += 1
        else:
            out_str = ''
            for column in column_headings:
                if column in data:
                    out_str += str(data[column]) + ','
                else:
                    out_str += ','
            out_str += '\n'
            outfile.write(out_str)

    infile.close()
    outfile.close()


def get_column_headings():
    """ Return the csv data column heading strings. These should
        match the data dict keys
    """
    return [
        'idx',
        'volts',
        'amps',
        'duty',
        'errors',
        'checksum_sum',
        'checksum_xor'
    ]


def parse_log_packet(packet):
    """ Return a dict of data from the given binary packet.
        Invalid data will have a field 'data_errors', which
        contains a list of errors
    """
    data = {}
    binary_packet = bytearray(packet)

    if is_packet_length_correct(binary_packet):
        data.update(get_packet_data(binary_packet))
        if not is_checksum_correct(binary_packet):
            expected_sum, expected_xor = calculate_checksum(binary_packet)
            expected_str = str(expected_sum)+' '+str(expected_xor)
            append_data_error(data, 'invalid checksum. Expected '+expected_str)
    else:
        append_data_error(data, 'incorrect packet length: '+str(len(binary_packet)))

    return data


def append_data_error(data, error):
    if 'data_errors' not in data:
        data['data_errors'] = error
    else:
        data['data_errors'].append(error)


def is_valid_packet(packet):
    is_valid = False
    if is_packet_length_correct(packet):
        if is_checksum_correct(packet):
            is_valid = True
    return is_valid


def is_packet_length_correct(packet):
    if len(packet) != LOG_PACKET_LENGTH:
        return False
    return True


def is_checksum_correct(packet):
    checksum_sum, checksum_xor = calculate_checksum(packet)
    if checksum_sum != packet[6]:
        return False
    if checksum_xor != packet[7]:
        return False
    return True


def calculate_checksum(packet):
    checksum_sum = 0
    checksum_xor = 0
    for byte in packet[:6]:
        checksum_sum += byte
        checksum_sum = checksum_sum % 256
        checksum_xor ^= byte

    return checksum_sum, checksum_xor


def get_packet_data(packet):
    """ Extract data from a valid packet, return as a dict """
    data = {
        'idx': int(packet[0]),
        'volts': int(packet[1]),
        'amps': int(packet[2]),
        'duty': int(packet[3]*256 + packet[4]),
        'errors': int(packet[5]),
        'checksum_sum': int(packet[6]),
        'checksum_xor': int(packet[7])
    }

    return data


def print_log_to_console(logfile):
    with open(logfile) as infile:
        for line in infile:
            print line


if __name__ == '__main__':
    main()
