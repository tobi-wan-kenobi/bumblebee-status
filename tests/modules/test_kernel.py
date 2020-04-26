import unittest

import core.config
import modules.core.kernel

class kernel(unittest.TestCase):
    def setUp(self):
        self.someKernel = 'this-is-my-kernel'
        self.module = modules.core.kernel.Module(config=core.config.Config([]), theme=None)

    def test_full_text(self):
        with unittest.mock.patch('modules.core.kernel.platform') as platform:
            platform.release.return_value = self.someKernel
            self.assertEqual(1, len(self.module.widgets()))
            self.assertEqual(self.someKernel, self.module.widget().full_text())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
