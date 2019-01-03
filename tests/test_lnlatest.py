import os
from unittest import TestCase

from lnlatest import TEST_ARGS_STRING, TEST_LINK_NAME, TEST_ROOT_DIR_PATH, TEST_SUB_DIR_PATTERN, create_link, \
    get_arg_parser, get_create_link_command_list, get_dir_latest, get_dir_list, \
    verify_safe_link_path, is_admin


class TestLnLatest(TestCase):
    def test_is_admin(self):
        print(is_admin())

    def test_get_dir_list(self):
        print(get_dir_list(TEST_ROOT_DIR_PATH, TEST_SUB_DIR_PATTERN))

    def test_get_dir_latest(self):
        print(get_dir_latest(TEST_ROOT_DIR_PATH, TEST_SUB_DIR_PATTERN))

    def test_get_create_link_command_list(self):
        print(get_create_link_command_list(TEST_ROOT_DIR_PATH, TEST_SUB_DIR_PATTERN, TEST_LINK_NAME))

    def test_create_link(self):
        print(create_link(TEST_ROOT_DIR_PATH, TEST_SUB_DIR_PATTERN, TEST_LINK_NAME))

    def test_get_arg_parser(self):
        parser = get_arg_parser()
        args = parser.parse_args(TEST_ARGS_STRING.split())
        print(args)

    def test_verify_safe_link_path(self):
        link_path = os.path.join(TEST_ROOT_DIR_PATH, TEST_LINK_NAME)
        print(verify_safe_link_path(link_path, erase_old_link=False))
