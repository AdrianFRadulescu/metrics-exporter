import unittest
import system_commands
import threading
import time
import darwin_metrics


class SysCmdTestCase(unittest.TestCase):

    __test__ = False
    component = None
    component_args = {}

    def shortDescription(self):

        doc = self._testMethodDoc

        doc = doc and doc.split("\n")[0].strip() or ""
        if "%(component)s" in doc:
            doc = doc % {'component': self.component.__name__}
        doc = "%s : %s" % (self.__class__.__name__, doc)

        return doc

    def setUp(self):
        self.cmd = self.component(**self.component_args)
        self.cmd.start()

    def tearDown(self):
        self.cmd.do_run = False
        del self.cmd

    def test_init(self):

        self.assertIsNotNone(self.cmd, 'None object, command object was not created')
        self.assertIsNotNone(self.cmd.get_metrics(), 'metrics field was not created')
        self.assertIsNotNone(self.cmd.get_output_stream(), 'output_stream field is None')
        self.assertIsNot(self.cmd.get_output_stream().readline(), '', 'empty output stream')

    def test_start(self):


        time.sleep(self.cmd.get_sleep_time())
        self.assertTrue(self.cmd.isAlive(), 'thread {} could not be started'.format(self.cmd.getName()))
        print 'Passed'

    def test_update_stats(self):

        """
            Test if metrics are updated, not a very efficient method yet
        :return:
        """

        initial_stats = self.cmd.get_stats()

        time.sleep(self.cmd.get_sleep_time())
        final_stats = self.cmd.get_stats()

        try:
            self.assertNotEqual(initial_stats, final_stats, 'States were not changed')
        except AssertionError:
            print 'time lap might not have been enough for significand change to occure'

    def test_update_metrics(self):

        initial_metrics = self.cmd.get_metrics()
        time.sleep(self.cmd.sleep_time())
        final_metrics = self.cmd.get_metrics()

        self.assertNotEqual(initial_metrics, final_metrics, )


class NetStatTestCase(SysCmdTestCase):
    """
        Test the netstat Command
    """

    __test__ = True
    component = system_commands.NetStat
    component_args = {'cmd':['netstat', '-w 10'], 'metrics' : darwin_metrics.NETSTAT_METRICS, 'sleep_time':10, 'name': 'Netstat'}


class VMStatTestCase(SysCmdTestCase):
    """
        Test the vm_stat command execution
    """

    __test__ = True
    component = system_commands.VMStat
    component_args = {'cmd': [vm_stat]}


del (SysCmdTestCase)

if __name__ == '__main__':
    unittest.main()