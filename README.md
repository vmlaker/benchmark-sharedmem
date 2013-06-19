Performance benchmark of NumPy shared memory.

First install numpy-sharedmem:

    hg clone http://bitbucket.org/cleemesser/numpy-sharedmem
    cd numpy-sharedmem
    python setup.py install --user

Run using threads on vanilla NumPy arrays of size 100k, using 8 processes and 20 tasks per process:

    time python main.py Thread numpy 8 20 100000

Run the same thing, this time using ```multiprocessing.Process``` class instead:

    time python main.py Process numpy 8 20 100000

And now using shared memory for the two cases above:

    time python main.py Thread sharedmem 8 20 100000
    time python main.py Process sharedmem 8 20 100000

