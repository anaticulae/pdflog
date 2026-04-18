# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pdflog.version
import power


def test_pdflog_parse_version():
    resource = power.DOCU027_PDF
    parsed = pdflog.version.parse(resource)
    assert parsed == iamraw.PDFVersion(1, 5), str(parsed)
