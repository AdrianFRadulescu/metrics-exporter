from prometheus_client import start_http_server, Summary, Histogram, Gauge, Counter
import psutil

"""
    Contains standard metrics for darwin based systems
"""

# netstat metrics

INPUT_PACKETS = Gauge('input_packets', 'Number of received packets')
INPUT_ERRORS = Gauge('input_error', 'Number of input errors')
INPUT_SIZE_BYTES = Gauge('input_size_bytes', 'The size of the input')

INPUT_PACKETS_TOTAL = Counter('input_packets_total', 'Total number of received packets')
INPUT_ERRORS_TOTAL = Counter('input_error_total', 'Total number of input errors')
INPUT_SIZE_BYTES_TOTAL = Counter('input_size_bytes_total', 'Total size of the input')


OUTPUT_PACKETS = Gauge('output_packets', 'Number of received packets')
OUTPUT_ERRORS = Gauge('output_error', 'Number of input errors')
OUTPUT_SIZE_BYTES = Gauge('output_size_bytes', 'The size of the input')

OUTPUT_PACKETS_TOTAL = Counter('output_packets_total', 'Total number of received packets')
OUTPUT_ERRORS_TOTAL = Counter('output_error_total', 'Total number of input errors')
OUTPUT_SIZE_BYTES_TOTAL = Counter('output_size_bytes_total', 'Total size of the input')

NETSTAT_METRICS = {

    'Gauge': [
        INPUT_PACKETS, INPUT_ERRORS, INPUT_SIZE_BYTES,
        OUTPUT_PACKETS, OUTPUT_ERRORS, OUTPUT_SIZE_BYTES
    ],

    'Counter': [
        INPUT_PACKETS_TOTAL, INPUT_ERRORS_TOTAL, INPUT_SIZE_BYTES_TOTAL,
        OUTPUT_PACKETS_TOTAL,OUTPUT_ERRORS_TOTAL, OUTPUT_SIZE_BYTES_TOTAL
    ]

}

# vm_stat metrics
VM_FREE_PAGES = Gauge('vm_free_pages', 'Number of free pages in Virtual Memory')
VM_ACTIVE_PAGES = Gauge('vm_active_pages', 'Number of active pages')
VM_SPECUL_PAGES = Gauge('vm_speculative_pages', 'Number of pages on the speculative list.')
VM_INACTIVE_PAGES = Gauge('vm_inactiv_pages', 'Number of inactive pages')

VM_THROTTLED_PAGES = Gauge('VM_THROTTLED_PAGES'.lower(), 'Number of pages on the throttled list (not wired but not pageable).')
VM_WIRED_DOWN_PAGES = Gauge('VM_WIRED_DOWN_PAGES'.lower(), 'The total number of pages wired down.  That is, pages that cannot be paged out.')

VM_PURGEABLE_PAGES = Gauge('VM_PURGEABLE_PAGES'.lower(), 'Number of purgeable pages')

VM_TRANSLATION_FAULTS_TOTAL = Counter('VM_TRANSLATION_FAULTS'.lower(), 'Number of times the "vm_fault" routine has been called.')
VM_COPY_ON_WRITE_COUNT = Counter('VM_COPY_ON_WRITE'.lower(), 'Number of faults that caused a page to be copied')

VM_ZERO_FILLED_PAGES_TOTAL = Counter('VM_ZERO_FILLED_PAGES_TOTAL'.lower(), 'Total number of pages that have been zero-filled on demand.')
VM_REACTIVE_PAGES = Gauge('VM_REACTIVE_PAGES'.lower(), '')

VM_PURGED_PAGES_TOTAL = Counter('VM_PURGED_PAGES_TOTAL'.lower(), 'Total number of pages that have been purged')


VM_STAT_METRICS = [

    VM_FREE_PAGES,
    VM_ACTIVE_PAGES,
    VM_SPECUL_PAGES,
    VM_INACTIVE_PAGES,
    VM_THROTTLED_PAGES,
    VM_WIRED_DOWN_PAGES,
    VM_PURGEABLE_PAGES,
    VM_TRANSLATION_FAULTS_TOTAL,
    VM_COPY_ON_WRITE_COUNT,
    VM_ZERO_FILLED_PAGES_TOTAL,
    VM_REACTIVE_PAGES,
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

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfer_size_kilobytes', 'Current transfer average size')]

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_transfers', 'Current number of disk transfers per second')]
    DISK_TRANSFER_METRICS[d] += [Counter(d + '_transfers_total', 'Total number of disk transfers made')]

    DISK_TRANSFER_METRICS[d] += [Gauge(d + '_data_transfer_rate_megabytes_per_second', 'Size of transfer')]
    DISK_TRANSFER_METRICS[d] += [Counter(d + '_transfer_size_megabytes_total', 'Total number of transfered bytes')]


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