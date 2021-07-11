from django.utils.translation import ugettext_lazy as _


# Expiry time for access token
ACCESS_TOKEN_EXPIRY_TIME = 5

LANGUAGES = (
    ('spa', _('Spanish')),
    ('eng', _('English')),
    ('ger', _('German')),
    ('pid', _('Pidgin')),
)

CURRENCIES = (
    ('USD', _('Dollars')),
    ('EUR', _('Euros')),
    ('NGN', _('Naira')),
)
