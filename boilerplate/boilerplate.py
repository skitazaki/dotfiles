#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Shigeru Kitazaki
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Simple command line script.
TODO: Write description on your own.
"""

import argparse
import configparser
import json
import logging
import logging.config
import os
import sys
import traceback

__version__ = '0.1.0'
__author__ = 'Shigeru Kitazaki'

APPNAME = os.path.splitext(os.path.basename(__file__))[0]
BASEDIR = os.path.dirname(os.path.abspath(__file__))

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(levelname)s] %(name)s '
                      '%(filename)s:L%(lineno)-4d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stderr',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': APPNAME + '.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        APPNAME: {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': False
        }
    }
})

DEFUALT_INPUT_FILE_ENCODING = 'utf8'


def parse_arguments():
    """Parse arguments and set up logging verbosity.

    :rtype: parsed arguments as Namespace object.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-c', '--config', dest='config',
                        help='configuration file', metavar='FILE')
    parser.add_argument('-o', '--output', dest='output',
                        help='output path', metavar='FILE')
    parser.add_argument('-n', '--dryrun', dest='dryrun',
                        help='dry run', default=False, action='store_true')
    parser.add_argument('-e', '--encoding', dest='encoding',
                        help='input file encoding',
                        default=DEFUALT_INPUT_FILE_ENCODING)
    parser.add_argument('-E', '--output-encoding', dest='encoding_out',
                        help='output file encoding',
                        default=DEFUALT_INPUT_FILE_ENCODING)
    parser.add_argument('files', nargs='*',
                        help='input files', metavar='FILE')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-v', '--verbose', dest='verbose',
                       action='count', default=0,
                       help='increase logging verbosity')

    group.add_argument('-q', '--quiet', dest='quiet',
                       default=False, action='store_true',
                       help='set logging to quiet mode')

    try:
        args = parser.parse_args()
    except IOError:
        e = sys.exc_info()[1]
        parser.error('File not found: %s' % (e, ))

    # Set up logging verbosity level.
    logger = logging.getLogger(APPNAME)
    if args.quiet:
        logger.setLevel(logging.CRITICAL)
    elif args.verbose >= 3:
        logger.setLevel(logging.DEBUG)
    elif args.verbose >= 2:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 1:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.ERROR)

    return args


class ConfigLoader(object):
    """Configuration file loader to support multiple file types.

    Supported file types are:
    * ini/cfg
    * json

    :param fp: file pointer to load
    :param filetype: either of 'ini|cfg', 'json', or 'yml|yaml' file.
        If nothing specified, detect by file extension automatically.
    """

    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(APPNAME + '.config')

    def _load(self, extension):
        self.logger.debug('Config file extension is "%s".', extension)
        if extension == '.json':
            with open(self.path) as fp:
                return json.load(fp)
        elif extension in (".ini", ".cfg"):
            parser = configparser.SafeConfigParser()
            with open(self.path) as fp:
                parser.readfp(fp)
            config = {}
            for s in parser.sections():
                config[s] = dict(parser.items(s))
            return config
        else:
            self.logger.warn('Unknown file type extension: %s', extension)

    def load(self, env=None):
        """ Load a section values of given environment.
        If nothing to specified, use environmental variable.
        If unknown environment was specified, warn it on logger.
        :param env: environment key to load in a coercive manner
        :type env: string
        :rtype: dict
        """
        self.logger.debug('Loading config "%s" ...', self.path)
        ext = os.path.splitext(self.path)[-1].lower()
        if len(ext) == 0:
            self.logger.warn("Missing file extension: %s", self.path)
            return
        elif not ext.startswith('.'):
            self.logger.warn("Extension doesn't start with dot: %s", self.path)
            return
        return self._load(ext)


class MainProcess(object):

    """Main process class.
    # TODO: Implement your logic.
    """

    def __init__(self, dryrun):
        self.dryrun = dryrun
        self.logger = logging.getLogger(APPNAME + '.main')

    def configure(self, configfile):
        loader = ConfigLoader(configfile)
        config = loader.load()
        for k in sorted(config):
            self.logger.debug('config key: %s', k)
        # TODO: Implement your logic.

    def process(self, files, encoding, output):
        # TODO: Implement your logic.
        pass

CONFIGURATION = """Start processing with following configurations.
==============================================================================
  Base directory     : {basedir}
  Current working dir: {cwd}
  Configuration file : {configfile}
  Dry-run            : {dryrun}
  Input encoding     : {encoding}
  Input #files       : {nfiles}
  Output path        : {output}
  Output encoding    : {encoding_out}
==============================================================================
""".rstrip()


def main():
    logger = logging.getLogger(APPNAME)
    # Parse command line arguments.
    args = parse_arguments()
    files = None
    encoding = args.encoding
    outputpath = sys.stdout
    processor = MainProcess(args.dryrun)
    # Check and set configuration file.
    if args.config:
        configfile = args.config
        if os.path.isfile(configfile):
            processor.configure(configfile)
        else:
            logger.fatal('Configuration file is not found: %s', configfile)
            sys.exit(1)
    # Check input argument files path.
    if args.files:
        files = args.files
        for path in files:
            if os.path.isfile(path):
                logger.debug('Target file exists: %s', path)
            else:
                logger.fatal('File not found: %s', path)
                sys.exit(1)
    if args.output:
        outputpath = args.output
        if os.path.isfile(outputpath):
            logger.warn('Overwrite output file: %s', outputpath)
    logger.info(CONFIGURATION.format(basedir=BASEDIR, cwd=os.getcwd(),
                configfile=args.config, dryrun=args.dryrun,
                encoding=encoding, nfiles=len(files or []),
                output=args.output, encoding_out=args.encoding_out))
    # Dispatch main process., and catch unknown error.
    try:
        processor.process(files, encoding, outputpath)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(e)
        traceback.print_exc(file=sys.stderr)
    finally:
        logger.info('Finish processing.')


def test():
    # TODO: Implement test code.
    pass

if __name__ == '__main__':
    main()

# vim: set et ts=4 sw=4 cindent fileencoding=utf-8 :
