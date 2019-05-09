import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLEADS_YAML_FILE = os.path.join(ROOT_DIR, 'googleads.yaml')


#########################################################################
# DFP SETTINGS
#########################################################################

# A string describing the order
DFP_ORDER_NAME = None

# The email of the DFP user who will be the trafficker for
# the created order
DFP_USER_EMAIL_ADDRESS = None

# The exact name of the DFP advertiser for the created order
DFP_ADVERTISER_NAME = None

# Names of placements the line items should target.
DFP_TARGETED_PLACEMENT_NAMES = []

# Names of ad units the line items should target.
DFP_TARGETED_AD_UNIT_NAMES = []

# Sizes of placements. These are used to set line item and creative sizes.
DFP_PLACEMENT_SIZES = [
  {
    'width': '300',
    'height': '250'
  },
  {
    'width': '728',
    'height': '90'
  },
]

# Whether we should create the advertiser in DFP if it does not exist.
# If False, the program will exit rather than create an advertiser.
DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST = True

# If settings.DFP_ORDER_NAME is the same as an existing order, add the created 
# line items to that order. If False, the program will exit rather than
# modify an existing order.
DFP_USE_EXISTING_ORDER_IF_EXISTS = False

# Optional
# If the line item exists in the existing order, ignore them.
# Only use this when the new line items has the same configurations, except prices.
DFP_SKIP_EXISTING_LINE_ITEMS = False

# Optional
# Each line item should have at least as many creatives as the number of 
# ad units you serve on a single page because DFP specifies:
#   "Each of a line item's assigned creatives can only serve once per page,
#    so if you want the same creative to appear more than once per page,
#    copy the creative to associate multiple instances of the same creative."
# https://support.google.com/dfp_sb/answer/82245?hl=en
#
# This will default to the number of placements specified in
# `DFP_TARGETED_PLACEMENT_NAMES`.
DFP_NUM_CREATIVES_PER_LINE_ITEM = 4

# Optional
# The currency to use in DFP when setting line item CPMs. Defaults to 'USD'.
DFP_CURRENCY_CODE = 'USD'

#########################################################################
# PREBID SETTINGS
#########################################################################

# When bidder code is None, create a set of line items for all bidders.
# Otherwise, set line item targeting 'hb_bidder' to the specified bidder.
PREBID_BIDDER_CODE = None


#########################################################################
# PREBID PRICE BUCKET SETTINGS
#########################################################################

# Price buckets. This should match your Prebid settings for the partner. See:
# http://prebid.org/dev-docs/publisher-api-reference.html#module_pbjs.setPriceGranularity
PREBID_PRICE_BUCKETS = [
  {
    'precision': 2,
    'min': 0,
    'max': 2.99,
    'increment': 0.01
  },
  {
    'precision': 2,
    'min': 3.0,
    'max': 7.95,
    'increment': 0.05
  },
  {
    'precision': 2,
    'min': 8.0,
    'max': 20.0,
    'increment': 0.50
  }
]

# The price multiplier to adjust price buckets. This should match the currency settings.
PRICE_MULTIPLIERS = {
    'TWD': 30,
    'JPY': 110,
    'USD': 1
}

#########################################################################

# Try importing local settings, which will take precedence.
try:
    from local_settings import *
except ImportError:
    pass
