"""Test NumPy shared memory.
Arguments:  
   <Thread|Process> <numpy|sharedmem> <num_proc> <tasks_per_proc> <array_size>""" 

import sys
from multiprocessing import Pipe, Process, Manager
from threading import Thread
import numpy
import sharedmem

pclass = eval(sys.argv[1])  # Process or Thread
np = eval(sys.argv[2])  # Use either numpy or sharedmem module.
NUM_PROCS = int(sys.argv[3])  # Number of worker processes to use.
NUM_TASKS = int(sys.argv[4])  # Number of tasks per worker.
ARRAY_SIZE = int(sys.argv[5])  # Size of data array.

conns = list()  # Outgoing connections.
arrays = Manager().dict()  # References to arrays.
procs = list()  # List of spawned processes.

def f(c2):
    """Continuously receive tuple (array, index) from connection,
    compute sum and delete the array. Exit when received array is None."""
    while True:
        a,i = c2.recv()
        if a is None:
            break
        a.sum()  
        del arrays[i]

# Spawn processes (or threads.)
for ii in range(NUM_PROCS):
    c1,c2 = Pipe()
    conns.append(c1)  
    p = pclass(target=f, args=(c2,))
    p.start()
    procs.append(p)

# Send NumPy arrays to processes (or threads.)
count = -1
for ii in range(NUM_TASKS):
    for c1 in conns:
        count += 1
        a = np.ones(ARRAY_SIZE)  # Create array.
        arrays[count] = a
        c1.send((a, count))

# Signal processes (or threads) to stop.
for c1 in conns:
    c1.send((None,None))

# Join forked processes (or threads.)
for p in procs:
    p.join()
