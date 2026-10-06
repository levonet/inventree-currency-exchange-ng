"""Plugin for requesting exchange rates from an external API."""

from plugin import InvenTreePlugin
from plugin.mixins import APICallMixin, CurrencyExchangeMixin, SettingsMixin

import structlog

from . import PLUGIN_VERSION

logger = structlog.get_logger('inventree')

class InvenTreeCurrencyExchangeNG(APICallMixin, CurrencyExchangeMixin, SettingsMixin, InvenTreePlugin):

    """InvenTreeCurrencyExchangeNG - custom InvenTree plugin for currency exchange rates.

    Fetches exchange rate information from frankfurter.dev
    """

    # Plugin metadata
    TITLE = "InvenTree Currency Exchange NG"
    NAME = "InvenTreeCurrencyExchangeNG"
    SLUG = "inventree-currency-exchange-ng"
    DESCRIPTION = "Currency exchange integration"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "Pavlo Bashynskyi"
    WEBSITE = "https://github.com/levonet/inventree-currency-exchange-ng"
    LICENSE = "MIT"

    # Optionally specify supported InvenTree versions
    # MIN_VERSION = '0.18.0'
    # MAX_VERSION = '2.0.0'


    # Plugin settings (from SettingsMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/settings/
    SETTINGS = {
        'PROVIDER': {
            'name': 'Central banks or official institutions',
            'description': 'A custom value',
            'choices': [('ECB','European Central Bank'),('BOC','Bank of Canada'),('NBU','Natsionalnyi Bank Ukrainy'),('FED','Federal Reserve Bank of St. Louis')],
            'default': 'ECB',
        }
    }

    # Support for currency exchange rates (from CurrencyExchangeMixin)
    # Ref: https://docs.inventree.org/en/latest/plugins/mixins/currency/
    def update_exchange_rates(self, base_currency: str, symbols: list[str]) -> dict:
        """Update currency exchange rates for InvenTree."""

        response = self.api_call(
            '/v2/rates',
            url_args={'base': [base_currency], 'quotes': symbols, 'providers': [self.get_setting('PROVIDER')]},
            simple_response=False,
        )
        logger.info(
            'GET %s: CODE %s: BODY %s',
            response.url,
            response.status_code,
            response.text,
        )

        if response.status_code == 200:
            rates = {item['quote']: item['rate'] for item in response.json()}
            rates[base_currency] = 1.00

            return rates
        logger.warning(
            'Failed to update exchange rates from %s: Server returned status %s',
            self.api_url,
            response.status_code,
        )


        # API https://frankfurter.dev
        return {
            'USD': 1.0,
            'EUR': 0.88,
            'GBP': 0.77,
            'UAH': 45.0,
        }

    @property
    def api_url(self):
        """Return the API URL for this plugin."""
        return 'https://api.frankfurter.dev'
