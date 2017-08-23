from prometheus_client import start_http_server, Summary, Histogram, Gauge, Counter
import psutil

"""
    Contains standard metrics for darwin based systems

"""

# netstat metrics

INPUT_PACKETS_COUNT = Gauge('input_packets_count', 'Number of received packets')
INPUT_ERRORS_COUNT = Gauge('input_error_count', 'Number of input errors')
INPUT_SIZE_BYTES = Gauge('input_size_bytes', 'The size of the input')

INPUT_PACKETS_COUNT_TOTAL = Gauge('input_packets_count_total', 'Total number of received packets')
INPUT_ERRORS_COUNT_TOTAL = Gauge('input_error_count_total', 'Total number of input errors')
INPUT_SIZE_BYTES_TOTAL = Gauge('input_size_bytes_total', 'Total size of the input')


OUTPUT_PACKETS_COUNT = Gauge('output_packets_count', 'Number of received packets')
OUTPUT_ERRORS_COUNT = Gauge('output_error_count', 'Number of input errors')
OUTPUT_SIZE_BYTES = Gauge('output_size_bytes', 'The size of the input')

OUTPUT_PACKETS_COUNT_TOTAL = Gauge('output_packets_count_total', 'Total number of received packets')
OUTPUT_ERRORS_COUNT_TOTAL = Gauge('output_error_count_total', 'Total number of input errors')
OUTPUT_SIZE_BYTES_TOTAL = Gauge('output_size_bytes_total', 'Total size of the input')

NETSTAT_METRICS = [

    INPUT_PACKETS_COUNT,
    INPUT_ERRORS_COUNT,
    INPUT_SIZE_BYTES,

    INPUT_PACKETS_COUNT_TOTAL,
    INPUT_ERRORS_COUNT_TOTAL,
    INPUT_SIZE_BYTES_TOTAL,

    OUTPUT_PACKETS_COUNT,
    OUTPUT_ERRORS_COUNT,
    OUTPUT_SIZE_BYTES,

    OUTPUT_PACKETS_COUNT_TOTAL,
    OUTPUT_ERRORS_COUNT_TOTAL,
    OUTPUT_SIZE_BYTES_TOTAL

]


# vm_stat metrics
VM_FREE_PAGES = Gauge('vm_free_pages', 'Number of free pages in Virtual Memory')
VM_ACTIVE_PAGES = Gauge('vm_active_pages', 'Number of active pages')

VM_METRICS = [
    VM_FREE_PAGES,
    VM_ACTIVE_PAGES
]


# iostat metrics

# Disk
# count disks
from subprocess import Popen, PIPE
proc = Popen('iostat', stdout=PIPE)
disks = proc.stdout.readline().split()[:-3]
proc.terminate()

DISK_TRANSFER_METRICS = {}

for d in disks:

    DISK_TRANSFER_METRICS[d] = []

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfers', 'Disk transfers per second')]
    DISK_TRANSFER_METRICS[d] += [Counter(d + '_transfers_total', 'Total number of disk transfers made')]

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfer_size_kilobytes', 'Size of transfer')]
    DISK_TRANSFER_METRICS[d] += [Counter(d +'_transfer_size_bytes_total', 'Total nuber of transfered bytes')]


# CPU
CPU_USAGE_RATIO = Gauge('cpu_usage_ratio', '% of cpu time in user, system and idle modes', ['mode'])

# Load Average
CPU_LOAD_AVERAGE_1M = Gauge('cpu_load_average_1m', 'CPU current load average on a 1m span')
CPU_LOAD_AVERAGE_5M = Gauge('cpu_load_average_5m', 'CPU current load average on a 5m span')
CPU_LOAD_AVERAGE_15M = Gauge('cpu_load_average_15m', 'CPU current load average on a 15m span')

IOSTAT_METRICS = [

    DISK_TRANSFER_METRICS,

]


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    #start_http_server(8000)
    # Generate some requests.


    print psutil.cpu_times(True)
    print
    print psutil.cpu_times()

    print psutil.disk_io_counters(True)
    print psutil.disk_partitions(all=True)

    print
    print