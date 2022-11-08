# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import pdfinfo
import pdfinfo.info
import pdfinfo.version
import tests

NO_PDF = __file__


@pytest.mark.parametrize('cmd', [
    '--help',
    pytest.param(f'-i {NO_PDF}', id='invalid_pdf'),
    pytest.param(f'-i {NO_PDF} --format=yaml', id='use yaml'),
    pytest.param(f'-i {power.DOCU027_PDF}', id='valid_pdf'),
    pytest.param(f'-i {power.MASTER116_PDF}', id='master116'),
    pytest.param(f'-i {power.MASTER089_PDF}', id='master89'),
    pytest.param(f'-i {power.MASTER098_PDF}', id='master98'),
])
def test_pdfinfo_run(cmd, td, mp):  #pylint: disable=W0613
    tests.run(cmd, mp=mp)


@pytest.mark.parametrize(
    'cmd',
    [
        pytest.param(f'-i {pdfinfo.ROOT}', id='input_directory'),
        pytest.param(f'-i {__file__} --strict', id='no_pdf_file'),
    ],
)
def test_pdfinfo_run_invalid(cmd, td, mp):  #pylint: disable=W0613
    tests.fail(cmd, mp=mp)


def test_pdfinfo_status_valid(td, mp):
    valid = iamraw.PDFInfo(
        pages=42,
        generator=iamraw.Generator.MSWORD,
        version=iamraw.PDFVersion(1, 5),
    )
    raw = serializeraw.dump_pdfinfo(valid)
    path = td.tmpdir.join('pdfinfo.json')
    utila.file_create(path, raw)
    tests.run('--status', mp=mp)


def test_pdfinfo_status_invalid(td, mp):
    path = td.tmpdir.join('pdfinfo.json')
    utila.file_create(path, '{}')
    returncode = tests.fail('--status', mp=mp)
    assert returncode == pdfinfo.INVALID_PDF


def test_pdfinfo_stdout(td, mp, capsys):
    root = td.tmpdir
    source = power.DOCU027_PDF
    with utilatest.increased_filecount(root, mindiff=0, maxdiff=0):
        tests.run(f'-i {source}', mp=mp)
    stdout = utilatest.stdout(capsys)
    expected = (
        '{"pages": 27, "generator": "latex", "version": {"major": 1, '
        '"minor": 5}, "meta": {"author": "", "title": "", "subject": "",')
    assert expected in stdout  # do not verify all parsed meta data


FAIL = {power.DISS273_PDF}
RESOURCES = [
    pytest.param(
        item,
        id=utila.file_name(item),
        marks=pytest.mark.xfail(reason='???') if item in FAIL else (),
    ) for item in power.PDF
]


@utilatest.longrun
@pytest.mark.parametrize('source', RESOURCES)
def test_huge(source, mp, tmpdir):
    cmd = f'-i {source} -o {tmpdir} --format=yaml'
    tests.run(cmd, mp=mp)
    pagecount = utila.parse_ints(
        utila.file_name(source),
        maxcount=1,
    )[0]
    info = serializeraw.load_pdfinfo(tmpdir)
    assert info.pages == pagecount, str(info)
