# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import pdflog.reader
import pdfminer.pdfpage


@functools.lru_cache(128)
def determine(path: str) -> int:
    with pdflog.reader.read(path) as document:
        pages = list(pdfminer.pdfpage.PDFPage.create_pages(document))
    result = len(pages)
    return result
