import subprocess
import threading
import psutil

sys_cmd = {
    'darwin': ['iostat', 'vm_stat', 'netstat']
}


class SysCmd(threading.Thread):
    """
        A thread monitoring a terminal system status command
        Covers the arguments, status(with the associated metrics) and output of the command
        Adds data collected via psutils if necessary
    """

    def __init__(self, cmd, name, metrics, sleep_time):
        """
        :param cmd: the process that this object contains
        """
        self.name = name
        self.stats = None
        self.metrics = metrics
        self.sleep_time = sleep_time
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.headers = [self.process.stdout.readline(), self.process.stdout.readline()]
        self.output_stream = self.process.stdout
        threading.Thread.__init__(self)

    def _update_metrics(self, metrics):
        pass

    def _update_stats(self):
        pass


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

    def __init__(self, cmd, name, metrics):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)


class NetStat(SysCmd):
    """
            Follows the process of the 'netstat' command and makes the
            necessary updates
     """

    def __init__(self, cmd, name, metrics):
        SysCmd.__init__(self, cmd=cmd, name=name, metrics=metrics, sleep_time=sleep_time)

        self.stats = [0] * 6

    def _update_stats(self):
        """
            Read output stream of the followed process and update stats variable
        :return:
        """

        line = 'input'
        while 'input' in line or 'bytes' in line:
            line = self.output_stream.readline()

        self.stats = list(map(lambda x: int(x),line.split()))

    def _update_metrics(self, metrics):
        """
            Update the metrics
        :param metrics:
        :return:
        """

        for m in metrics:
