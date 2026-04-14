# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import jam
import pytest
import utilotest

import tests


@pytest.mark.timeout(120)
@utilotest.nightly
@pytest.mark.security
def test_badguy_longpdf(td, mp):
    """Test that program success on very long, empty pdf file.

    Long files with content are excluded by file size limit.
    """
    very_long = td.tmpdir.join('mejabalong.pdf')
    jam.write_blank_pdf(10000, very_long)
    tests.run(f'-i {very_long}', mp=mp)
