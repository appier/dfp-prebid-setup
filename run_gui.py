import tempfile
import os

try:
    import PySimpleGUIWx as sg
except ImportError:
    import PySimpleGUI as sg

from tasks import add_new_prebid_partner
import settings

# Reference: http://prebid.org/prebid-mobile/adops-price-granularity.html
price_granularity_buckets = {

    'dense': [
        # min, max, increment
        (0, 2.99, 0.01),   # 0 - 3
        (3, 7.95, 0.05),   # 3 - 8
        (8, 20.0, 0.50),  # 8 - 20 (cap at 20)
    ]
}

price_multipliers = {
    'TWD': 30,
    'JPY': 110,
    'USD': 1
}


DEFAULT_TITLE = 'Prebid Setup Tool for Google Ad Manager'

GOOGLE_YAML_FILE = """
# From: https://github.com/googleads/googleads-python-lib/blob/master/googleads.yaml
ad_manager:
  #############################################################################
  # Required Fields                                                           #
  #############################################################################
  application_name: {application}
  network_code: {network}
  path_to_private_key_file: {key_file}
"""


def main():
    settings.NO_CONFIRM = True
    try:
        # basic setup
        event, values = setup_basic_info()
        if event != 'OK':
            return
        settings.DFP_USER_EMAIL_ADDRESS = values['_NAME_']
        settings.DFP_ORDER_NAME = values['_ORDER_']
        settings.DFP_ADVERTISER_NAME = values['_ADVERTISER_']
        settings.DFP_CURRENCY_CODE = currency = values['_CURRENCY_'][0]

        granularity_type = 'dense'  # TODO: make it changeable
        multiplier = price_multipliers[currency]

        # setup credentials
        key_json_file = choose_key_file()
        if not key_json_file:
            return
        settings.GOOGLEADS_YAML_FILE = setup_googleads_yaml(network=values['_NETWORK_'], key_json_file=key_json_file)

        # setup ad units
        settings.DFP_TARGETED_AD_UNIT_NAMES = setup_adunits()
        if not settings.DFP_TARGETED_AD_UNIT_NAMES:
            return

        # setup as many creatives per line item as the adunit count
        settings.DFP_NUM_CREATIVES_PER_LINE_ITEM = len(settings.DFP_TARGETED_AD_UNIT_NAMES)

        # start
        # FIXME: it's bad to override globals like this, but due to the structure of the original code we have no choice.
        settings.PREBID_BIDDER_CODE = None
        price_buckets = price_granularity_buckets[granularity_type]
        for i, (min_price, max_price, increment) in enumerate(price_buckets):
            settings.PREBID_PRICE_BUCKETS = {
                'precision': 2,
                'min': min_price * multiplier,
                'max': max_price * multiplier,
                'increment': increment * multiplier,
            }

            msg = 'Creating line items for price range: {min} - {max}; increment={inc}, {currency})'.format(
                min=min_price, max=max_price, inc=increment, currency=currency
            )
            ret = sg.OneLineProgressMeter(DEFAULT_TITLE, i, len(price_buckets), 'progress_key', msg, orientation='h')
            if not ret:
                break

            # do the work
            add_new_prebid_partner.main()

            ret = sg.OneLineProgressMeter(DEFAULT_TITLE, i + 1, len(price_buckets), 'progress_key', msg, orientation='h')
            if not ret:
                break

        os.unlink(settings.GOOGLEADS_YAML_FILE)

        sg.PopupOK('Creation of line items completed!')

    except Exception as e:
        sg.PopupOK('Failed: ' + str(e))


def setup_basic_info():
    # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/docs/cookbook.md
    while True:
        currencies = tuple(price_multipliers.keys())
        layout = [
            [sg.Text('Setup basic info (all fields are required):')],
            [sg.Text('E-mail of Google Ad Manager account:', auto_size_text=True), sg.InputText(key='_NAME_', size=(32, 1))],
            [sg.Text('GAM network code:', auto_size_text=True), sg.InputText(key='_NETWORK_', size=(32, 1))],
            [sg.Text('Order Name', auto_size_text=True), sg.InputText(key='_ORDER_', size=(32, 1))],
            [sg.Text('Advertiser Name', auto_size_text=True), sg.InputText(key='_ADVERTISER_', size=(32, 1))],
            [sg.Text('Select the currency of your GAM account:', auto_size_text=True)],
            [sg.Listbox(values=currencies, default_values=('TWD', ), size=(40, 10), bind_return_key=True, key='_CURRENCY_')],
            [sg.OK(), sg.Cancel()]
        ]
        window = sg.Window(DEFAULT_TITLE, layout)
        event, values = window.Read()

        if event == 'OK' and len(values) < 5:
            sg.Popup('All fields are required!')
            continue
        else:
            break

    window.Close()
    return event, values


def setup_adunits():
    layout = [
        [sg.Text('List ad units you have (one adunit name per line):', auto_size_text=True)],
        [sg.Multiline('', size=(45, 30), key='_ADUNITS_')],
        [sg.OK(), sg.Cancel()]
    ]
    window = sg.Window(DEFAULT_TITLE, layout)
    event, values = window.Read()
    window.Close()
    adunit_lines = values['_ADUNITS_']
    return adunit_lines.splitlines() if adunit_lines else None


def choose_key_file():
    msg = """Please generate your Google AdManager credential file:
After you have download your credential file, browse for the file and click "OK" to continue.

1.  Sign into your GAM account. You must have admin rights.
2.  In the Admin section, select Global settings
3.  Ensure that API access is enabled.
4.  Click the Add a service account user button.
5.  Use the service account email for the Google developer credentials you created above.
6.  Set the role to "Trafficker".
7.  Click Save.

Details:
https://github.com/kmjennison/dfp-prebid-setup#creating-google-credentials

Select your credential file:"""
    key_json_file = sg.PopupGetFile(message=msg, title='Open file', file_types=[('JSON', '*.json')])
    return key_json_file


def setup_googleads_yaml(network, key_json_file):
    config_yaml = GOOGLE_YAML_FILE.format(application='Prebid Setup', network=network,
                                          key_file=key_json_file)
    with tempfile.NamedTemporaryFile('w', suffix='google.yaml', delete=False) as f:
        f.write(config_yaml)
    return f.name


if __name__ == '__main__':
    main()
