# -*- coding: utf-8 -*-


def main():
    """
    This is the main entrypoint for the application.

    It is designed to handle:
     - cli argument parsing via docopt
     - setup logging across the application.
     - start the main application logic

    This should allways be the first file in this package to be imported
     otherwise setup of logging can fail and cause unwanted behaviour.
    """
    import djinja
    from docopt import docopt

    __docopt__ = """
    Usage:
      dj -d DOCKERFILE -o OUTFILE [-s DSFILE]... [-e ENV]... [-c CONFIGFILE]
         [-v ...] [-q] [-h] [--version]

    Options:
      -c CONFIGFILE --config CONFIGFILE       file containing global config for dj
      -s DSFILE --datasource DSFILE           file that should be loaded as a datasource
      -d DOCKERFILE --dockerfile DOCKERFILE   dockerfile to render
      -e ENV --env ENV                        variable with form "key=value" that should be used in the rendering
      -o OUTFILE --outfile OUTFILE            output result to file
      -h --help                               show this help
      -v --verbosity                          verbosity level of logging messages. ( -v == CRITICAL )  ( -vvvvv == DEBUG )
      -V --version                            display the version number and exit
      -q --quiet                              silence all logging output no matter what
        """

    args = docopt(__docopt__, version=djinja.__version__)

    djinja.init_logging(1 if args["--quiet"] else args["--verbosity"])

    # Import rest of application so logging will work for them correctely
    import djinja.main
    c = djinja.main.Core(args)
    c.main()
    return c
