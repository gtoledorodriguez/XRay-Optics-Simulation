import multiprocessing
import sys
import time
from multiprocessing import Queue

from typing import Callable, List


def run_multicore_test(cpu_cores: int = 8, number_calculations: int = 1000000, sleep_time: float = 5):
    """

    :param cpu_cores: Number of cores to use.
    :param number_calculations: Number of calculations per core to run.
    :param sleep_time: Time to sleep.
    :return: TODO
    """

    # Initialize arrays based on arguments provided
    q = Queue()  # used to save information generated within child process in separate core
    
    calculations_per_core = int(number_calculations / cpu_cores)  # Splits val into [numberCores] parts, which will need to merge later
    # create an array of arrays
    jobs = cpu_cores*[cpu_cores*[]]

    # Independent functions to fill arrays within separate cores with corresponding values  
    def generate_core_fn(core_number, work_array: List[List[int]], calculations_per_core) -> Callable[[int], None]:
        """Generate a function for a core to run. TODO"""

        def core_n():
            for i in range(calculations_per_core):
                work_array.append(i)
            q.put(work_array)
            #print("Core {}: Job Done".format(core_number))
            pass

        return core_n

        pass


    core_functions = list(map(lambda x: generate_core_fn( x, jobs[x], len(jobs[x]) ), range(cpu_cores)))

    # Separate processeses between [numberCores] cores
        
    threads = []
    
    for i in range(cpu_cores):
        threads.append(multiprocessing.Process(target=core_functions[i]))

    for thread in threads:
        thread.daemon = True

    # START TIMER, run processes
    start = time.time()
    for thread in threads:
        thread.start()

    for i in range(len(threads)):
        if threads[i].is_alive():
            #print("Joining thread " + str(i))
            threads[i].join()

    # Get objects in queue
    if q.empty():
        print("\nFail: Timer too short to allow child processes enough time to join parent\nProgram terminated\n")
        sys.exit(0)

    # Merge objects from queue into a single array
    mergedArray = []
    for n in range(0, cpu_cores):
        mergedArray = mergedArray + q.get()

    # TOTAL operating time of split loops
    # print("\nTotal time multi:")
    multiTime = (time.time() - start) - sleep_time
    # print(multiTime)

    # Compare with making a single array on one core
    array = []
    newstart = time.time()
    for j in range(0, number_calculations):
        array.append(j)

    time.sleep(sleep_time)
    # print("\nTotal time single: ")
    singleTime = (time.time() - newstart) - sleep_time
    # print(singleTime)

    print("\nEfficiency ratio:\n",(multiTime/singleTime), "\n")
    return (multiTime, singleTime)
