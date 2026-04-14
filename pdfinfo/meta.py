# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import pdfminer.utils
import utilo

import pdfinfo.reader


def determine(path: str) -> dict:
    result = {}
    with pdfinfo.reader.read(path) as document:
        infos = document.info
        if not infos:
            # no meta information available
            utilo.error(f'could not read any meta information: {path}')
            return {}
        assert len(infos) == 1, str(infos)
        infos = infos[0]
        for key, value in infos.items():
            key = key.lower()
            value = prepare(value)
            result[key] = value
    return result


def resolve(reference):
    with contextlib.suppress(AttributeError):
        return reference.resolve()
    return reference


def prepare(value):
    """\
    >>> prepare([b'hello', b'tello'])
    ['hello', 'tello']
    """
    value = resolve(value)
    if isinstance(value, bytes):
        # SEE PDFDocEncoding Character Set
        value = pdfminer.utils.decode_text(value)
    elif isinstance(value, list):
        # convert bytes if required
        value = [prepare(item) for item in value]
    else:
        value = utilo.str2bool(value.name)
    return value
