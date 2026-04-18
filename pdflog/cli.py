# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pdflog.data
import serializeraw
import utilo
import utilo.cli

import pdflog

DESCRIPTION = """\
Verify given -i input file that file is a valid pdf file. Extract:
 + version
 + generator
 + pages

If no output is given, print validation result to stdout.
"""

COMMANDS = [
    utilo.cli.Flag(
        '--status',
        message=('evaluate pdflog.json. '
                 'return 0 if info is valid, 4 if pdflog is invalid, '
                 '2 if pdflog does not exists')),
    utilo.cli.Command(
        longcut='--format',
        message='choose output format, json is default',
        args={
            'nargs': '?',
            'const': 'auto',
            'choices': [
                'json',
                'yaml',
            ],
        },
    ),
    utilo.cli.Flag('--strict', message='fail on invalid pdf file'),
]

CONFIG = utilo.ParserConfiguration(
    inputparameter=True,
    outputparameter=True,
    prefix=False,
    verboseflag=True,
    multiprocessed=False,
    pages=False,
    cacheflag=False,
    waitingflag=False,
)


@utilo.saveme
def main():
    parser = utilo.cli.create_parser(
        config=CONFIG,
        description=DESCRIPTION,
        todo=COMMANDS,
        version=pdflog.__version__,
    )
    args = utilo.parse(parser)
    inpath, outpath = utilo.sources(args, singleinput=True)  # pylint:disable=W0632
    # It is only single path supported. Run program multiple times if more
    # than one analysis is required.
    inpath = inpath[0]
    if args['status']:
        return status(inpath)
    # TODO: REPLACE AFTER UPGRADING UTILO
    if args['output'] is None:
        outpath = None
    ext = args['format']
    if ext is None:
        ext = 'json'
    strict = args.get('strict', False)
    validated = validate(inpath, outpath, ext, strict)
    return validated


def validate(inpath, outpath, ext='json', strict: bool = False) -> int:
    if not os.path.isfile(inpath):
        utilo.error(f'require valid pdf file: {inpath}')
        return utilo.INVALID_COMMAND
    assert os.path.exists(inpath), f'invalid inpath: {inpath}'
    try:
        parsed = pdflog.data.parse(inpath)
    except ValueError:
        # not a valid pdf file
        parsed = None
    if parsed is None and strict:
        utilo.error(f'invalid pdf file: {inpath}')
        return pdflog.INVALID_PDF
    raw = '{}'
    if parsed is not None:
        try:
            raw = serializeraw.dump_pdfinfo(parsed, ext)
        except TypeError as error:
            utilo.error(error)
            utilo.error('could not dump pdflog')
            return utilo.FAILURE
    if outpath is None:
        # print to stdout
        utilo.log(raw)
    else:
        if os.path.isdir(outpath):
            outpath = os.path.join(outpath, f'pdflog.{ext}')
        assert str(outpath).endswith(
            ext), f'missmatching --format and --outpath {outpath}'
        utilo.file_replace(outpath, raw)
    return utilo.SUCCESS


def status(path: str) -> int:
    source = os.path.join(path, 'pdflog.json')
    if not os.path.exists(source):
        utilo.error(f'path: {source} does not exists')
        return utilo.INVALID_COMMAND
    # load status
    parsed = utilo.file_read(source)
    if parsed == '{}':
        return pdflog.INVALID_PDF
    return utilo.SUCCESS
