[![Build Status](https://travis-ci.org/kmjennison/dfp-prebid-setup.svg?branch=master)](https://travis-ci.org/kmjennison/dfp-prebid-setup)

# Line item creator for Google Ad Manager
An automated line item generator for Google Ad Manager (previously DFP)<br>**Clone this repository** and follow 3 major steps to create 425 line items in Google Ad Manager for AIRIS.
1. Creat Google Credentials
2. Creating a Placement in Google Ad Manager
3. Input Configuration and run the code
<!--## Overview
When setting up Prebid, your ad ops team often has to create [hundreds of line items](http://prebid.org/adops.html) in Google Ad Manager (GAM).

This tool automates setup for new header bidding partners. You define the advertiser, placements or ad units, and Prebid settings; then, it creates an order with one line item per price level, attaches creatives, sets placement and/or ad units, and Prebid key-value targeting.

While this tool covers typical use cases, it might not fit your needs. Check out the [limitations](#limitations) before you dive in.

_Note: Doubleclick for Publishers (DFP) was recently renamed to Google Ad Manager (GAM), so this repository may refer to GAM as DFP._-->

## Create Google Credentials
### Create a Sercvice account key
<!--_You will need credentials to access your GAM account programmatically. This summarizes steps from [GAM docs](https://developers.google.com/ad-manager/docs/authentication) and the Google Ads Python libary [auth guide](https://github.com/googleads/googleads-python-lib)._-->

<!--1. If you haven't yet, sign up for a [GAM account](https://admanager.google.com/).-->
1. Go to the [Google Developers Console Credentials page](https://console.developers.google.com/apis/credentials).
2. On the **Credentials** page, select **Create credentials**, then select **Service account key**.
 ![GDCC_createCredentials] 
3. Click the dropdown menu under **Service account**.
 ![GDCC_CreateServiceAccount] 
4. Select **New service account**
 ![GDCC_NewServiceAccount] 
5. Set up the service account name, leave the role blank, and select JSON key type.
 ![GDCC_SetUpNewServiceAccount] 
6. Click **Create** to download a file containing a `.json` private key. Click **CREATE WITHOUT ROLE** when you see the dialogue.
 ![GDCC_CreateWithoutRole] 
7.  Rename the private key (`[something].json`) to `key.json` and move it to the root of this repository
### Set up Service Account in Google Ad manager
1. Enable API access to Google Ad Manager
   * Sign into your [Google Ad Manager](https://admanager.google.com/). You must have admin rights.
   * In the **Admin** section, select **Global settings**
   * Ensure that **API access** is enabled.
   * Click the **Add a service account user** button.
   ![GAM_AddAServiceAccountUser] 
   * Set up the service account user.
     * Use the service account email for the Google developer credentials you created above.
     * Set the role to "Trafficker".
     * Click **Save**.
     ![GAM_SetUpServiceAccount] 

## Create a Placement in Google Ad Manager

1. Create a Placement in Google Ad manager
   * In the **Inventory** section, select **Ad units**, select **Placements** tab, and click **New placement** button.
   ![GAM_Placement]
   * Give the new placement a name. In the Inventory section, select all the ad units that are specified in the configuration csv file that you previously uploaded to AIRIS
   ![GAM_SetUpNewPlacement]
   * Click **Save**.
## Set Up Configuration and Run the Code
### Set Up google.yaml in the repository
<!--1. Clone this repository.-->

1. From the root of the repository, set up python3 development environment.
2. Run `pip install -r requirements.txt`.
3. Make a copy of `googleads.example.yaml` and name it `googleads.yaml`.
4. In `googleads.yaml`, set the required fields:
   * `application_name` is the name of the Google project you created when creating the service account credentials. It should appear in the top-left of the [credentials page](https://console.developers.google.com/apis/credentials).
   * `network_code` is your GAM network number; e.g., for `https://admanager.google.com/12398712#delivery`, the network code is `12398712`.

### Verify Setup
Let's try it out! From the top level directory, run

`python -m dfp.get_orders`

and you should see all of the orders in your GAM account.

If you see the error message, `ValueError: unknown locale: UTF-8`, please run

`export LC_ALL=en_US.UTF-8`<br>`export LANG=en_US.UTF-8`

and try again.

### Set up **local_settings.py**

1. Make a copy of `local_settings.example.py` and name it `local_settings.py`.
2. Modify the following settings in `local_settings.py`:

Setting | Description | Type
------------ | ------------- | -------------
`DFP_ORDER_NAME` | What you want to call this order | string (e.g., `'dfpordername'`)
`DFP_USER_EMAIL_ADDRESS` | The service account email for the Google developer credentials you created above  | string (e.g., `'email@email.com'`)
`DFP_ADVERTISER_NAME` | The service account name for the Google developer credentials you created above | string (e.g., `'advertisername'`)
`DFP_TARGETED_PLACEMENT_NAMES` | The names of GAM placements you created above | array of strings (e.g., `['placementname']`)
`DFP_PLACEMENT_SIZES` | The creative sizes of all ad units specified in the configuration csv you uploaded | array of objects (e.g., `[{'width': '728', 'height': '90'}]`)
`DFP_CURRENCY_CODE` | New Taiwan Dollar: ‘TWD'<br>United States Dollar: ‘USD’<br> Japanese Yen: ‘JPY’<br>The currency settings is in the Global Settings of Google Ad Manager | string
`DFP_NUM_CREATIVES_PER_LINE_ITEM` | Maximum Ad Units on any given webpage of your website | number

**Run:**

`python -m tasks.add_new_prebid_partner`

After running successfully, you will see this message

`Happy bidding!`

Then, approve the order in [Google Ad Manager](https://admanager.google.com/).
![GAM_Approve] 

*Note: GAM might show a "Needs creatives" warning on the order for ~15 minutes after order creation. Typically, the warning is incorrect and will disappear on its own.*

<!--## Additional Settings

In most cases, you won't need to modify these settings.

Setting | Description | Default
------------ | ------------- | -------------
`DFP_CREATE_ADVERTISER_IF_DOES_NOT_EXIST` | Whether we should create the advertiser with `DFP_ADVERTISER_NAME` in GAM if it does not exist | `False`
`DFP_USE_EXISTING_ORDER_IF_EXISTS` | Whether we should modify an existing order if one already exists with name `DFP_ORDER_NAME` | `False`
`DFP_NUM_CREATIVES_PER_LINE_ITEM` | The number of duplicate creatives to attach to each line item. Due to GAM limitations, this should be equal to or greater than the number of ad units you serve on a given page. | the length of setting `DFP_TARGETED_PLACEMENT_NAMES`
`DFP_CURRENCY_CODE` | The currency to use in line items. | `'USD'`-->

## Limitations

* This tool does not currently support run-of-network line items (see [#16](../../issues/16)). You must target line items to placements, ad units, or both.
* Currently, the names of the bidder code targeting key (`hb_bidder`) and price bucket targeting key (`hb_pb`) are not customizable. The `hb_bidder` targeting key is currently required (see [#18](../../issues/18))
* This tool does not support additional line item targeting beyond placement, ad units, `hb_bidder`, and `hb_pb` values. 
<!--* The price bucketing setting `PREBID_PRICE_BUCKETS` only allows for uniform bucketing. For example, you can create $0.01 buckets from $0 - $20, but you cannot specify $0.01 buckets from $0 - $5 and $0.50 buckets from $5 - $20. Using entirely $0.01 buckets will still work for the custom buckets—you'll just have more line items than you need.-->
* This tool does not modify existing orders or line items, it only creates them. If you need to make a change to an order, it's easiest to archive the existing order and recreate it.

Please consider [contributing](CONTRIBUTING.md) to make the tool more flexible.

[GDCC_createCredentials]: ./images/GDCC_createCredentials.png "Create Credentials"
[GDCC_CreateServiceAccount]: ./images/GDCC_CreateServiceAccount.png "Create Credentials"
[GDCC_NewServiceAccount]: ./images/GDCC_NewServiceAccount.png "New service account"
[GDCC_SetUpNewServiceAccount]: ./images/GDCC_SetUpNewServiceAccount.png "Set Up new service account"
[GDCC_CreateWithoutRole]: ./images/GDCC_CreateWithoutRole.png "Create without role"
[GAM_Placement]: ./images/GAM_Placement.png "New placements"
[GAM_AddAServiceAccountUser]: ./images/GAM_AddAServiceAccountUser.png "Add a service account"
[GAM_SetUpServiceAccount]: ./images/GAM_SetUpServiceAccount.png "Set up a service account"
[GAM_SetUpNewPlacement]: ./images/GAM_SetUpNewPlacement.png "Set up a new placement"
[GAM_Approve]: ./images/GAM_Approve.png "Approve Order"