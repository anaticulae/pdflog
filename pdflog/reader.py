# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import sys

import utilo
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFEncryptionError
from pdfminer.pdfdocument import PDFSyntaxError
from pdfminer.pdfparser import PDFParser

import pdflog.data


@contextlib.contextmanager
def read(path: str, password: str = None, verify: bool = True) -> PDFDocument:
    """Open pdf from `path`.

    Args:
        path(str): path to pdf-file
        password(str): optional password to extract encrypted data
        verify(bool): ensure that file starts with `%PDF-`
    Raises:
        TextExtractNotAllowed: if no extraction is allowed - currently disabled
        FileNotFoundError: `path` does not exists
        ValueError: `path` is not a file
    Yields:
        PDFDocument: open pdf file
    """
    if verify and pdflog.version.parse(path) is None:
        raise ValueError(f'invalid pdf header: {path}')
    with open(path, 'rb') as fp:
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = open_document(parser, password)
        yield document


def open_document(parser: PDFParser, password: str) -> PDFDocument:
    """Open pdf document base on selected `parser`.

    Hint:
        Using fallback as default mode is very slow. Therefore we try
        without fallback and if this does not work, we try it with
        fallback again.
        Try first without using fallback because this is much faster on
        valid documents. If the run without fallback fails, start it
        with fallback again.
    """
    password = password if password is not None else ''
    try:
        document = PDFDocument(parser, password, fallback=False)
    except PDFSyntaxError:
        pass  # try with fallback again
    except PDFEncryptionError as encryption:
        utilo.error('encryption not supported')
        utilo.debug(encryption)
        sys.exit(1)
    except Exception:  # pylint:disable=broad-except
        utilo.print_stacktrace()
        sys.exit(2)
        # raise PDFParserImplementationError(path) from exc
    else:
        return document
    try:
        utilo.info('try to use `fallback` pdf loader')
        document = PDFDocument(parser, password, fallback=True)
    except PDFSyntaxError:
        utilo.print_stacktrace()
        sys.exit(3)
        # raise InvalidPDF(path) from exc
    except Exception:  # pylint:disable=broad-except
        # raise PDFParserImplementationError(path) from exc
        utilo.print_stacktrace()
        sys.exit(2)
    return document
