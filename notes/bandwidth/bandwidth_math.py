# Calculations from our CUDA GPU instrumentation
time_to_transfer_seconds = (386.861  # microseconds
                            / 1E6)  # to seconds
data_transferred_mb = 4.5  # data of mb

mb_per_second = data_transferred_mb / time_to_transfer_seconds
gb_per_second = mb_per_second / 1000

print("{} MB/s potential transfer speed from small CUDA test".format(mb_per_second))
print("{} GB/s potential transfer speed from small CUDA test".format(gb_per_second))

################################################################

# Calculated memory transfer usinghttps://zsmith.co/bandwidth.php
#TODO
