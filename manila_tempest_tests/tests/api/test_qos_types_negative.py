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
from testtools import testcase as tc

from manila_tempest_tests.common import constants
from manila_tempest_tests.tests.api import base
from manila_tempest_tests import utils


CONF = config.CONF


class QosTypesNegativeTest(base.BaseSharesMixedTest):

    @classmethod
    def skip_checks(cls):
        super(QosTypesNegativeTest, cls).skip_checks()
        utils.check_skip_if_microversion_not_supported(
            constants.QOS_TYPE_VERSION)

    @classmethod
    def resource_setup(cls):
        super(QosTypesNegativeTest, cls).resource_setup()
        extra_specs = {'default_qos_type': 'qos_type_negative_test'}
        cls.share_type = cls.create_share_type(extra_specs=extra_specs)
        cls.share_type_id = cls.share_type['id']

    @decorators.idempotent_id('e6a6ac4d-6582-408d-ba55-6f5128eb940e')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_create_qos_type_with_nonadmin_user(self):
        self.assertRaises(lib_exc.Forbidden,
                          self.create_qos_type,
                          name=data_utils.rand_name("used_user_creds"),
                          client=self.alt_shares_v2_client)

    @decorators.idempotent_id('2193465a-ed8e-44d5-9ca9-4e8a3c5958f0')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_qos_type_create_with_same_name(self):
        specs = {
            "policy_type": 'adaptive',
            "peak_iops": '1000',
            "expected_iops": '200',
        }
        name = data_utils.rand_name('GOLD')
        self.create_qos_type(
            name=name,
            specs=specs,
            client=self.admin_shares_v2_client)

        self.assertRaises(lib_exc.Conflict,
                          self.create_qos_type,
                          name=name,
                          specs={},
                          client=self.admin_shares_v2_client)

    @decorators.idempotent_id('f962c88c-e4f7-4d37-8449-e3faf8e30a4a')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_share_create_with_invalid_share_type_extra_specs(self):
        self.assertRaises(lib_exc.BadRequest,
                          self.create_share,
                          size=1,
                          share_type_id=self.share_type_id)
