# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pdflog.info
import pdflog.meta
import pdflog.pages
import pdflog.version


def parse(path: str) -> iamraw.PDFInfo:
    version = pdflog.version.parse(path)
    if not version:
        # invalid file
        return None
    pages = pdflog.pages.determine(path)
    generator = pdflog.info.generator(path)
    meta = pdflog.meta.determine(path)
    info = iamraw.PDFInfo(
        pages=pages,
        version=version,
        generator=generator,
        meta=meta,
    )
    return info
