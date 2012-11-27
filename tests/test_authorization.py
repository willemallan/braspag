# -*- coding: utf8 -*-

from __future__ import absolute_import

import codecs

from mock import MagicMock

from decimal import Decimal

from braspag.utils import spaceless
from braspag.consts import PAYMENT_METHODS

from base import BraspagTestCase


AUTHORIZATION_DATA = 'tests/data/authorization_request.xml'


class AuthorizeTest(BraspagTestCase):

    def setUp(self):
        super(AuthorizeTest, self).setUp()
        self.data_dict = {
            'request_id': '782a56e2-2dae-11e2-b3ee-080027d29772',
            'order_id': '782b632a-2dae-11e2-b3ee-080027d29772',
            'customer_id': '12345678900',
            'customer_name': u'José da Silva',
            'customer_email': 'jose123@dasilva.com.br',
            'amount': 10000,
            'card_holder': 'Jose da Silva',
            'card_number': '0000000000000001',
            'card_security_code': '123',
            'card_exp_date': '05/2018',
            'payment_method': PAYMENT_METHODS['Simulated']['BRL'],
        }

        with open('tests/data/cc_auth_response.xml') as response:
            self.braspag._request.return_value = response.read()

        self.response = self.braspag.authorize(**self.data_dict)

    def test_amount(self):
        assert self.response.amount == Decimal('100.00')

    def test_auth_code(self):
        assert self.response.authorization_code == u'20121127023808921'

    def test_acquirer_transaction(self):
        assert self.response.acquirer_transaction_id == u'1127023808906'

    def test_brapag_order_id(self):
        assert self.response.braspag_order_id == u'893cd2c6-9a29-4009-bd5b-4cc8791ebb49'

    def test_order_id(self):
        assert self.response.order_id == u'893cd2c6-9a29-4009-bd5b-4cc8791ebb49'

    def test_card_token(self):
        pass

    def test_correlation_id(self):
        assert self.response.correlation_id == u'5b4515b3-eaa8-4d0c-983b-8e4aa0d4893f'

    def test_errors(self):
        pass

    def test_payment_method(self):
        assert self.response.payment_method == 997

    def test_return_code(self):
        assert self.response.return_code == 4

    def test_return_message(self):
        assert self.response.return_message == u'Operation Successful'

    def test_status(self):
        assert self.response.status == 1

    def test_status_message(self):
        assert self.response.status_message == 'Authorized'

    def test_success(self):
        assert self.response.success == True

    def test_transaction_id(self):
        assert self.response.transaction_id == u'0dfc078c-4c8b-454a-af0f-1f02023a4141'

    def test_render_cc_template(self):
        self.braspag._render_template = MagicMock(name='_render_template')
        response = self.braspag.authorize(**self.data_dict)

        self.braspag._render_template.assert_called_once_with(
            'authorize_creditcard.xml',
            dict(self.data_dict.items() + [
                ('currency', 'BRL'),
                ('payment_plan', 0),
                ('number_of_payments', 1),
                ('country', 'BRA'),
                ('transaction_type', 2),
            ])
        )

    def test_webservice_request(self):
        response = self.braspag.authorize(**self.data_dict)
        with codecs.open(AUTHORIZATION_DATA, encoding='utf-8') as xml:
            self.braspag._request.assert_called_with(spaceless(xml.read()))
