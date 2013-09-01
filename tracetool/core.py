""" Core functions of tracetool. Name may change, couldn't
    think of a better one sorry
"""

import imp


def main():
    pass


def open_tracefile(tracefile, reader):
    """ Return a packet generator from the given tracefile
        and tracefile reader paths
    """
    return _get_packet_generator(tracefile, reader)


def _get_packet_generator(tracefile, reader_file):
    """ Use the specified reader to return a packet
        generator that extacts packets from the
        given tracefile
    """
    reader = imp.load_source('', reader_file)
    for packet in reader.packetise(tracefile):
        yield reader.parse(packet)


def get_data_keys(reader):
    """ Get the expected trace data fields from the reader """
    reader = imp.load_source('', reader)
    return reader.parse(bytearray(reader.TEST_PACKET)).keys()


def get_data_key_order(reader):
    """ Return the order that data fields should be presented
        (list), if specified by the reader. Otherwise
        return None.
    """
    reader = imp.load_source('', reader)
    try:
        return reader.DATA_KEY_ORDER
    except AttributeError:
        return None


def get_plot_options(reader):
    """ Get any plotting options from the reader """
    reader = imp.load_source('', reader)
    try:
        return reader.DATA_PLOT_OPTIONS
    except AttributeError:
        return None


if __name__ == '__main__':
    main()
