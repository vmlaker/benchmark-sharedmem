Performance benchmark of NumPy shared memory.

First, install Python virtual environment and numpy-sharedmem:

    make

Run using threads on vanilla NumPy arrays of size 100K, using 8 processes and 20 tasks per process:

    time ./python main.py Thread numpy 8 20 100000

Run the same thing, this time using ```multiprocessing.Process``` class instead:

    time ./python main.py Process numpy 8 20 100000

And now using shared memory for the two cases above:

    time ./python main.py Thread sharedmem 8 20 100000
    time ./python main.py Process sharedmem 8 20 100000
