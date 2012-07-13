convert_matlab73_hdf5
=====================

Convert Matlab v7.3 '.mat' files (i.e. HDF5 file format) into Python's
pickle/numpy format. This recent Matlab file format is unsupported by
SciPy's scipy.io.loadmat function. See notes here:
http://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html

This script opens the Matlab file in HDF5 format, recursively navigate
the hierarchical structers and follows the pointers till final data,
usually in the form of numbers, arrays and strings. Once a leaf is
reached it heuristically converts the data as Python data types and
put them in a (Python) dictionary following the HDF5 semantic
structure.

This code works well for MEG (magnetoencephalography) files saved from
recent Matlab versions. For examples those you can find some of them
here:
ftp://ftp.fcdonders.nl/pub/biomag2012/


USAGE

python mat73_to_pickle.py <filename.mat>

