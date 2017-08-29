import subprocess
import threading
import psutil
import time

sys_cmd = {
    'darwin': ['iostat', 'vm_stat', 'netstat']
}


class SysCmd(threading.Thread):
    """
        A thread monitoring a terminal system status command
        Covers the arguments, status(with the associated metrics) and output of the command
        Adds data collected via psutils if necessary

        Note:
            Each child class which tracks specific commands will make
            assumptions on the provided metrics(which need to be
            in the appropriate order for the command)

    """

    def __init__(self, cmd, name, metrics=None, sleep_time=1):
        """

        :param cmd: the process that this object contains
                    format has to be list of string representing the arguments:param name:
        :param metrics: a list of the metrics this thread needs to update
        :param sleep_time:
        """
        threading.Thread.__init__(self)
        self._name = name
        self._stats = None
        self._metrics = metrics
        self._last_update_time = time.time()
        self._sleep_time = sleep_time
        self._process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self._headers = [self._process.stdout.readline(), self._process.stdout.readline()]
        self._output_stream = self._process.stdout
        self._lock = threading.RLock()

    def run(self):

        while getattr(self, 'do_run', True):
            self._update_metrics()
            self._last_update_time = time.time()
            time.sleep(self._sleep_time)

        self._process.terminate()
        del self._process
        del self._output_stream
        del self._stats
        self._metrics = None

    def _update_stats(self):
        """
            Updates the stats with the values outputed by the process
        :return:
        """
        def __convert(val):
            f = int if '.' not in val else float
            return f(val[:-1]) * 1000 if val[-1] == 'K' else f(val)

        line = 'input'
        while any(map(lambda w: w in line, ['input', 'packets', 'free', 'Virtual', 'disk', 'bytes', 'memory', 'KB/t'])):
            line = self._output_stream.readline()
        self._stats = list(map(lambda x: __convert(x), line.split()))

    def _update_metrics(self):
        pass

    # getters

    def get_output_stream(self):
        return self._output_stream

    def get_metrics(self):
        self._update_metrics()
        return self._metrics

    def get_stats(self):
        self._update_stats()
        return self._stats

    def get_sleep_time(self):
        return self._sleep_time

    def get_last_update_time(self):
        return self._last_update_time

    # setters

    def set_sleep_time(self, new_value):
        self._sleep_time = new_value


class IOStat(SysCmd):
    """
        Follows the process of the 'iostat' command and makes the
        necessary updates
    """

    def __init__(self, cmd, name, metrics, sleep_time):
        """

        :param cmd: the given command
        :param name: the name of the thread
        :param metrics: the list of metrics that needs to be updated by this thread
                        metrics need to correspond to the stats displayed by the command
        """

        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)

    def _update_metrics(self):
        self._update_stats()

        with self._lock:

            st = iter(self._stats)

            # update disk metrics
            for disk in self._metrics[0]:

                # KB/t update
                self._metrics[0][disk][0].set(float(st.next()))
                # tps update
                tps = float(st.next())
                self._metrics[0][disk][1].set(tps)
                self._metrics[0][disk][2].inc(tps)

                # MB/s update
                mbps = float(st.next())
                self._metrics[0][disk][3].set(mbps)
                self._metrics[0][disk][4].inc(mbps * self._sleep_time)

            # update cpu usage metrics
            for mode in ['us', 'sy', 'id']:
                self._metrics[1].labels(mode=mode).set(float(st.next()))

            # update cpu average load metrics
            for q in ['1m','5m','15m']:
                self._metrics[2].labels(quantile=q).set(float(st.next()))


class VMStat(SysCmd):
    """
            Follows the process of the 'vm_stat' command and makes the
            necessary updates
    """

    def __init__(self, cmd, name, metrics, sleep_time):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)

    def _update_metrics(self):
        self._update_stats()

        with self._lock:
            for m, st in zip(self._metrics, self._stats):
                if 'Gauge' in str(type(m)):
                    m.set(st)
                elif 'Counter' in str(type(m)):
                    m.inc(st)


class NetStat(SysCmd):
    """
            Follows the process of the 'netstat' command and makes the
            necessary updates
     """

    def __init__(self, cmd, name, metrics, sleep_time):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)
        self.stats = [0] * 6

    def _update_metrics(self):
        """
            Update the metrics
        """
        self._update_stats()

        with self._lock:
            for gm,cm,st in zip(self._metrics['Gauge'], self._metrics['Counter'], self._stats):
                gm.set(st)
                cm.inc(st)