# Copyright (c) 2013 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from savanna.plugins.general import exceptions as g_ex
from savanna.plugins.intel import plugin as p
from savanna.plugins.intel.v3_0_2 import config_helper as c_helper
from savanna.tests.unit import base
from savanna.tests.unit import testutils as tu


class TestIDHPlugin302(base.SaharaWithDbTestCase):

    def test_get_configs(self):
        plugin = p.IDHProvider()
        configs = plugin.get_configs('3.0.2')

        self.assertIn(c_helper.IDH_REPO_URL, configs)
        self.assertIn(c_helper.IDH_TARBALL_URL, configs)
        self.assertIn(c_helper.OS_REPO_URL, configs)

    def test_validate(self):
        plugin = p.IDHProvider()

        ng_mng = tu.make_ng_dict('mng', 'f1', ['manager'], 1)
        ng_nn = tu.make_ng_dict('nn', 'f1', ['namenode'], 1)
        ng_rm = tu.make_ng_dict('rm', 'f1', ['resourcemanager'], 1)
        ng_dn = tu.make_ng_dict('dn', 'f1', ['datanode'], 2)
        ng_nm = tu.make_ng_dict('nm', 'f1', ['nodemanager'], 2)

        cl = tu.create_cluster('cl1', 't1', 'intel', '3.0.2',
                               [ng_nn] + [ng_dn])
        self.assertRaises(g_ex.InvalidComponentCountException,
                          plugin.validate, cl)

        cl = tu.create_cluster('cl1', 't1', 'intel', '3.0.2', [ng_mng])
        self.assertRaises(g_ex.InvalidComponentCountException,
                          plugin.validate, cl)

        cl = tu.create_cluster('cl1', 't1', 'intel', '3.0.2',
                               [ng_mng] + [ng_nn] * 2)
        self.assertRaises(g_ex.InvalidComponentCountException,
                          plugin.validate, cl)

        cl = tu.create_cluster('cl1', 't1', 'intel', '3.0.2',
                               [ng_mng] + [ng_nn] + [ng_nm])
        self.assertRaises(g_ex.RequiredServiceMissingException,
                          plugin.validate, cl)

        cl = tu.create_cluster('cl1', 't1', 'intel', '3.0.2',
                               [ng_mng] + [ng_nn] + [ng_rm] * 2 + [ng_rm])
        self.assertRaises(g_ex.InvalidComponentCountException,
                          plugin.validate, cl)
