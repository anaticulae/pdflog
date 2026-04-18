# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import pdflog.data


def test_pdflog_data_jsonify():
    resource = power.DOCU027_PDF
    info = pdflog.data.parse(resource)
    # dump it
    jsoned = serializeraw.dump_pdfinfo(info)
    assert isinstance(jsoned, str), str(jsoned)
    assert 'latex' in jsoned
    assert 'version' in jsoned
    assert 'major' in jsoned
    assert 'pages' in jsoned
