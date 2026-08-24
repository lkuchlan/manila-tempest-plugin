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


class QosTypeSpecsAdminNegativeTest(base.BaseSharesMixedTest):

    @classmethod
    def skip_checks(cls):
        super(QosTypeSpecsAdminNegativeTest, cls).skip_checks()
        utils.check_skip_if_microversion_not_supported(
            constants.QOS_TYPE_VERSION)

    @classmethod
    def resource_setup(cls):
        super(QosTypeSpecsAdminNegativeTest, cls).resource_setup()
        cls.specs = {"key": "value"}

    @decorators.idempotent_id('9ac9df0c-faaa-4680-8726-1365ee0ccd3c')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_create_specs_with_user(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.Forbidden,
            self.shares_v2_client.create_qos_type_specs,
            qos_type["id"],
            {"key": "new_value"})

    @decorators.idempotent_id('9c7ffa08-62e9-43c1-a7a0-4d31f28b1a53')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_update_spec_with_user(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.Forbidden,
            self.shares_v2_client.update_qos_type_spec,
            qos_type["id"], "key", "new_value")

    @decorators.idempotent_id('8bc1f291-cce3-4c67-b82d-fc6d07ea3764')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_delete_specs_with_user(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.Forbidden,
            self.shares_v2_client.delete_qos_type_spec,
            qos_type["id"], "key")

    @decorators.idempotent_id('7e744f35-02b3-43dc-8dd0-0dec443e7a26')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_set_too_long_key(self):
        too_big_key = "k" * 256
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.BadRequest,
            self.admin_shares_v2_client.create_qos_type_specs,
            qos_type["id"],
            {too_big_key: "value"})

    @decorators.idempotent_id('2d1a5327-ae5f-47b1-9ae4-90c3d26bcc10')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_set_too_long_value_with_creation(self):
        too_big_value = "v" * 1024
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.BadRequest,
            self.admin_shares_v2_client.create_qos_type_specs,
            qos_type["id"],
            {"key": too_big_value})

    @decorators.idempotent_id('b60aa991-0253-4af2-8e85-fe856b7514d3')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_set_too_long_value_with_update(self):
        too_big_value = "v" * 1024
        qos_type = self.create_qos_type(specs=self.specs)
        self.admin_shares_v2_client.create_qos_type_specs(
            qos_type["id"],
            {"key": "value"})
        self.assertRaises(
            lib_exc.BadRequest,
            self.admin_shares_v2_client.update_qos_type_spec,
            qos_type["id"],
            "key",
            too_big_value)

    @decorators.idempotent_id('2b59b2c2-b3ae-442c-8ee3-708fdbd9e496')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_list_spec_with_invalid_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type_specs,
            "fake_qos_type_id")

    @decorators.idempotent_id('3282a0cb-60bc-46ac-9ed2-5414f879d72e')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_create_spec_with_empty_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.create_qos_type_specs,
            "", {"key1": "value1"})

    @decorators.idempotent_id('c11b0bda-d0f5-4bde-90fd-0e2314923d27')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_create_spec_with_invalid_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.create_qos_type_specs,
            data_utils.rand_name("fake"), {"key1": "value1", })

    @decorators.idempotent_id('dc6d2f11-223b-47a6-ad28-cb586e9cbf34')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_create_spec_with_invalid_specs(self):
        qos_type = self.create_qos_type()
        self.assertRaises(
            lib_exc.BadRequest,
            self.admin_shares_v2_client.create_qos_type_specs,
            qos_type["id"], {"": "value_with_empty_key"})

    @decorators.idempotent_id('a6288784-db9a-4617-831e-974b5a832201')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_get_spec_with_empty_key(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type_spec,
            qos_type["id"], "")

    @decorators.idempotent_id('3eae0a8d-5482-4ba7-aecd-c75ee9fd026b')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_get_spec_with_invalid_key(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type_spec,
            qos_type["id"], data_utils.rand_name("fake"))

    @decorators.idempotent_id('a5e939fb-4b58-4b88-8786-9898defb50e6')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_get_specs_with_empty_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type_specs,
            "")

    @decorators.idempotent_id('dadf0f8b-75cc-446a-abc3-048f148a435d')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_get_specs_with_invalid_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.get_qos_type_specs,
            data_utils.rand_name("fake"))

    @decorators.idempotent_id('81013350-1e4d-49ab-9a3d-3852c3595956')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_delete_spec_key_with_empty_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.delete_qos_type_spec,
            "", "key", )

    @decorators.idempotent_id('370722b6-17cd-4e14-bf0e-90513e73cf15')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_delete_spec_key_with_invalid_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.delete_qos_type_spec,
            data_utils.rand_name("fake"), "key", )

    @decorators.idempotent_id('726b24be-f387-4f4d-9c25-53854ddad31f')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_delete_with_invalid_key(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.delete_qos_type_spec,
            qos_type["id"], data_utils.rand_name("fake"))

    @decorators.idempotent_id('687ffcac-d7d5-4f54-a7b4-46935b7507a8')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_update_spec_with_empty_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.update_qos_type_spec,
            "", "key", "new_value")

    @decorators.idempotent_id('d19b5fca-3b96-44ef-a1d6-20671186db45')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_update_spec_with_invalid_qos_type_id(self):
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.update_qos_type_spec,
            data_utils.rand_name("fake"), "key", "new_value")

    @decorators.idempotent_id('a55c50db-f49b-4639-aff4-1ec8ee77de97')
    @tc.attr(base.TAG_NEGATIVE, base.TAG_API)
    def test_try_update_spec_with_empty_key(self):
        qos_type = self.create_qos_type(specs=self.specs)
        self.assertRaises(
            lib_exc.NotFound,
            self.admin_shares_v2_client.update_qos_type_spec,
            qos_type["id"], "", "new_value")
