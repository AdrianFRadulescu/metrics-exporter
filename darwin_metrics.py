from prometheus_client import start_http_server, Summary, Histogram, Gauge, Counter
import psutil

"""
    Contains standard metrics for darwin based systems
"""

# netstat metrics

_INPUT_PACKETS_COUNT = Gauge('input_packets_count', 'Number of received packets')
INPUT_ERRORS_COUNT = Gauge('input_error_count', 'Number of input errors')
INPUT_SIZE_BYTES = Gauge('input_size_bytes', 'The size of the input')

INPUT_PACKETS_COUNT_TOTAL = Counter('input_packets_count_total', 'Total number of received packets')
INPUT_ERRORS_COUNT_TOTAL = Counter('input_error_count_total', 'Total number of input errors')
INPUT_SIZE_BYTES_TOTAL = Counter('input_size_bytes_total', 'Total size of the input')


OUTPUT_PACKETS_COUNT = Gauge('output_packets_count', 'Number of received packets')
OUTPUT_ERRORS_COUNT = Gauge('output_error_count', 'Number of input errors')
OUTPUT_SIZE_BYTES = Gauge('output_size_bytes', 'The size of the input')

OUTPUT_PACKETS_COUNT_TOTAL = Counter('output_packets_count_total', 'Total number of received packets')
OUTPUT_ERRORS_COUNT_TOTAL = Counter('output_error_count_total', 'Total number of input errors')
OUTPUT_SIZE_BYTES_TOTAL = Counter('output_size_bytes_total', 'Total size of the input')

NETSTAT_METRICS = {

    'Gauge': [
        _INPUT_PACKETS_COUNT, INPUT_ERRORS_COUNT, INPUT_SIZE_BYTES,
        OUTPUT_PACKETS_COUNT, OUTPUT_ERRORS_COUNT, OUTPUT_SIZE_BYTES
    ],

    'Counter': [
        INPUT_PACKETS_COUNT_TOTAL, INPUT_ERRORS_COUNT_TOTAL, INPUT_SIZE_BYTES_TOTAL,
        OUTPUT_PACKETS_COUNT_TOTAL,OUTPUT_ERRORS_COUNT_TOTAL, OUTPUT_SIZE_BYTES_TOTAL
    ]

}

# vm_stat metrics
VM_FREE_PAGES_COUNT = Gauge('vm_free_pages_count', 'Number of free pages in Virtual Memory')
VM_ACTIVE_PAGES_COUNT = Gauge('vm_active_pages_count', 'Number of active pages')
VM_SPECUL_PAGES_COUNT = Gauge('vm_speculative_pages_count', 'Number of pages on the speculative list.')
VM_INACTIVE_PAGES_COUNT = Gauge('vm_inactiv_pages_count', 'Number of inactive pages')

VM_THROTTLED_PAGES_COUNT = Gauge('VM_THROTTLED_PAGES_COUNT'.lower(), 'Number of pages on the throttled list (not wired but not pageable).')
VM_WIRED_DOWN_PAGES_COUNT = Gauge('VM_WIRED_DOWN_PAGES_COUNT'.lower(), 'The total number of pages wired down.  That is, pages that cannot be paged out.')

VM_PURGEABLE_PAGES_COUNT = Gauge('VM_PURGEABLE_PAGES_COUNT'.lower(), 'Number of purgeable pages')

VM_TRANSLATION_FAULTS_COUNT = Counter('VM_TRANSLATION_FAULTS_COUNT'.lower(), 'Number of times the "vm_fault" routine has been called.')
VM_COPY_ON_WRITE_COUNT = Counter('VM_COPY_ON_WRITE_COUNT'.lower(), 'Number of faults that caused a page to be copied')

VM_ZERO_FILLED_PAGES_COUNT = Counter('VM_ZERO_FILLED_PAGES_COUNT'.lower(), 'Total number of pages that have been zero-filled on demand.')
VM_REACTIVE_PAGES_COUNT = Gauge('VM_REACTIVE_PAGES_COUNT'.lower(), '')

VM_PURGED_PAGES_TOTAL = Counter('VM_PURGED_PAGES_TOTAL'.lower(), 'Total number of pages that have been purged')


VM_STAT_METRICS = [
    VM_FREE_PAGES_COUNT,
    VM_ACTIVE_PAGES_COUNT,
    VM_SPECUL_PAGES_COUNT,
    VM_INACTIVE_PAGES_COUNT,
    VM_THROTTLED_PAGES_COUNT,
    VM_WIRED_DOWN_PAGES_COUNT,
    VM_PURGEABLE_PAGES_COUNT,
    VM_TRANSLATION_FAULTS_COUNT,
    VM_COPY_ON_WRITE_COUNT,
    VM_ZERO_FILLED_PAGES_COUNT,
    VM_REACTIVE_PAGES_COUNT,
    VM_PURGED_PAGES_TOTAL
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

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_kilobytes_per_transfer', 'Current transfer average size')]

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfers_count', 'Current number of disk transfers per second')]
    DISK_TRANSFER_METRICS[d] += [Counter(d + '_transfers_total', 'Total number of disk transfers made')]

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfer_size_kilobytes', 'Size of transfer')]
    DISK_TRANSFER_METRICS[d] += [Counter(d + '_transfer_size_bytes_total', 'Total number of transfered bytes')]


# CPU
CPU_USAGE_RATIO = Gauge('cpu_usage_ratio', '% of cpu time in user, system and idle modes', ['mode'])

# Load Average
CPU_LOAD_AVERAGE = Gauge('cpu_load_average', 'CPU current load average on a 1m span', ['quantile'])


IOSTAT_METRICS = [

    DISK_TRANSFER_METRICS,
    CPU_USAGE_RATIO,
    CPU_LOAD_AVERAGE
]


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    #start_http_server(8000)
    # Generate some requests.

    from pprint import pprint
    pprint(IOSTAT_METRICS[0]['disk0'][1])