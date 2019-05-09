
def num_to_micro_amount(num, precision=2):
  """
  Converts a number into micro-amounts (multiplied by 1M), rounded to
  specified precision. Useful for more easily working with currency,
  and also for communicating with DFP API.

  Args:
    num (float or int)
    precision (int)
  Returns:
    an integer: int(num * 1,000,000), rounded to the nearest
      10^(6-`precision`)
  """
  rounding = -6 + precision
  return int(round(num * (10 ** 6), rounding))

def micro_amount_to_num(micro_amount):
  """
  Converts micro-amount into its number.

  Args:
    micro_amount (int)
  Returns:
    a float: micro_amount divided by 1M
  """
  return float(micro_amount) / (10 ** 6)

def num_to_str(num, precision=2):
  """
  Converts num into a string with `precision` number
  of decimal places.

  Args:
    num (float or int)
    precision (int)
  Returns:
    a string
  """
  return '%.{0}f'.format(str(precision)) % num 


def adjust_price_bucket_by_price_multiplier(price_bucket, price_multiplier):
  """
  Args:
    price_bucket (object): the price bucket configuration
    price_multiplier (int): the price_multiplier to adjust price bucket
  :return: updated price_bucket
  """
  new_price_buckets = {
    'precision': price_bucket['precision'],
    'min': price_bucket['min'] * price_multiplier,
    'max': price_bucket['max'] * price_multiplier,
    'increment': price_bucket['increment'] * price_multiplier,
  }
  return new_price_buckets


def get_prices_array_from_price_bucket_list(price_bucket_list):
  """
  Creates an array of prices from a list of price buckets.

  Args:
    price_bucket_list (list): a list of price bucket configuration
  Returns:
    an array of integers (list):
  """
  prices = []
  for price_bucket in price_bucket_list:
    prices.extend(get_prices_array(price_bucket))

  return prices


def get_prices_array(price_bucket):
  """
  Creates an array of price bucket cutoffs in micro-amounts
  from a price_bucket configuration.

  Args:
    price_bucket (object): the price bucket configuration
  Returns:
    an array of integers: every price bucket cutoff from:
      int(round(price_bucket['min'] * 10**6, precision)) to 
      int(round(price_bucket['max'] * 10**6, precision))
  """

  # Arbitrary max CPM to prevent large user errors.
  end_cpm = price_bucket['max']
  start_cpm = price_bucket['min'] if price_bucket['min'] >=0 else 0.00
  increment = price_bucket['increment']
  precision = price_bucket['precision']

  start_cpm_micro_amount = num_to_micro_amount(start_cpm, precision)
  end_cpm_micro_amount = num_to_micro_amount(end_cpm, precision)
  increment_micro_amount = num_to_micro_amount(increment, precision)

  current_cpm_micro_amount = start_cpm_micro_amount
  prices = []
  while current_cpm_micro_amount <= end_cpm_micro_amount:
    prices.append(current_cpm_micro_amount)
    current_cpm_micro_amount += increment_micro_amount
    
  return prices

def get_prices_summary_string(prices_array, precision=2):
  """
  Returns a string preview of the prices array.

  Args:
    prices_array (array): the list of prices in micro-amounts
  Returns:
    a string: a preview of the first few and last few
      items in the array in regular amounts (converted from
      micro-amounts).
  """
  if (len(prices_array) < 6):
    summary = ', '.join(
      [num_to_str(micro_amount_to_num(price), precision)
        for price in prices_array])
  else:
    summary = '{0}, {1}, {2}, ... {3}, {4}, {5}'.format(
        num_to_str(micro_amount_to_num(prices_array[0]), precision),
        num_to_str(micro_amount_to_num(prices_array[1]), precision),
        num_to_str(micro_amount_to_num(prices_array[2]), precision),
        num_to_str(micro_amount_to_num(prices_array[-3]), precision),
        num_to_str(micro_amount_to_num(prices_array[-2]), precision),
        num_to_str(micro_amount_to_num(prices_array[-1]), precision),
      )

  return summary
