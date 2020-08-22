""" check free mt services. """

from pool_tr.probe_services import probe_services


def test_check_sanity():
    """ check sanity. """
    assert 1


def test_check_minimal():
    """ check sanity. """
    res = probe_services()
    print("res: ", res)  # valid, invalid, pairs

    assert len(res) == 3
    assert len(res[0]) + len(res[1]) >= 9

    assert "试验" in " ".join([elm[2] for elm in res[2]])
