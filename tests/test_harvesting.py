# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
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

import os
import re
import responses

from invenio_oaiharvester.api import get_records, list_records
from invenio_testing import InvenioTestCase


class OaiHarvesterTests(InvenioTestCase):

    @responses.activate
    def test_list_records(self):
        raw_cs_xml = open(os.path.join(
            os.path.dirname(__file__), "data/sample_arxiv_response_listrecords_cs.xml"
        )).read()
        raw_physics_xml = open(os.path.join(
            os.path.dirname(__file__), "data/sample_arxiv_response_listrecords_physics.xml"
        )).read()

        responses.add(
            responses.GET,
            re.compile(r'http?://export.arxiv.org/oai2.*set=cs&.*'),
            body=raw_cs_xml,
            content_type='text/xml'
        )
        responses.add(
            responses.GET,
            re.compile(r'http?://export.arxiv.org/oai2.*set=physics&.*'),
            body=raw_physics_xml,
            content_type='text/xml'
        )
        records = list_records(metadata_prefix='arXiv',
                               from_date='2015-01-15',
                               until_date='2015-01-20',
                               url='http://export.arxiv.org/oai2',
                               name=None,
                               setSpec='cs physics')
        assert len(records) == 196   # 46 cs + 150 physics

    @responses.activate
    def test_get_from_identifiers(self):
        raw_xml = open(os.path.join(
            os.path.dirname(__file__), "data/sample_oai_dc_response.xml"
        )).read()

        responses.add(
            responses.GET,
            'http://export.arxiv.org/oai2',
            body=raw_xml,
            content_type='text/xml'
        )
        for rec in get_records(['oai:arXiv.org:1507.03011'],
                               url='http://export.arxiv.org/oai2'):
            identifier_in_request = rec.xml.xpath(
                "//dc:identifier",
                namespaces={"dc": "http://purl.org/dc/elements/1.1/"}
            )[0].text
            self.assertEqual(identifier_in_request,
                             "http://arxiv.org/abs/1507.03011")

    @responses.activate
    def test_get_from_identifiers_with_prefix(self):
        raw_xml = open(os.path.join(
            os.path.dirname(__file__), "data/sample_arxiv_response.xml"
        )).read()

        responses.add(
            responses.GET,
            'http://export.arxiv.org/oai2',
            body=raw_xml,
            content_type='text/xml'
        )
        for rec in get_records(['oai:arXiv.org:1507.03011'],
                               metadata_prefix="arXiv",
                               url='http://export.arxiv.org/oai2'):
            identifier_in_request = rec.xml.xpath(
                "//arXiv:id",
                namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}
            )[0].text
            self.assertEqual(identifier_in_request,
                             "1507.03011")
