"""Currency exchange integration"""


from plugin import InvenTreePlugin

from plugin.mixins import CurrencyExchangeMixin, SettingsMixin

from . import PLUGIN_VERSION


class InvenTreeCurrencyExchangeNG(CurrencyExchangeMixin, SettingsMixin, InvenTreePlugin):

    """InvenTreeCurrencyExchangeNG - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "InvenTree Currency Exchange NG"
    NAME = "InvenTreeCurrencyExchangeNG"
    SLUG = "inventree-currency-exchange-ng"
    DESCRIPTION = "Currency exchange integration"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "Pavlo Bashynskyi"
    WEBSITE = "https://inventree.org"
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
        # Example implementation
        return {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.75,
            'UAH': 45.0,
        }
