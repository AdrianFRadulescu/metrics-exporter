from prometheus_client import start_http_server

import darwin_metrics

from system_commands import NetStat, VMStat, IOStat

from pprint import pprint


if __name__ == "__main__":

    start_http_server(7800)

    # use mo

    netstat = NetStat(**{'cmd': ['netstat', '-w 10'], 'metrics': darwin_metrics.NETSTAT_METRICS, 'sleep_time': 10, 'name': 'Netstat'})
    vm_stat = VMStat(**{'cmd': ['vm_stat', '10'], 'metrics': darwin_metrics.VM_STAT_METRICS, 'sleep_time': 10, 'name': 'VMstat'})
    iostat  = IOStat(**{'cmd': ['iostat', '10'], 'metrics': darwin_metrics.IOSTAT_METRICS, 'sleep_time': 10, 'name': 'IOtstat'})

    netstat.start()
    vm_stat.start()
    iostat.start()

    while True:
        if raw_input() == 'stop':
            break

    # signal monitoring threads to stop

    netstat.do_run = False
    vm_stat.do_run = False
    iostat.do_run = False

    # wait for threads to stop

    netstat.join()
    vm_stat.join()
    iostat.join()