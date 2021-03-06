# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2011, 2012, 2013, 2014, 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""OAI harvest database models."""

from __future__ import absolute_import, print_function, unicode_literals

import datetime

from invenio_ext.sqlalchemy import db
from invenio_ext.sqlalchemy.utils import session_manager


class OaiHARVEST(db.Model):

    """Represents a OaiHARVEST record."""

    __tablename__ = 'oaiHARVEST'

    id = db.Column(db.MediumInteger(9, unsigned=True), nullable=False,
                   primary_key=True, autoincrement=True)
    baseurl = db.Column(db.String(255), nullable=False, server_default='')
    metadataprefix = db.Column(db.String(255), nullable=False,
                               server_default='oai_dc')
    comment = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    lastrun = db.Column(db.DateTime, default=datetime.datetime(year=1900, month=1, day=1), nullable=True)
    setspecs = db.Column(db.Text, nullable=False)

    @session_manager
    def save(self):
        """Save object to persistent storage."""
        db.session.add(self)

    def update_lastrun(self, new_date=None):
        """Update the 'lastrun' attribute of the OaiHARVEST object to now."""
        self.lastrun = new_date or datetime.datetime.now()


__all__ = ('OaiHARVEST',)
