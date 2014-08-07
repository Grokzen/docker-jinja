# -*- coding: utf-8 -*-

# djinja package imports
from djinja.conftree import ConfTree

# 3rd party imports
import pytest


class TestConfTree(object):

    def test_create_obj(self):
        """
        Test that creating a ConfTree object works and sets default values for internal variables.
        """
        c = ConfTree()
        assert c.config_files == []
        assert c.tree == {}

        # Only lists are allowed to be passed in
        with pytest.raises(Exception) as ex:
            c = ConfTree(config_files={"foo": "bar"})
        assert str(ex.value).startswith("config files must be a list of items that can be read from FS")

    def test_store_config_files(self):
        """
        Initial specefied config files should be stored internally in ConfTree object
        """
        dummy_files = ["/foo/bar"]
        c = ConfTree(config_files=dummy_files)
        assert c.config_files, dummy_files

    def test_load_file_not_exists(self):
        """
        Test to load a file that do not exists on the system
        """
        dummy_files = ["/tmp/foobar/opalopa"]
        c = ConfTree(config_files=dummy_files)
        with pytest.raises(Exception):
            c.load_config_file()

    def test_load_empty_file(self, tmpdir):
        """
        Test that when loading a file with no content it will raise exception
        """
        f = tmpdir.join("empty.json")
        f.write("")
        assert f.read() == ""

        with pytest.raises(Exception):
            c = ConfTree()
            c.load_config_file(str(f))

    def test_load_xml_file(self, tmpdir):
        """
        This will test that exception is raised when file contains something
         but it is not a supported datatype. For example XML.
        """
        f = tmpdir.join("xml.json")
        f.write("<b>foo</b>")

        with pytest.raises(Exception):
            c = ConfTree()
            c.load_config_file(str(f))

    def test_merge_data_tree(self):
        """
        Test that merging of 2 data tree:s work
        """
        c = ConfTree()
        c.tree = {"foo": True}
        c.merge_data_tree({"bar": False})
        assert c.tree == {"foo": True, "bar": False}

    def test_merge_data_tree_not_dict(self):
        """
        Exception should be raised if trying to merge a object that is not a dict
        """
        c = ConfTree()
        with pytest.raises(Exception):
            c.merge_data_tree([])

    def test_get_tree(self):
        """
        Method 'get_tree()' should return the entire data tree
        """
        c = ConfTree()
        c.tree = {"foo": True}
        assert c.get_tree() == {"foo": True}

    def test_get(self):
        """
        Test that 'get()' returns correct data
        """
        c = ConfTree()
        c.tree = {
            "foo": True,
            "bar": 1,
            "qwe": "rty"
        }

        assert c.get("foo", False) is True
        assert c.get("bar", -1) == 1
        assert c.get("qwe", "ytr") == "rty"
        assert c.get("foobar", "barfoo") == "barfoo"
