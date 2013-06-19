from subprocess import Popen, PIPE, STDOUT
from datetime import timedelta
import re

NUM_PROCS = range(1, 2+1)
METHODS = ('Process',)#, 'Thread')
MODULES = ('numpy', 'sharedmem')
NUM_TASKS = (24,)
ARRAY_SIZE = (100000,)
NUM_SAMPLES = 5

def test(method, module, num_procs, num_tasks, array_size):
    command = '/usr/bin/time -f "%E" python main.py {} {} {} {} {}'.format(
        method, module, num_procs, num_tasks, array_size)
    #print(command)
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    p.wait()
    tstring = p.stdout.readlines()[0].strip()
    #print(tstring)
    result = map(int, re.split('\:|\.', tstring))
    d = timedelta(
        minutes=result[0],
        seconds=result[1],
        microseconds=result[2]*10000,
        )
    return d.total_seconds()

elapsed = dict()
for num_procs in NUM_PROCS:
    elapsed[num_procs] = dict()
    for method in METHODS:
        for module in MODULES:
            import sys
            sys.stdout.write('{}{}'.format(num_procs, module[0]))
            sys.stdout.flush()
            elapsed[num_procs][module] = dict()
            for num_tasks in NUM_TASKS:
                for array_size in ARRAY_SIZE:
                    for sample in range(NUM_SAMPLES):
                        duration = test(method, module, num_procs, num_tasks, array_size)
                        elapsed[num_procs][module][sample] = duration
print('')
for num_procs in NUM_PROCS:
    for module in MODULES:
        durations = [xx for xx in elapsed[num_procs][module].values()]
        average = sum(durations)/len(durations)
        print '{:2d} {:12s} {:.3f}'.format(
            num_procs, module, average)
