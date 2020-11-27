'''
This is the pure python script version of gpu-memory-test-stats.ipynb.
The exact same charts and graphs can be created from this script. Use this
script if you don't like Jupyter Notebooks or if you wish to immediately
save the generated tables and graphs. It's also slightly simpler to use this
script if you're accessing via ssh.
'''

import pandas
import matplotlib.pyplot as plt

def calculate_total_point_sources(slitHeight: int, numOfSlits: int, pointSourcesPerSlit: int) -> int:
    """Given slit height in nm, number of slits, and the number of point sources per slit,
    calculate the number of total point sources"""
    return ((slitHeight-1)*(numOfSlits)) * pointSourcesPerSlit


def main():

    df = pandas.read_csv('gpu-memory-test-realistic-params.csv')
    df = df.sort_values('sourcePoints')

    # add other time formats
    df=df.assign(**{"total-time (minutes)": df['total-time (ms)']/1000/60})
    df=df.assign(**{"total-time (hours)": df['total-time (minutes)']/60})

    df=df.assign(**{"mem-to-gpu-time (minutes)": df['mem-to-gpu-time (ms)']/1000/60})
    df=df.assign(**{"mem-to-gpu-time (hours)": df['mem-to-gpu-time (minutes)']/60})

    df=df.assign(**{"kernel-time (minutes)": df['kernel-time (ms)']/1000/60})
    df=df.assign(**{"kernel-time (hours)": df['kernel-time (minutes)']/60})

    df=df.assign(**{"GPU to CPU transfer (GB)": df['bytes-transferred-total-gpu-to-cpu (DtoH)']/1e9})
    df=df.assign(**{"CPU to GPU transfer (GB)": df['bytes-transferred-total-cpu-to-to-gpu (HtoD)']/1e9})

    df=df.assign(**{"RAM used (GB)": df['bytes-ram-used-at-end']/1e9})

    # calculate how many individual point sources there are
    df=df.assign(**{"N (# of total point sources)": 

        calculate_total_point_sources(
            slitHeight=df['slit-height'],
            numOfSlits=df['num-of-slits'],
            pointSourcesPerSlit=df['sourcePoints']),
    })

    df.to_csv('realsitic_results.csv', index=False)

    plt.title("Kernel time and Memory-to-GPU time and total time vs. N") 
    plt.rcParams["font.size"] = 12
    plt.tick_params(labelsize=12)

    plt.ylabel("Time (hours)") 

    ax = plt.gca()
    df.plot(kind='line',x='N (# of total point sources)',y='mem-to-gpu-time (hours)', color='red', ax=ax)
    df.plot(kind='line',x='N (# of total point sources)',y='kernel-time (hours)', color='green', ax=ax)
    df.plot(kind='line',x='N (# of total point sources)',y='total-time (hours)',ax=ax) # total time slightly eclipses kernel time

    plt.savefig('kernel-time-v-N.png')

    Show relevant parts of our dataframe
    header = ['N (# of total point sources)','total-time (hours)','kernel-time (hours)']
    df.to_csv('kernel-time-v-N.csv', columns=header, index=False)


    #made as comparison that the kernel time makes up a majority of the time
    plt.title("Kernel time and Memory-to-GPU time vs. N") 
    plt.rcParams["font.size"] = 12
    plt.tick_params(labelsize=12)
    plt.ylabel("Time (hours)") 

    ax = plt.gca()
    df.plot(kind='line',x='sourcePoints',y='mem-to-gpu-time (hours)', color='red', ax=ax)
    df.plot(kind='line',x='sourcePoints',y='kernel-time (hours)', color='green', ax=ax)
    plt.savefig('kernel-time-gpu-mem-v-N.png')


    plt.title("Log plot of kernel time and Memory-to-GPU time vs. N")
    plt.rcParams["font.size"]=12
    plt.tick_params(labelsize=12)
    plt.ylabel("Time (hours)")

    ax = plt.gca()
    df.plot(logy=True, kind='line',x='sourcePoints',y='mem-to-gpu-time (hours)', color='red', ax=ax)
    df.plot(logy=True, kind='line',x='sourcePoints',y='kernel-time (hours)', color='green', ax=ax)
    plt.savefig('log-kernel-time-gpu-mem-v-N.png')


    plt.title("Log-Log plot of Kernel time and Memory-to-GPU time vs. N")
    plt.rcParams["font.size"] = 12
    plt.tick_params(labelsize=12)
    plt.ylabel("Time (hours)")

    ax = plt.gca()
    df.plot(loglog=True, kind='line',x='sourcePoints',y='mem-to-gpu-time (hours)', color='red', ax=ax)
    df.plot(loglog=True, kind='line',x='sourcePoints',y='kernel-time (hours)', color='green', ax=ax)
    plt.savefig('log-log-kernel-time-gpu-mem-v-N.png')


    plt.title("Total bytes transferred between GPU and CPU")
    plt.rcParams["font.size"] = 12
    plt.tick_params(labelsize=12)

    plt.ylabel("Gigabytes") 

    ax = plt.gca()
    df.plot(kind='line',x='sourcePoints',y='GPU to CPU transfer (GB)', color='red', ax=ax)
    df.plot(kind='line',x='sourcePoints',y='CPU to GPU transfer (GB)', ax=ax)
    plt.savefig('byte-trans-gpu-cpu')


    plt.title("Total memory usage by Python on CPU")
    plt.ylabel("Gigabytes")

    ax = plt.gca()
    df.plot(kind='line', x='N (# of total point sources)', y='RAM used (GB)', ax=ax)
    plt.savefig('total-usage-cpu.png')

    header = ['N (# of total point sources)', 'RAM used (GB)']
    df.to_csv('total-usage-cpu.csv', columns=header, index=False)

if __name__ == "__main__":
    main()
