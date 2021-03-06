# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test 'create'.
"""

import time
import unittest

from stratis_cli._errors import StratisCliDbusLookupError

from .._misc import _device_list
from .._misc import RUNNER
from .._misc import Service

_DEVICE_STRATEGY = _device_list(1)


class AddTestCase(unittest.TestCase):
    """
    Test adding devices to a non-existant pool.
    """
    _MENU = ['--propagate', 'blockdev', 'add']
    _POOLNAME = 'deadpool'


    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testAdd(self):
        """
        Adding the devices must fail since the pool does not exist.
        """
        command_line = self._MENU + [self._POOLNAME] \
            + _DEVICE_STRATEGY.example()
        with self.assertRaises(StratisCliDbusLookupError):
            RUNNER(command_line)


@unittest.skip("Can't test this because not modeling ownership of devs.")
class Add2TestCase(unittest.TestCase):
    """
    Test adding devices in an existing pool when the devices are already in the
    pool. There are circumstances under which this should fail, and others under
    which this should succeed.
    """
    _MENU = ['--propagate', 'blockdev', 'add']
    _POOLNAME = 'deadpool'
    _DEVICES = _DEVICE_STRATEGY.example()

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        command_line = ['pool', 'create', self._POOLNAME] + self._DEVICES
        RUNNER(command_line)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testAdd(self):
        """
        Adding devices that are already there should succeed if devices are
        unused by pool, but should fail otherwise.
        """
        command_line = self._MENU + [self._POOLNAME] + self._DEVICES
        RUNNER(command_line)

@unittest.skip('Not able to track if devices are in use.')
class Add3TestCase(unittest.TestCase):
    """
    Test adding devices to an existing pool, when the devices are not in the
    pool. This should fail if the devices are already occupied.
    """
    _MENU = ['--propagate', 'blockdev', 'add']
    _POOLNAME = 'deadpool'
    _DEVICES = _device_list(2).example()

    def setUp(self):
        """
        Start the stratisd daemon with the simulator.
        """
        self._service = Service()
        self._service.setUp()
        time.sleep(1)
        command_line = ['pool', 'create'] + [self._POOLNAME] + self._DEVICES[:1]
        RUNNER(command_line)

    def tearDown(self):
        """
        Stop the stratisd simulator and daemon.
        """
        self._service.tearDown()

    def testAdd(self):
        """
        Adding devices that are not already there should succeed if devices are
        unused by others, but should fail otherwise.
        """
        command_line = self._MENU + [self._POOLNAME] + self._DEVICES[1:]
        RUNNER(command_line)
