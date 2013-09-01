""" Graphically plot data stored in a trace file.
    Requires matplotlib.
"""

import pylab
import sys

import core

#--------------------------------------------------------------------
# Constants

USAGE = "usage: python traceplot.py <tracefile> <reader>"


#--------------------------------------------------------------------
# Functions

def main():
    if len(sys.argv) != 3:
        print USAGE
    else:
        traceplot(sys.argv[1], sys.argv[2])


def traceplot(tracefile, reader):
    """ Use the specified reader to extract & plot data
        stored in the given tracefile
    """
    data = _tracefile_to_data_arrays(tracefile, reader)
    plot_options = core.get_plot_options(reader)

    for key in data:
        if plot_options is not None:
            if key in plot_options and 'hide' in plot_options[key]:
                continue
        pylab.plot(range(len(data[key])), data[key], label=key)

    pylab.xlabel('sample')
    pylab.legend()
    pylab.grid()
    pylab.show()


def _tracefile_to_data_arrays(tracefile, reader, include_errors=False):
    """ Return a tracefile's data as arrays of data
        indexed by the data's key
    """
    data_arrays = {}
    data_keys = core.get_data_keys(reader)
    for key in data_keys:
        data_arrays[key] = []

    infile = core.open_tracefile(tracefile, reader)

    for sample in infile:
        if 'data_errors' in sample:
            if not include_errors:
                continue
        for key in data_keys:
            if key in sample:
                data_arrays[key].append(sample[key])
            else:
                data_arrays[key].append(0)

    return data_arrays


# TODO: something like data_process for plot_options
def _process_data_arrays(arrays, reader):
    plot_options = core.get_plot_options(reader)
    pass


if __name__ == '__main__':
    main()
