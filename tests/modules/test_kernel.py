import unittest

import modules.kernel

class kernel(unittest.TestCase):
    def setUp(self):
        self.someKernel = 'this-is-my-kernel'
        with unittest.mock.patch('modules.kernel.platform') as platform:
            platform.release.return_value = self.someKernel
            self.module = modules.kernel.Module()

    def test_full_text(self):
        self.assertEqual(1, len(self.module.widgets()))
        self.assertEqual(self.someKernel, self.module.widgets()[0].full_text())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
