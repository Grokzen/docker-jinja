# -*- coding: utf-8 -*-

# python std lib
import os
import yaml
import json
import logging

Log = logging.getLogger(__name__)


class ConfTree(object):

    def __init__(self, config_files=None):
        self.config_files = config_files if config_files else []
        if not isinstance(self.config_files, list):
            raise Exception("config files must be a list of items that can be read from FS")
        self.tree = {}

    def load_config_files(self):
        for config_file in self.config_files:
            try:
                self.load_config_file(config_file)
            except Exception:
                Log.debug("unable to load default config file : {}".format(config_file))
                pass

    def load_config_file(self, config_file):
        if not os.path.exists(config_file):
            raise Exception("Path to config file do not exists on disk...")

        with open(config_file, "r") as stream:
            data = stream.read()

        if not data:
            raise Exception("No data in config file : {}".format(config_file))

        # Try first with yaml as that is default config lagn
        # If yaml loading failed then try json loading
        try:
            data_tree = yaml.loads(data)
        except Exception:
            try:
                data_tree = json.loads(data)
            except Exception:
                raise Exception("Unable to load data as yaml or json from config file : {}".format(config_file))

        Log.debug("Loading default data from default config file : {}".format(config_file))

        # If data was loaded into python datastructure then load it into the config tree
        self.merge_data_tree(data_tree)

    def merge_data_tree(self, data_tree):
        if not isinstance(data_tree, dict):
            raise Exception("Data tree to merge must be of dict type")

        self.tree.update(data_tree)

    def get_tree(self):
        return self.tree

    def get(self, key, default=None):
        return self.tree.get(key, default)
