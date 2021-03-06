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
import csv
import datetime
import gzip
import hashlib
import json
import logging
import logging.config
import os
import sqlite3
import sys
import time
import traceback
from collections import Counter
from functools import partial
from pathlib import Path

__version__ = '0.1.0'
__author__ = 'Shigeru Kitazaki'

APPNAME = Path(__file__).stem
BASEDIR = Path(__file__).parent.resolve()

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CONFIG_FILE_ENCODING = 'utf8'
DEFAULT_SQLITE_FILE = ':memory:'
DEFAULT_INPUT_FILE_ENCODING = 'utf8'
DEFAULT_OUTPUT_FILE_ENCODING = 'utf8'
DEFAULT_LOG_DIRECTORY = Path.cwd()

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
            'level': 'INFO',
            'stream': 'ext://sys.stderr',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': DEFAULT_LOG_DIRECTORY / (APPNAME + '.log'),
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
            'handlers': ['console', 'file'],
            'level': 'WARN',
            'propagate': False
        }
    }
})


def parse_arguments():
    """Parse arguments and set up logging verbosity.

    :rtype: parsed arguments as Namespace object.
    """
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument('-c', '--config', dest='config', required=False,
                        help='configuration file', metavar='FILE')
    parser.add_argument('-s', '--sqlite', dest='sqlite', required=False,
                        help='local SQLite3 file', metavar='FILE')
    parser.add_argument('-M', '--monitor-output', dest='monitor_out',
                        help='progress monitor dump file', metavar='FILE')
    parser.add_argument('-o', '--output', dest='output',
                        help='output path', metavar='FILE')
    parser.add_argument('-n', '--dryrun', dest='dryrun',
                        help='dry run', default=False, action='store_true')
    parser.add_argument('-e', '--encoding', dest='encoding',
                        help='input file encoding',
                        default=DEFAULT_INPUT_FILE_ENCODING)
    parser.add_argument('-E', '--output-encoding', dest='encoding_out',
                        help='output file encoding',
                        default=DEFAULT_OUTPUT_FILE_ENCODING)
    parser.add_argument('-r', '--recursive', dest='recursive', default=False,
                        help='search recursive', action='store_true')
    parser.add_argument('files', nargs='*',
                        help='input files', metavar='FILE')

    header = parser.add_mutually_exclusive_group()

    header.add_argument('--with-header', dest='header',
                        action='store_const', const=True,
                        help='input file has header line (default)')

    header.add_argument('--without-header', dest='header',
                        action='store_const', const=False,
                        help='input file does not have header line')

    parser.set_defaults(header=True)

    loglevel = parser.add_mutually_exclusive_group()

    loglevel.add_argument('-v', '--verbose', dest='verbose',
                          action='count', default=0,
                          help='increase logging verbosity')

    loglevel.add_argument('-q', '--quiet', dest='quiet',
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
        logger.setLevel(logging.ERROR)
    elif args.verbose >= 1:
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.INFO)

    return args


def collect_files(inputs, recursive=False):
    '''Collect file paths from input arguments.
    The directory whose name starts with "." and the file whose name ends with
    "~" are skipped.
    '''
    logger = logging.getLogger(APPNAME + '.setup')
    files = []
    if inputs is None or len(inputs) == 0:
        return files
    for path in inputs:
        if os.path.isfile(path):
            logger.debug('Target file exists: %s', path)
            files.append(path)
        elif os.path.isdir(path) and recursive:
            logger.debug('Target directory exists: %s', path)
            for root, ds, fs in os.walk(path):
                # Prune hidden directory.
                ds[:] = [d for d in sorted(ds) if not d.startswith('.')]
                for f in sorted(filter(lambda f: not f.endswith('~'), fs)):
                    p = os.path.join(root, f)
                    files.append(p)
        else:
            logger.fatal('File not found: %s', path)
            sys.exit(1)
    logger.debug('Collect {:,} files.'.format(len(files)))
    return files


def md5sum(path):
    # Calculate MD5 sum value.
    chunk_size = 4096
    md5 = hashlib.md5()
    with open(path, 'rb') as fp:
        for buf in iter(partial(fp.read, chunk_size), b''):
            md5.update(buf)
    return md5.hexdigest()


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
        assert path
        self.path = path
        self.logger = logging.getLogger(APPNAME + '.config')

    def _load(self, extension):
        self.logger.debug('Config file extension is "%s".', extension)
        if extension == '.json':
            with open(self.path, encoding=CONFIG_FILE_ENCODING) as fp:
                return json.load(fp)
        elif extension in (".ini", ".cfg"):
            parser = configparser.SafeConfigParser()
            with open(self.path, encoding=CONFIG_FILE_ENCODING) as fp:
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
            self.logger.warning('missing file extension: %s', self.path)
            return
        elif not ext.startswith('.'):
            self.logger.warning("file extension doesn't start with dot: %s",
                                self.path)
            return
        return self._load(ext)


class ProgressMonitor(object):

    TABLE_NAME = '_monitor'
    SCHEMA = {
        'fields': (
            {'name': 'seq', 'type': 'integer',
             'constraints': {'required': True, 'unique': True}},
            {'name': 'path', 'type': 'string',
             'constraints': {'required': True}},
            {'name': 'size', 'type': 'integer',
             'constraints': {'required': True}},
            {'name': 'start_at', 'type': 'float',
             'constraints': {'required': True}},
            {'name': 'finish_at', 'type': 'float'},
            {'name': 'digest', 'type': 'string',
             'constraints': {'required': True, 'unique': True}},
            {'name': 'result', 'type': 'string'},  # Anything encoded by JSON
        ),
        'primaryKey': ['seq']
    }

    def __init__(self, db, dump=None):
        self.logger = logging.getLogger(APPNAME + '.monitor')
        self.db = db
        self.create_table()
        self.dump = dump
        self.current = None

    def create_table(self):
        # Check whether monitor table already exists.
        r = self.fetch_one('sql',
                           (('type', '=', 'table'),
                            ('tbl_name', '=', ProgressMonitor.TABLE_NAME)),
                           'sqlite_master')
        if r:
            self.logger.info('Monitor table is already created.')
            self.logger.debug(r[0])
            return
        d = []
        # Pattern mapping against JSON Table Schema
        for s in ProgressMonitor.SCHEMA['fields']:
            t = 'TEXT'
            if s['type'] == 'integer':
                t = 'INTEGER'
            elif s['type'] == 'float':
                t = 'REAL'
            f = '{} {}'.format(s['name'], t)
            c = s.get('constraints')
            if c:
                if c.get('required'):
                    f += ' NOT NULL'
                if c.get('unique'):
                    f += ' UNIQUE'
            d.append(f)
        f = 'PRIMARY KEY ('
        f += ','.join(k for k in ProgressMonitor.SCHEMA['primaryKey'])
        f += ')'
        d.append(f)
        ddl = """CREATE TABLE {} ({})""".format(
            ProgressMonitor.TABLE_NAME, ','.join(d))
        self.logger.debug('Create monitor table: %s', ddl)
        cur = self.db.cursor()
        cur.execute(ddl)
        cur.close()
        self.logger.info('Created monitor table.')

    def terminate(self, fields):
        if self.dump is None:
            return
        if os.path.isfile(self.dump):
            self.logger.warn('Overwrite dump file: %s', self.dump)
        self.logger.info('Dump monitor records as tab-delimited values.')
        fp = open(self.dump, 'w')
        writer = csv.writer(fp, delimiter='\t', lineterminator='\n')
        columns = [f['name'] for f in ProgressMonitor.SCHEMA['fields']]
        q = 'SELECT {} FROM {} ORDER BY seq'.format(
            ','.join(columns), ProgressMonitor.TABLE_NAME)
        cur = self.db.cursor()
        cur.execute(q)
        dumper = Tabular(fields)
        writer.writerow(dumper.header())
        for r in cur:
            t = dict(zip(columns, r))
            t['path'] = t['path'].replace('\\', '/')
            t['basename'] = os.path.basename(t['path'])
            t['extension'] = os.path.splitext(t['path'])[-1].lower()
            if t['finish_at'] is not None:
                t['elapsed'] = t['finish_at'] - t['start_at']
                t['finish_at'] = datetime.datetime.fromtimestamp(t['finish_at'])
            t['start_at'] = datetime.datetime.fromtimestamp(t['start_at'])
            if t['result']:
                result = json.loads(t['result'])
                for k in result:
                    t[k] = result[k]
            writer.writerow(dumper(t))
        cur.close()
        fp.close()

    def fetch_one(self, columns, conditions, table=None):
        # It's okay `columns` is string or list.
        if type(columns) == str:
            columns = [columns, ]
        d = []
        values = []
        # Column name, Operator, Value tuples.
        for c, o, v in conditions:
            # "?" is placement holder.
            d.append("{} {} ?".format(c, o))
            values.append(v)
        q = """SELECT {} FROM {} WHERE {}""".format(
            ','.join(columns),
            table or ProgressMonitor.TABLE_NAME,
            ' AND '.join(d))
        self.logger.debug('Fetch one record: %s; %s', q, values)
        cur = self.db.cursor()
        cur.execute(q, values)
        r = cur.fetchone()
        cur.close()
        return r

    def start(self, path):
        md5 = md5sum(path)
        r = self.fetch_one(['seq', 'path', 'size', 'start_at', 'finish_at'], (
            ('digest', '=', md5),
        ))
        if r:
            msg = 'Already processed "{}": [{}] {} -> {}'
            self.logger.info(msg.format(r[1], r[0], r[2], r[3]))
            return r
        size = os.path.getsize(path)
        self.logger.info('Start monitoring: {} ({}) {:,}bytes'.format(
                         path, md5, size))
        columns = ('path', 'size', 'start_at', 'digest')
        values = (path, size, time.time(), md5)
        q = """INSERT INTO {} ({}) VALUES ({})""".format(
            ProgressMonitor.TABLE_NAME,
            ','.join(columns),
            ','.join(['?' for i in range(len(values))])
            )
        self.logger.debug('Insert one record: %s; %s', q, values)
        cur = self.db.cursor()
        cur.execute(q, values)
        cur.close()
        self.current = md5

    def finish(self, result=None):
        if self.current is None:
            self.logger.fatal('Monitor nothing, but `finish()` is called.')
            return
        r = self.fetch_one(['seq', 'path', 'start_at'], (
            ('digest', '=', self.current),
        ))
        if r is None:
            self.logger.fatal('Monitor "%s", but removed.', self.current)
            return
        now = time.time()
        if result:
            values = (now, json.dumps(result), r[0])
            columns = ('finish_at = ?', 'result = ?')
        else:
            values = (now, r[0])
            columns = ('finish_at = ?', )
        q = """UPDATE {} SET {} WHERE seq = ?""".format(
            ProgressMonitor.TABLE_NAME,
            ','.join(columns)
            )
        self.logger.debug('Update one record: %s; %s', q, values)
        cur = self.db.cursor()
        cur.execute(q, values)
        cur.close()
        self.current = None
        self.logger.info('Finish processing: {} [{}] {:,.03f}sec'.format(
            r[1], r[0], now - r[2]))


class Tabular(object):

    '''JSON Table Schema based record class.

    FIELDS = (
        {'name': 'id', 'type': 'string'},
        {'name': 'updated', 'type': 'datetime', 'format': '%Y-%m-%dT%H:%M:%SZ'},
        {'name': 'name', 'type': 'string'},
        {'name': 'latitude', 'type': 'float'},
        {'name': 'longitude', 'type': 'float'},
        {'name': 'zipcode', 'type': 'string'},
        {'name': 'kind', 'type': 'string', 'default': 'UNKNOWN'},
        {'name': 'update_type', 'type': 'integer'}
    )
    '''

    def __init__(self, fields):
        self.fields = fields

    def header(self):
        return [f['name'] for f in self.fields]

    def __call__(self, dt):
        out = []
        for f in self.fields:
            k, t = f['name'], f['type']
            v = dt.get(k, f.get('default', ''))
            if v is None:
                val = ''
            elif t == 'string':
                val = v
            elif t == 'datetime':
                val = v.strftime(f['format'])
            elif t == 'integer':
                val = str(v)
            elif t in ('float', 'numeric'):
                if 'precision' in f:
                    v = round(v, f['precision'])
                val = str(v)
            elif t == 'boolean':
                m = f.get('mapping', {})
                if v in m:
                    val = m[v]
                else:
                    val = str(v)
            else:
                raise ValueError('Unknown type "{}" for "{}"'.format(t, k))
            out.append(val)
        return out

# Default monitor dump schema. If you add more fields to dump, add it here.
MONITOR_DUMP_FIELDS = (
    {'name': 'seq', 'type': 'integer'},
    {'name': 'path', 'type': 'string'},
    {'name': 'basename', 'type': 'string'},
    {'name': 'extension', 'type': 'string'},
    {'name': 'size', 'type': 'integer'},
    {'name': 'columns', 'type': 'integer'},
    {'name': 'lines', 'type': 'integer'},
    {'name': 'start_at', 'type': 'datetime', 'format': DATETIME_FORMAT},
    {'name': 'finish_at', 'type': 'datetime', 'format': DATETIME_FORMAT},
    {'name': 'elapsed', 'type': 'float', 'precision': 4},
    {'name': 'digest', 'type': 'string'},
)


class App(object):

    """Main application class.
    # TODO: Implement your logic.
    """

    def __init__(self, db):
        self.logger = logging.getLogger(APPNAME + '.app')
        self.db = db

    def process(self, fp, header):
        lines = 0
        if header:  # skip header line
            next(fp)
            lines += 1
        # TODO: Implement your logic.
        reader = map(str.rstrip, fp)
        for l in reader:
            lines += 1
        return {'lines': lines}


class MainProcess(object):

    """Main process class for wrapping setup/termination.
    """

    def __init__(self, dryrun):
        self.dryrun = dryrun
        self.logger = logging.getLogger(APPNAME + '.main')

    def configure(self, configfile):
        if not os.path.isfile(configfile):
            self.logger.fatal('Configuration file is not found: %s', configfile)
            return
        loader = ConfigLoader(configfile)
        config = loader.load()
        if config is None:
            self.logger.warn('Nothing to be loaded.')
            return
        for k in sorted(config):
            self.logger.debug('config key: %s', k)
        # TODO: Implement your logic.

    def initialize(self, config, output, output_encoding,
                   sqlite=None, monitor_dump=None):
        if config:
            self.configure(config)
        if output:
            if os.path.isfile(output):
                self.logger.warn('Overwrite output file: %s', output)
            self.output = open(output, 'w', encoding=output_encoding)
        else:
            self.output = sys.stdout
        if sqlite and os.path.isfile(sqlite):
            self.logger.info('Reuse local SQLite3 file: %s', sqlite)
        self.localdb = sqlite3.connect(sqlite or DEFAULT_SQLITE_FILE)
        self.monitor = ProgressMonitor(self.localdb, monitor_dump)

    def terminate(self):
        self.monitor.terminate(MONITOR_DUMP_FIELDS)
        if not self.output.isatty():
            self.output.close()
        self.localdb.commit()
        self.logger.info('Terminated the process.')

    def run(self, files, encoding, header):
        app = App(self.localdb)
        if not files:
            app.process(sys.stdin, header)
            return
        counter = Counter()
        for path in files:
            counter['total'] += 1
            canskip = self.monitor.start(path)
            if canskip:
                counter['skip'] += 1
                self.logger.info('Skip to process: %s', path)
                continue
            _, suffix = os.path.splitext(path)
            if suffix == '.gz':
                opener = gzip.open
                open_mode = 'rt'
            else:
                opener = open
                open_mode = 'r'
            with opener(path, open_mode, encoding=encoding) as fp:
                r = app.process(fp, header)
            self.monitor.finish(r)
            if r is None:
                counter['ignore'] += 1
            else:
                counter['process'] += 1
        self.logger.info('show summary:')
        for k in sorted(counter):
            self.logger.info(' - {:20s} : {:,}'.format(k, counter[k]))


CONFIGURATION = """Start running with following configurations.
==============================================================================
  Base directory     : {basedir}
  Current working dir: {cwd}
  Configuration file : {configfile}
  Local SQLite3 file : {sqlite}
  Monitor dump file  : {monitordumpfile}
  Dry-run            : {dryrun}
  Input encoding     : {encoding}
  Input has header   : {header}
  Input #files       : {nfiles}
  Search recursive   : {recursive}
  Output path        : {output}
  Output encoding    : {encoding_out}
==============================================================================
""".rstrip()


def main():
    # Parse command line arguments.
    args = parse_arguments()
    files = collect_files(args.files, args.recursive)
    encoding = args.encoding
    configfile = os.path.abspath(args.config) if args.config else None
    logger = logging.getLogger(APPNAME + '.setup')
    logger.info(CONFIGURATION.format(basedir=BASEDIR, cwd=os.getcwd(),
                configfile=configfile, dryrun=args.dryrun,
                encoding=encoding, nfiles=len(files or []),
                recursive=args.recursive, header=args.header,
                sqlite=args.sqlite, monitordumpfile=args.monitor_out,
                output=args.output, encoding_out=args.encoding_out))
    # Initialize main class.
    processor = MainProcess(args.dryrun)
    processor.initialize(configfile, args.output, args.encoding_out,
                         args.sqlite, args.monitor_out)
    # Dispatch main process, and catch unknown error.
    try:
        processor.run(files, encoding, args.header)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(e)
        traceback.print_exc(file=sys.stderr)
    finally:
        processor.terminate()


if __name__ == '__main__':
    main()


# Test suites to bundle as one file script.
# To run the tests, invoke this script using "-m unittest" option.
# i.e. `python3 -m unittest -v boilerplate.py`
import tempfile
import unittest


class TabularTest(unittest.TestCase):

    def setUp(self):
        fields = (
            {'name': 'id', 'type': 'string'},
            {'name': 'updated', 'type': 'datetime',
             'format': DATETIME_FORMAT},
            {'name': 'name', 'type': 'string'},
            {'name': 'latitude', 'type': 'float'},
            {'name': 'longitude', 'type': 'float'},
            {'name': 'zipcode', 'type': 'string'},
            {'name': 'kind', 'type': 'string', 'default': 'UNKNOWN'},
            {'name': 'update_type', 'type': 'integer'}
        )
        self.tabular = Tabular(fields)

    def test_header(self):
        expected = ['id', 'updated', 'name', 'latitude', 'longitude',
                    'zipcode', 'kind', 'update_type']
        self.assertEqual(expected, self.tabular.header())

    def test_call(self):
        data = {
            'id': '1234567890',
            'updated': datetime.datetime(2000, 1, 1, 12, 34, 56),
            'name': 'somewhere',
            'latitude': 12.34,
            'longitude': -123.45678,
            'zipcode': 'ABCDEF',
            'update_type': 0
        }
        expected = ['1234567890', '2000-01-01 12:34:56', 'somewhere',
                    '12.34', '-123.45678', 'ABCDEF', 'UNKNOWN', '0']
        self.assertEqual(expected, self.tabular(data))


class ConfigLoaderTest(unittest.TestCase):

    def setUp(self):
        config = '''
            {
                "database": {
                    "host": "127.0.0.1",
                    "port": 5432,
                    "name": "t",
                    "user": "app",
                    "password": "secret"
                }
            }
        '''
        fd, path = tempfile.mkstemp('.json')
        with open(path, 'w', encoding=CONFIG_FILE_ENCODING) as fp:
            fp.write(config)
        self.loader = ConfigLoader(path)

    def tearDown(self):
        os.unlink(self.loader.path)

    def test_load(self):
        expected = {
            'host': '127.0.0.1',
            'port': 5432,
            'name': 't',
            'user': 'app',
            'password': 'secret'
        }
        config = self.loader.load()
        self.assertEqual(expected, config['database'])

    def test_initialize_failure(self):
        with self.assertRaises(AssertionError):
            ConfigLoader(None)
            ConfigLoader('')

    def test_invalid_path(self):
        loader = ConfigLoader('notfound')
        self.assertIsNone(loader.load())
