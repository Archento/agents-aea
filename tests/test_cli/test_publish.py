# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Test module for Registry publish methods."""

from unittest import TestCase, mock

from click import ClickException

from aea.cli.publish import (
    _check_is_item_in_local_registry,
    _save_agent_locally
)

from tests.test_cli.tools_for_testing import ContextMock, PublicIdMock


@mock.patch("aea.cli.publish._check_is_item_in_local_registry")
@mock.patch("aea.cli.publish.copyfile")
@mock.patch("aea.cli.publish.os.makedirs")
@mock.patch("aea.cli.publish.os.path.exists", return_value=False)
@mock.patch("aea.cli.publish.try_get_item_target_path", return_value="target-dir")
@mock.patch("aea.cli.publish.os.path.join", return_value="joined-path")
class SaveAgentLocallyTestCase(TestCase):
    """Test case for _save_agent_locally method."""

    def test_save_agent_locally_positive(
        self,
        path_join_mock,
        try_get_item_target_path_mock,
        path_exists_mock,
        makedirs_mock,
        copyfile_mock,
        _check_is_item_in_local_registry_mock
    ):
        """Test for save_agent_locally positive result."""
        _save_agent_locally(ContextMock())
        makedirs_mock.assert_called_once_with("target-dir", exist_ok=True)
        copyfile_mock.assert_called_once_with("joined-path", "joined-path")


def _raise_click_exception(*args):
    raise ClickException('Message')


class CheckIsItemInLocalRegistryTestCase(TestCase):
    """Test case for _check_is_item_in_local_registry method."""

    @mock.patch("aea.cli.publish.try_get_item_source_path")
    def test__check_is_item_in_local_registry_positive(self, get_path_mock):
        """Test for _check_is_item_in_local_registry positive result."""
        public_id = PublicIdMock.from_str('author/name:version')
        registry_path = 'some-registry-path'
        item_type_plural = 'items'
        _check_is_item_in_local_registry(
            public_id, item_type_plural, registry_path
        )
        get_path_mock.assert_called_once_with(
            registry_path, public_id.author, item_type_plural, public_id.name
        )

    @mock.patch(
        "aea.cli.publish.try_get_item_source_path", _raise_click_exception
    )
    def test__check_is_item_in_local_registry_negative(self):
        """Test for _check_is_item_in_local_registry negative result."""
        public_id = PublicIdMock.from_str('author/name:version')
        registry_path = 'some-registry-path'
        item_type_plural = 'items'
        with self.assertRaises(ClickException):
            _check_is_item_in_local_registry(
                public_id, item_type_plural, registry_path
            )
