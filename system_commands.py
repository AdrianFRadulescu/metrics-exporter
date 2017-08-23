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
        self.name = name
        self.stats = None
        self.metrics = metrics
        self.sleep_time = sleep_time
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.headers = [self.process.stdout.readline(), self.process.stdout.readline()]
        self.output_stream = self.process.stdout
        self.lock = threading.RLock()

    def _update_metrics(self):
        pass

    def _update_stats(self):
        pass

    # getters

    def get_output_stream(self):
        return self.output_stream

    def get_metrics(self):
        self._update_metrics()
        return self.metrics

    def get_stats(self):
        self._update_stats()
        return self.stats

    def get_sleep_time(self):
        return self.sleep_time

    # setters

    def set_sleep_time(self, new_value):
        self.sleep_time = new_value


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

        # initialize statistics parameters for every given metric


class VMStat(SysCmd):
    """
            Follows the process of the 'vm_stat' command and makes the
            necessary updates
    """

    def __init__(self, cmd, name, metrics, sleep_time):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)


class NetStat(SysCmd):
    """
            Follows the process of the 'netstat' command and makes the
            necessary updates
     """

    def __init__(self, cmd, name, metrics, sleep_time):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)

        self.stats = [0] * 6

    def run(self):

        while getattr(self, 'do_run', True):
            with self.lock:
                self._update_metrics()
            #print 'running {}'.format(self.name)
            time.sleep(self.sleep_time)

        self.process.terminate()
        del self.process
        del self.output_stream
        del self.stats
        self.metrics = None

    def _update_stats(self):
        """
            Read output stream of the followed process and update stats variable
        :return:
        """

        line = 'input'
        while 'input' in line or 'bytes' in line:
            line = self.output_stream.readline()
        self.stats = list(map(lambda x: int(x),line.split()))

    def _update_metrics(self):
        """
            Update the metrics
        :param metrics:
        :return:
        """

        self._update_stats()
        for gm,cm,st in zip(self.metrics['Gauge'], self.metrics['Counter'], self.stats):
            print

