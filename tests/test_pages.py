# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdflog.pages
import power


def test_pdflog_parse_pages():
    resource = power.DOCU027_PDF
    pages = pdflog.pages.determine(resource)
    assert pages == 27, str(pages)
