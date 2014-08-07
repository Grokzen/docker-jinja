# -*- coding: utf-8 -*-

# python std lib
import logging

# djinja package imports
import djinja
from djinja import _local_env
from djinja.main import Core
from djinja.conftree import ConfTree

# 3rd party imports
import pytest
from jinja2 import Template
from testfixtures import LogCapture


class TestCore(object):

    def test_create_obj(self):
        """
        Create empty object and ensure defaults is set correctly
        """
        c = Core({})
        assert c.args == {}

        # Test that loading all default config files works
        ct = ConfTree(c.default_config_files)
        assert ct.tree == c.config.get_tree()

    def test_parse_env_vars(self):
        """
        Test setting env variables from cli and ensure they are set
        correctly in configuration.
        """
        c = Core({
            "--env": [
                "foo=bar",
                "opa=1",
                "barfoo=True",
            ]
        })

        c.parse_env_vars()
        assert c.config.get("foo") == "bar"
        assert c.config.get("opa") == "1"
        assert c.config.get("barfoo") == "True"

    def test_parse_env_vars_invalid_key(self):
        """
        Test that invalid keyformats cause exceptions
        """
        # specify a key that do not follow the key=value structures
        c = Core({
            "--env": [
                "foo:bar"
            ]
        })
        with pytest.raises(Exception) as ex:
            c.parse_env_vars()
        # TODO: str() maybe not py2 & 3 compatible. Look into unicode in from redis._compat
        assert str(ex.value).startswith("var 'foo:bar' is not of format 'key=value'")

        c = Core({
            "--env": [
                "foo="
            ]
        })
        with pytest.raises(Exception) as ex:
            c.parse_env_vars()
        # TODO: str() maybe not py2 & 3 compatible. Look into unicode in from redis._compat
        assert str(ex.value).startswith("var 'foo=' is not of format 'key=value'")

        c = Core({
            "--env": [
                "=bar"
            ]
        })
        with pytest.raises(Exception) as ex:
            c.parse_env_vars()
        # TODO: str() maybe not py2 & 3 compatible. Look into unicode in from redis._compat
        assert str(ex.value).startswith("var '=bar' is not of format 'key=value'")

    def test_parse_no_env_vars(self):
        """
        Test that if no env variables is specefied none should be loaded
        """
        c = Core({})
        c.parse_env_vars()
        assert c.config.get_tree().get("env", {}) == {}

    def test_load_user_specefied_config_file(self, tmpdir):
        """
        Test that loadinloading of config file that user specefies work
        and that config keys is set correctly.
        """
        f = tmpdir.join("empty.json")
        f.write('{"foo": "bar"}')

        c = Core({
            "--config": str(f)
        })
        c.load_user_specefied_config_file()
        assert c.config.get_tree() == {"foo": "bar"}

    def test_load_no_user_specefied_config_file(self):
        """
        Test that not loading a user specefied config file works
        """
        c = Core({})
        c.load_user_specefied_config_file()
        assert c.config.get_tree() == {}

    def test_load_user_specefied_config_file_wrong_format(self, tmpdir):
        """
        Config data is a dict at top level and loading something else should raise error
        """
        f = tmpdir.join("empty.json")
        f.write('["foo", "bar"]')
        c = Core({
            "--config": str(f)
        })
        with pytest.raises(Exception) as ex:
            c.load_user_specefied_config_file()
        assert str(ex.value).startswith("Data tree to merge must be of dict type")

    def test_handle_datasources(self, tmpdir):
        """
        Test that loading of datasources work and that they are usable.
        """
        input = tmpdir.join("Dockerfile.jinja")
        input.write("{{ 'foo'|upper }} : {{ lower('BAR') }}")

        output = tmpdir.join("Dockerfile")
        dsfile = tmpdir.join("_datasource.py")
        dsfile.write("""
def _filter_upper(string):
    return string.upper()

def _global_lower(string):
    return string.lower()
        """)

        c = Core({
            "--dockerfile": str(input),
            "--outfile": str(output),
            "--datasource": [str(dsfile)]
        })
        c.main()
        assert output.read() == "FOO : bar"

    def test_fail_load_non_existing_datasource(self, tmpdir):
        """
        Prove a path to a datasource that do not exists and try to load it
        and look for exception to be raised.
        """
        input = tmpdir.join("Dockerfile.jinja")
        output = tmpdir.join("Dockerfile")
        c = Core({
            "--dockerfile": str(input),
            "--outfile": str(output),
            "--datasource": ["/tmp/foobar/barfoo"]
        })
        with pytest.raises(Exception) as ex:
            c.main()
        assert str(ex.value).startswith("Unable to load datasource file : /tmp/foobar/barfoo")

    def test_load_datasource_import_error(self, tmpdir):
        """
        Provide a datasource file that will raise ImportError. Ensure log msg
        and that exception was raised.

        We fake the ImportError exception by manually raising it from inside
        the datasource file to make it consistent.
        """
        input = tmpdir.join("Dockerfile.jinja")
        input.write("foobar")
        output = tmpdir.join("Dockerfile")
        dsfile = tmpdir.join("_datasource_.py")
        dsfile.write("""
raise ImportError("foobar")
        """)
        c = Core({
            "--dockerfile": str(input),
            "--outfile": str(output),
            "--datasource": [str(dsfile)]
        })
        with pytest.raises(ImportError):
            c.main()

    def test_process_dockerfile(self, tmpdir):
        """
        """
        input = tmpdir.join("Dockerfile.jinja")
        input.write("{{ barfoo }}")
        o = tmpdir.join("Dockerfile")
        c = tmpdir.join("conf.json")
        c.write('{"env": {"barfoo": "foobar"}}')

        c = Core({
            "--dockerfile": str(input),
            "--outfile": str(o),
            "--config": str(c),
        })

        c.load_user_specefied_config_file()
        c.parse_env_vars()
        c.handle_data_sources()
        c.process_dockerfile()

        assert o.read() == "foobar"

    def test_process_dockerfile_no_env(self, tmpdir):
        """
        Found a bug before that if parse_env_vars() is not used before
         process_dockerfile() then it will throw exception, but it should not do that
        """
        pass

    def test_process_dockerfile_no_output_file_specefied(self, tmpdir):
        """
        Found a bug that if no --outfile is specefied it will not work and throw exception
         that it should not do...
        """
        input = tmpdir.join("Dockerfile.jinja")
        input.write("{{ barfoo }}")
        c = tmpdir.join("conf.json")
        c.write('{"env": {"barfoo": "foobar"}}')

        c = Core({
            "--dockerfile": str(input),
            "--config": str(c),
        })

        with pytest.raises(Exception) as ex:
            c.load_user_specefied_config_file()
            c.parse_env_vars()
            c.handle_data_sources()
            c.process_dockerfile()

        assert str(ex.value).startswith("missing key '--outfile' in cli_args. Could not write to output file.")

    def test__attach_function(self):
        """
        Test that it works to attach a function to the global namespace that
        jinja will later use.
        """
        global _local_env

        c = Core({})

        def foo_func():
            pass
        c._attach_function("globals", foo_func, "func")
        assert "func" in _local_env["globals"]
        assert _local_env["globals"]["func"] == foo_func

        # Test that exception is raised if we try to attach to wrong jinja namespace
        with pytest.raises(KeyError) as ex:
            c._attach_function("foobar", foo_func, "func")
        assert str(ex.value).startswith("'foobar'")

        # TODO: Test that if you attach the same function twice to the same namespace
        #       it should fail with some exception

    def test__update_env(self, tmpdir):
        """
        """
        global _local_env

        i = tmpdir.join("Dockerfile.jinja")
        i.write("{{ func() }}")
        o = tmpdir.join("Dockerfile")

        c = Core({
            "--dockerfile": str(i),
            "--outfile": str(o),
        })

        def foo_func():
            return "foobar"
        c._attach_function("globals", foo_func, "func")

        template = Template(i.read())
        c._update_env(template.environment)
        rendered_template = template.render()
        assert rendered_template == "foobar"

    def test_main(self, tmpdir):
        """
        Test that the main methos is callable and use as many things as possible
        to verify as much as possible works in the main flow.
        """
        # TODO: Add datasource support
        # TODO: Add default config data files
        input = tmpdir.join("Dockerfile.jinja")
        input.write("{{ myvar }}")
        o = tmpdir.join("Dockerfile")
        c = tmpdir.join("conf.json")
        c.write('{"env": {"myvar": "foobar"}}')

        c = Core({
            "--dockerfile": str(input),
            "--outfile": str(o),
            "--config": str(c),
        })

        c.main()
        assert o.read() == "foobar"

    def test_debug_logging(self):
        """
        Test that if -vvvvv is passed into docopt and debug logging will output.
        """
        djinja.init_logging(5)
        Log = logging.getLogger("foobar")
        with LogCapture() as l:
            Log.debug("barfoo")
        l.check(("foobar", "DEBUG", "barfoo"))
