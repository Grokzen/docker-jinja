# -*- coding: utf-8 -*-

# python std lib
import sys

# djinja package imports
from djinja import cli


class TestCLI(object):

    def test_cli(self, tmpdir):
        """
        Test that when passing in certain arguments from commandline they
        are handled correctly by docopt and that the method creates a Core object
        and runs main method and the args dict passed in have correct format
        """
        input = tmpdir.join("Dockerfile.jinja")
        input.write("foobar")
        output = tmpdir.join("Dockerfile")
        dsfile = tmpdir.join("datasource.py")
        dsfile.write("#")

        sys.argv = [
            'scripts/dj',
            '-d', str(input),
            '-o', str(output),
            '-e', 'OS=ubuntu:12.04',
            '-s', str(dsfile),
            '-vvvvv'
        ]

        expected = {
            '--dockerfile': str(input),
            '--env': ['OS=ubuntu:12.04'],
            '--help': False,
            '--outfile': str(output),
            '--quiet': False,
            '--verbosity': 5,
            '--version': False
        }

        c = cli.main()

        for k, v in expected.items():
            assert k in c.args

        assert str(dsfile) in c.args["--datasource"]
