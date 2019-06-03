#!/usr/bin/env python

import logging

from googleads import ad_manager

import settings
import dfp.get_orders
from dfp.client import get_client
from dfp.exceptions import (
  MissingSettingException
)


logger = logging.getLogger(__name__)


def get_line_item_names_by_order_id(order_id):
  """
  Gets all line item names in an order.

  Args:
    order_id (int): the id of the DFP order
  Returns:
    a DFP placement object
  """

  dfp_client = get_client()
  line_item_service = dfp_client.GetService('LineItemService', version='v201811')

  # Create a statement to select line items.
  statement = (ad_manager.StatementBuilder(version='v201811')
               .Where('orderId = :orderId')
               .WithBindVariable('orderId', order_id))

  response = line_item_service.getLineItemsByStatement(statement.ToStatement())

  if 'results' not in response or len(response['results']) < 1:
    return []

  found_line_item_names = []
  line_items = response['results']
  for line_item in line_items:
    found_line_item_names.append(line_item['name'])

  logger.info(u'OrderId "{order_id}" has {num} existing line_items.'.format(
    order_id=order_id, num=len(line_items))
  )

  return found_line_item_names


def main():
  """
  Loads order name from settings and fetch line items from DFP.

  Returns:
    None
  """  

  order_name = getattr(settings, 'DFP_ORDER_NAME', None)
  if order_name is None:
    raise MissingSettingException('DFP_ORDER_NAME')

  existing_order = dfp.get_orders.get_order_by_name(order_name)

  existing_order_id = existing_order['id']
  print(get_line_item_names_by_order_id(existing_order_id))


if __name__ == '__main__':
  main()
