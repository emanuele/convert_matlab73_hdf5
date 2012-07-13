"""This function transforms Matlab7.3 HDF5 '.mat' files into a Python
dictionary of arrays and strings (and some leftover).

Copyright 2012, Emanuele Olivetti

BSD License, 3 clauses.
"""

import numpy as np
import h5py


def string(seq):
    """Convert a sequence of integers into a single string.
    """
    return ''.join([chr(a) for a in seq])


def recursive_dict(f,root):
    """This function recursively navigates the HDF5 structure from
    node 'f' and tries to unpack the data structure by guessing their
    content from dtype, shape etc.. It returns a dictionary of
    strings, arrays and some leftovers. 'root' is the root node of the
    HDF5 structure, i.e. what h5py.File() returns.

    Note that this function works well on the Matlab7.3 datasets on
    which it was tested, but in general it might be wrong and it might
    crash. The motivation is that it sometimes has to guess the
    content of substructures so it might fail. One source of headache
    seems to be Matlab7.3 format that represents strings as array of
    integers so not using the string datatype.
    """
    if hasattr(f, 'keys'):
        a = dict(f)
        if u'#refs#' in a.keys(): # we don't want to keep this
            del(a[u'#refs#'])
        for k in a.keys():
            # print k
            a[k] = recursive_dict(f[k], root)
        return a
    elif hasattr(f, 'shape'):
        if f.dtype.str in ['<f8', '<u8']: # this is a numpy array
            # Check shape to assess whether it can fit in memory
            # or not. If not recast to a smaller dtype!
            dtype = f.dtype
            if (np.prod(f.shape)*f.dtype.itemsize) > 2e9:
                print "The array takes > 2Gb"
                if f.dtype.char=='d':
                    print "Recasting", dtype, "to float32"
                    dtype = np.float32
                else:
                    raise MemoryError
            return np.array(f, dtype=dtype).squeeze()
        if f.dtype.str in ['<u2']: # this is a string
            try:
                return string(f)
            except ValueError:
                print "\t CONVERSION TO STRING FAILED, USING ARRAY!"
                return np.array(f).squeeze()
            pass
        else: # this is a 2D array of HDF5 object references
            container = []
            for i in range(f.shape[0]):
                for j in range(f.shape[1]):
                    if str(f[i][j])=='<HDF5 object reference>':
                        container.append(recursive_dict(root[f[i][j]], root))
            try:
                return np.array(container).squeeze()
            except ValueError:
                print container
                return np.array(container, dtype=np.object).squeeze()
    return

    
if __name__ == '__main__':

    import sys
    import pickle

    pickling = True
    joblibing = False

    filename = sys.argv[-1]

    print "Loading", filename

    f = h5py.File(filename)

    data = recursive_dict(f, f)

    # If you have enough memory just use pickle:
    if pickling:
        filename = filename[:-4]+".pickle"
        print "Saving", filename
        pickle.dump(data, open(filename,'w'),
                    protocol=pickle.HIGHEST_PROTOCOL)

    # Otherwise use joblib, with no compression which is a
    # streaming dumper. But then you have 1 file for each array...
    if joblibing:
        import joblib
        filename = filename[:-4]+".joblib"
        print "Saving", filename
        print joblib.dump(data, filename, compress=0)
