# Copyright 2026 Cloudification GmbH
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc
import testtools

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils

tc = testtools.testcase
CONF = config.CONF


class QosTypesTest(base.BaseSharesAdminTest):

    @classmethod
    def skip_checks(cls):
        super(QosTypesTest, cls).skip_checks()
        utils.check_skip_if_microversion_not_supported(
            constants.QOS_TYPE_VERSION)

    @decorators.idempotent_id('83a65d3e-550d-4967-a0b6-0d403f0fb592')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_qos_type_create_delete(self):
        specs = {
            "policy_type": 'adaptive',
            "peak_iops": '1000',
            "expected_iops": '200',
        }
        qos_type = self.create_qos_type(
            data_utils.rand_name('GOLD'),
            cleanup_in_class=False,
            specs=specs,
            client=self.admin_shares_v2_client)
        self.assertEqual(
            'adaptive', qos_type['specs']['policy_type'])
        self.assertIsNone(qos_type['description'])

        # update description
        self.admin_shares_v2_client.update_qos_type(
            qos_type['id'], description="test_description")
        qos_type = self.admin_shares_v2_client.get_qos_type(
            qos_type['id'])['qos_type']
        self.assertEqual('adaptive', qos_type['specs']['policy_type'])
        self.assertEqual('test_description', qos_type['description'])

        # delete qos_type
        self.admin_shares_v2_client.delete_qos_type(qos_type["id"])
        self.admin_shares_v2_client.wait_for_resource_deletion(
            qos_type_id=qos_type["id"])
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type, qos_type['id'])
