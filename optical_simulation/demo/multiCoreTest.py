import multiprocessing
import sys
import time
from multiprocessing import Queue


def run_multicore_test(cpu_cores: int = 8, calculations: int = 1000000, sleep_time: float = 5):
    """

    :param cpu_cores: Number of cores to use.
    :param calculations: Number of calculations per core to run.
    :param sleep_time: Time to sleep.
    :return: TODO
    """

    numberCores = int(cpu_cores)

    val = calculations

    sleeptimer = float(sleep_time)

    # Initialize arrays based on arguments provided
    q = Queue()  # used to save information generated within child process in separate core
    array1 = []
    array2 = []

    if numberCores > 2:
        array3 = []
    if numberCores > 3:
        array4 = []
    if numberCores > 4:
        array5 = []
    if numberCores > 5:
        array6 = []
    if numberCores > 6:
        array7 = []
    if numberCores > 7:
        array8 = []

    # Independent functions to fill arrays within separate cores with corresponding values

    multiVal = int(val / numberCores)  # Splits val into [numberCores] parts, which will need to merge later

    def core1(n):
        for i in range(0, multiVal):
            array1.append(i)
        q.put(array1)

    def core2(n):
        for i in range(0, multiVal):
            array2.append(i + multiVal)
        q.put(array2)

    def core3(n):
        for i in range(0, multiVal):
            array3.append(i + (multiVal * 2))
        q.put(array3)

    def core4(n):
        for i in range(0, int(val / numberCores)):
            array4.append(i + (multiVal * 3))
        q.put(array4)

    def core5(n):
        for i in range(0, multiVal):
            array5.append(i + (multiVal * 4))
        q.put(array5)

    def core6(n):
        for i in range(0, multiVal):
            array6.append(i + (multiVal * 5))
        q.put(array6)

    def core7(n):
        for i in range(0, multiVal):
            array7.append(i + (multiVal * 6))
        q.put(array7)

    def core8(n):
        for i in range(0, multiVal):
            array8.append(i + (multiVal * 7))
        q.put(array8)

    # Separate processeses between [numberCores] cores

    for i in range(1):  # Scaled to create between 2 to 8 cores based on args provided
        t = multiprocessing.Process(target=core1, args=(i,))
        t2 = multiprocessing.Process(target=core2, args=(i,))
        if numberCores > 2:
            t3 = multiprocessing.Process(target=core3, args=(i,))
        if numberCores > 3:
            t4 = multiprocessing.Process(target=core4, args=(i,))
        if numberCores > 4:
            t5 = multiprocessing.Process(target=core5, args=(i,))
        if numberCores > 5:
            t6 = multiprocessing.Process(target=core6, args=(i,))
        if numberCores > 6:
            t7 = multiprocessing.Process(target=core7, args=(i,))
        if numberCores > 7:
            t8 = multiprocessing.Process(target=core8, args=(i,))

        # 'daemon = true' stops the parent process from having to wait for child processes to end before terminating.
        t.daemon = True
        t2.daemon = True
        if numberCores > 2:
            t3.daemon = True
        if numberCores > 3:
            t4.daemon = True
        if numberCores > 4:
            t5.daemon = True
        if numberCores > 5:
            t6.daemon = True
        if numberCores > 6:
            t7.daemon = True
        if numberCores > 7:
            t8.daemon = True

        # START TIMER, run processes
        start = time.time()

        t.start()  # start processes
        t2.start()
        if numberCores > 2:
            t3.start()
        if numberCores > 3:
            t4.start()
        if numberCores > 4:
            t5.start()
        if numberCores > 5:
            t6.start()
        if numberCores > 6:
            t7.start()
        if numberCores > 7:
            t8.start()

    mylist = []  # Used to retrieve values from queue sequentially

    time.sleep(sleeptimer)  # FIXME: This is a race condition!

    # Get objects in queue
    if q.empty():
        print("\nFail: Timer too short to allow child processes enough time to join parent\nProgram terminated\n")
        sys.exit(0)
    # while not q.empty():
    #   mylist.append(q.get())

    # Merge objects from queue into a single array
    mergedArray = []
    for n in range(0, numberCores):
        mergedArray = mergedArray + q.get()

    # TOTAL operating time of split loops
    # print("\nTotal time multi:")
    multiTime = (time.time() - start) - sleeptimer
    # print(multiTime)

    # Compare with making a single array on one core
    array = []
    newstart = time.time()
    for j in range(0, val):
        array.append(j)
    time.sleep(sleeptimer)
    # print("\nTotal time single: ")
    singleTime = (time.time() - newstart) - sleeptimer
    # print(singleTime)

    # print("\nEfficiency ratio:\n",(multiTime/singleTime), "\n")
    return (multiTime, singleTime)
