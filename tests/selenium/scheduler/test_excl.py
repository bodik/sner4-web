# This file is part of sner4 project governed by MIT license, see the LICENSE.txt file.
"""
selenium ui tests for scheduler.excl component
"""

from flask import url_for

from sner.server.extensions import db
from sner.server.scheduler.models import Excl
from tests.selenium import dt_inrow_delete, dt_rendered


def test_excl_list_route(live_server, sl_operator, excl_network):  # pylint: disable=unused-argument
    """simple test ajaxed datatable rendering"""

    sl_operator.get(url_for('scheduler.excl_list_route', _external=True))
    dt_rendered(sl_operator, 'excl_list_table', excl_network.comment)


def test_excl_list_route_inrow_delete(live_server, sl_operator, excl_network):  # pylint: disable=unused-argument
    """delete excl inrow button"""

    excl_network_id = excl_network.id
    db.session.expunge(excl_network)

    sl_operator.get(url_for('scheduler.excl_list_route', _external=True))
    dt_inrow_delete(sl_operator, 'excl_list_table')
    assert not Excl.query.get(excl_network_id)
