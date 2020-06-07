import pytest

import kojoney_alert_server


def test_processAlert():
    """

    :param msg:
    :param expected_result:
    :return:
    """
    f = open('data/kojoney_alert_queue.txt', 'r')
    lines = f.readlines()
    for line in lines:
        result = kojoney_alert_server.processAlert(line)
        assert result is not None
    assert True
