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
from tempest.lib import decorators
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils


CONF = config.CONF
LATEST_MICROVERSION = CONF.share.max_api_microversion


class QosTypeSpecsAdminTest(base.BaseSharesAdminTest):

    @classmethod
    def skip_checks(cls):
        super(QosTypeSpecsAdminTest, cls).skip_checks()
        utils.check_skip_if_microversion_not_supported(
            constants.QOS_TYPE_VERSION)

    @classmethod
    def resource_setup(cls):
        super(QosTypeSpecsAdminTest, cls).resource_setup()
        cls.specs = {"key1": "value1", "key2": "value2"}

    @decorators.idempotent_id('1606a3f8-514f-4b6a-9bb0-d16ab90d23c5')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_get_one_qos_type_spec(self):
        qos_type = self.create_qos_type()
        self.admin_shares_v2_client.create_qos_type_specs(
            qos_type['id'], self.specs)

        spec_get_one = self.admin_shares_v2_client.get_qos_type_spec(
            qos_type['id'], "key1")

        self.assertEqual({"key1": self.specs["key1"]}, spec_get_one)

    @decorators.idempotent_id('90f1ea8f-9c9e-4c09-858c-52d9757eebb9')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_get_all_qos_type_specs(self):
        qos_type = self.create_qos_type()
        self.admin_shares_v2_client.create_qos_type_specs(
            qos_type['id'], self.specs)

        spec_get_all = self.admin_shares_v2_client.get_qos_type_specs(
            qos_type['id'])['specs']

        self.assertEqual(self.specs, spec_get_all)

    @decorators.idempotent_id('d3d0e841-d00d-41aa-b7da-83c8f0ca182c')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_update_qos_type_spec(self):
        qos_type = self.create_qos_type()
        self.admin_shares_v2_client.create_qos_type_specs(
            qos_type['id'], self.specs)

        updated_specs = dict(self.specs)
        updated_specs["key1"] = "fake_value1_updated"

        # Update spec of qos type
        update_one = self.admin_shares_v2_client.update_qos_type_spec(
            qos_type['id'], "key1", updated_specs["key1"])
        self.assertEqual({"key1": updated_specs["key1"]}, update_one)

        get = self.admin_shares_v2_client.get_qos_type_specs(
            qos_type['id'])['specs']
        self.assertEqual(updated_specs, get)

    @decorators.idempotent_id('1db3ff90-7263-434d-892f-4d28d7e6ac56')
    @tc.attr(base.TAG_POSITIVE, base.TAG_API)
    def test_delete_one_qos_type_spec(self):
        qos_type = self.create_qos_type()
        self.admin_shares_v2_client.create_qos_type_specs(
            qos_type['id'], self.specs)

        # Delete one spec for qos type
        self.admin_shares_v2_client.delete_qos_type_spec(
            qos_type['id'], "key1")

        get = self.admin_shares_v2_client.get_qos_type_specs(
            qos_type['id'])['specs']
        self.assertNotIn('key1', get)
