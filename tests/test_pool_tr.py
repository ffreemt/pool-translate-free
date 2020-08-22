from pool_tr import __version__
from pool_tr.pool_tr import pool_tr


def test_version():
    assert __version__[:3] in "0.1.0"
