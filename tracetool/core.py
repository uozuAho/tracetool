import imp


def main():
    pass


def open_tracefile(tracefile, reader):
    return _get_packet_generator(tracefile, reader)


def get_data_keys(reader):
    """ Get the expected data fields from the reader """
    reader = imp.load_source('', reader)
    return reader.parse(bytearray(reader.TEST_PACKET)).keys()


def get_data_key_order(reader):
    """ Return the order that data keys should be presented
        (list), if specified by the reader. Otherwise
        return None.
    """
    reader = imp.load_source('', reader)
    try:
        return reader.DATA_KEY_ORDER
    except AttributeError:
        return None


def _get_packet_generator(tracefile, reader_file):
    reader = imp.load_source('', reader_file)
    for packet in reader.packetise(tracefile):
        yield reader.parse(packet)


if __name__ == '__main__':
    main()
