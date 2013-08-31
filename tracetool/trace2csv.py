import core

import sys
import os

#--------------------------------------------------------------------
# Constants

USAGE = "usage: python trace2csv_new.py <tracefile> <reader>"


#--------------------------------------------------------------------
# Functions

def main():
    if len(sys.argv) != 3:
        print USAGE
    else:
        trace2csv(sys.argv[1], sys.argv[2])


def trace2csv(tracefile, reader):
    out_path = os.path.splitext(tracefile)[0]+'.csv'
    data_keys = core.get_data_keys(reader)
    data_key_order = core.get_data_key_order(reader)

    infile = core.open_tracefile(tracefile, reader)
    outfile = open(out_path, 'w')

    if data_key_order is not None:
        outfile.write(','.join([key for key in data_key_order]) + '\n')
    else:
        outfile.write(','.join([key for key in data_keys]) + '\n')

    for packet in infile:
        out_str = packet2csv_row(packet, num_fields=len(data_keys),
                                 data_key_order=data_key_order)
        outfile.write(out_str)

    outfile.close()


def packet2csv_row(packet, num_fields, data_key_order):
    out_str = ''
    if data_key_order is not None:
        # This is easy, data key order lets us know what's expected
        for key in data_key_order:
            if key in packet:
                out_str += str(packet[key]) + ','
            else:
                out_str += ','
    else:
        # No data key order makes life a bit more difficult
        keys = packet.keys()
        if 'data_errors' in keys:
            keys.remove('data_errors')
        for key in keys:
            out_str += str(packet[key]) + ','
        for i in range(num_fields - len(keys)):
            # Pad csv row to expected number of fields
            out_str += ','

    # Any errors are appended to the end of the row
    if 'data_errors' in packet:
        out_str += packet['data_errors']
    out_str += '\n'

    return out_str


if __name__ == '__main__':
    main()
