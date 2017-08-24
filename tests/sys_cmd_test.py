import unittest
import system_commands
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

    def test_update_stats(self):

        """
            Test if metrics are updated, not a very efficient method yet
        :return:
        """

        t0 = time.gmtime()
        initial_stats = self.cmd.get_stats()
        ti = time.gmtime()
        time.sleep(self.cmd.get_sleep_time())
        final_stats = self.cmd.get_stats()
        tf = time.gmtime()

        try:
            self.assertNotEqual(initial_stats, final_stats, 'Metrcis were equal')
        except AssertionError:
            self.assertLess(t0,ti, 'metrics were not updated')
            self.assertLess(tf, ti, 'Second update was not done')

    def test_update_metrics(self):

        t0 = time.time()

        initial_metrics = self.cmd.get_metrics()
        time.sleep(4 * self.cmd.get_sleep_time())
        ti = self.cmd.get_last_update_time()
        print 'ti = {}'.format(ti)

        final_metrics = self.cmd.get_metrics()
        time.sleep(4 * self.cmd.get_sleep_time())
        tf = self.cmd.get_last_update_time()
        print 'tf = {}'.format(tf)

        try:
            self.assertNotEqual(initial_metrics, final_metrics, 'Metrcis were equal')
        except AssertionError:
            self.assertTrue(t0 < ti, 'err1')
            self.assertLess(t0, ti, 'metrics were not updated')
            self.assertLess(ti, tf, 'Second update was not done')

    def test_get_metrics(self):
        """
            Check if metrics a re in the right format
        :return:
        """
        self.assertEqual(len(self.component_args['metrics']), self.cmd.get_metrics(), "Component's metrics are not properly transmitted")


class NetStatTestCase(SysCmdTestCase):
    """
        Test the netstat command execution
    """

    __test__ = True
    component = system_commands.NetStat
    component_args = {'cmd':['netstat', '-w 2'], 'metrics': darwin_metrics.NETSTAT_METRICS, 'sleep_time': 2, 'name': 'Netstat'}


class VMStatTestCase(SysCmdTestCase):
    """
        Test the vm_stat command execution
    """

    __test__ = True
    component = system_commands.VMStat
    component_args = {'cmd': ['vm_stat', '2'], 'metrics': darwin_metrics.VM_STAT_METRICS, 'sleep_time': 2, 'name': 'VMStat'}


class IOStatTestCase(SysCmdTestCase):
    """
        Test the iostat command execution
    """

    __test__ = True
    component = system_commands.IOStat
    component_args = {'cmd': ['iostat', '-w 5'], 'metrics': darwin_metrics.IOSTAT_METRICS, 'sleep_time': 5, 'name': 'IOStat'}

del SysCmdTestCase

if __name__ == '__main__':
    unittest.main()