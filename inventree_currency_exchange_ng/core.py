"""Plugin for requesting exchange rates from an external API."""

import structlog

from plugin import InvenTreePlugin
from plugin.mixins import APICallMixin, CurrencyExchangeMixin, SettingsMixin

from . import PLUGIN_VERSION

logger = structlog.get_logger("inventree")


class InvenTreeCurrencyExchangeNG(
    APICallMixin, CurrencyExchangeMixin, SettingsMixin, InvenTreePlugin
):
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

    SETTINGS = {
        "PROVIDER": {
            "name": "Central banks or official institutions",
            "description": "Choose a provider to get a specific exchange rate",
            "choices": [("ECB", "European Central Bank")],
            "default": "ECB",
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        providers = []

        response = self.api_call("/v2/providers", simple_response=False)
        if response.status_code == 200:
            providers = [(item["key"], item["name"]) for item in response.json()]

        if providers:
            self.SETTINGS["PROVIDER"]["choices"] = providers

    def update_exchange_rates(self, base_currency: str, symbols: list[str]) -> dict:
        """Update currency exchange rates for InvenTree."""

        response = self.api_call(
            "/v2/rates",
            url_args={
                "base": [base_currency],
                "quotes": symbols,
                "providers": [self.get_setting("PROVIDER")],
            },
            simple_response=False,
        )

        if response.status_code == 200:
            return {item["quote"]: item["rate"] for item in response.json()}

        logger.warning(
            "Failed to update exchange rates from %s: Server returned status %s",
            self.api_url,
            response.status_code,
        )

        return {
            base_currency: 1.0,
        }

    @property
    def api_url(self):
        """Return the API URL for this plugin."""
        return "https://api.frankfurter.dev"
