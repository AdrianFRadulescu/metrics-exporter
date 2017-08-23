from prometheus_client import start_http_server

import darwin_metrics
from pprint import pprint


if __name__ == "__main__":

    pprint(darwin_metrics.NETSTAT_METRICS)

    start_http_server(8000)

    while True:
        if raw_input() == 'stop':
            break