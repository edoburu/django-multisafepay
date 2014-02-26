<?php
include('MultiSafepay.combined.php');
include('MultiSafepay.config.php');

$msp = new MultiSafepay();

/* 
 * Merchant Settings
 */
$msp->test                         = MSP_TEST_API;
$msp->merchant['account_id']       = MSP_ACCOUNT_ID;
$msp->merchant['site_id']          = MSP_SITE_ID;
$msp->merchant['site_code']        = MSP_SITE_CODE;
$msp->merchant['notification_url'] = BASE_URL . 'notify.php?type=initial';
$msp->merchant['cancel_url']       = BASE_URL . 'index.php';
// optional automatic redirect back to the shop:
// $msp->merchant['redirect_url']     = BASE_URL . 'return.php'; 

/* 
 * Customer Details - supply if available
 */
$msp->customer['locale']           = 'nl';
$msp->customer['firstname']        = 'Jan';
$msp->customer['lastname']         = 'Modaal';
$msp->customer['zipcode']          = '1234AB';
$msp->customer['city']             = 'Amsterdam';
$msp->customer['country']          = 'NL';
$msp->customer['phone']            = '012-3456789';
$msp->customer['email']            = 'test@example.com';

$msp->parseCustomerAddress('Teststraat 21');
// or 
// $msp->customer['address1']         = 'Teststraat';
// $msp->customer['housenumber']      = '21';


 /* 
  * Delivery address - supply if available
  */
  
/*
$msp->delivery['firstname']        = 'Piet';
$msp->delivery['lastname']         = 'Modaal';
$msp->delivery['zipcode']          = '1234AB';
$msp->delivery['city']             = 'Amsterdam';
$msp->delivery['country']          = 'NL';
$msp->delivery['phone']            = '012-3456789';
$msp->delivery['email']            = 'test@example.com';

$msp->parseDeliveryAddress('Teststraat 22a');
*/

/* 
 * Transaction Details
 */
$msp->transaction['id']            = rand(100000000,999999999); // generally the shop's order ID is used here
$msp->transaction['currency']      = 'EUR';
$msp->transaction['amount']        = '56000'; // cents
$msp->transaction['description']   = 'Order #' . $msp->transaction['id'];
$msp->transaction['items']         = '<br/><ul><li>1 x Item1</li><li>2 x Item2</li></ul>';


/* 
 * Shopping cart
 */
$c_item = new MspItem(
   'Test product',
   'Dit is een test product',
    3,
    '12.00',
    'KG',
    '1'
);
$c_item->SetMerchantItemId('SH123TEST');
$msp->cart->AddItem($c_item);

$c_item = new MspItem(
   'Test product 2',
   'Dit is nog een test product',
    2,
    '10.00'
);
$c_item->SetMerchantItemId('SH456TEST');
$msp->cart->AddItem($c_item);


$c_item = new MspItem(
   'Test product 3',
   'Dit is nog een test product',
    4,
    '10.00'
);
$c_item->SetTaxTableSelector('BTW6'); // tax group
$c_item->SetMerchantItemId('SH456TEST');
$msp->cart->AddItem($c_item);


/* 
 * Shipping methods
 */

$ship_1 = new MspFlatRateShipping("TNT - verzending NL", 7);
$filter = new MspShippingFilters();
$filter->AddAllowedPostalArea('NL');
$ship_1->AddShippingRestrictions($filter);
$msp->cart->AddShipping($ship_1);

$ship_2 = new MspFlatRateShipping("TNT - verzending BE", 12);
$filter = new MspShippingFilters();
$filter->AddAllowedPostalArea('BE');
$ship_2->AddShippingRestrictions($filter);
$msp->cart->AddShipping($ship_2);

$ship_3 = new MspFlatRateShipping("TNT - verzending Anders", 25);
$filter = new MspShippingFilters();
$filter->AddExcludedPostalArea('NL');
$filter->AddExcludedPostalArea('BE');
$ship_3->AddShippingRestrictions($filter);
$msp->cart->AddShipping($ship_3);

$ship_4 = new MspPickup("Ophalen", 0);
$msp->cart->AddShipping($ship_4);


/* 
 * Taxes
 */
 
// sets default tax to 21%
// and creates 3 tax-tables (BTW21, BTW6, BTW0)
$msp->setDefaultTaxZones();

/*
  // or create manually

  // add a default rule (21%)
  $rule = new MspDefaultTaxRule('0.21', 'true');
  $msp->cart->AddDefaultTaxRules($rule);
  
  // add an alternative rule (6%) named BTW6, use on item with SetTaxTableSelector('BTW6')
  $table = new MspAlternateTaxTable('BTW6', 'true');
  $rule  = new MspAlternateTaxRule('0.06');
  $table->AddAlternateTaxRules($rule);
  $msp->cart->AddAlternateTaxTables($table);
  
  // add an alternative rule (0%) named BTW0, use on item with SetTaxTableSelector('BTW0')
  $table = new MspAlternateTaxTable('BTW0', 'true');
  $rule  = new MspAlternateTaxRule('0.00');
  $table->AddAlternateTaxRules($rule);
  $msp->cart->AddAlternateTaxTables($table);
*/
      
/* 
 * Custom fields
 */

// standard field
$field = new MspCustomField();
$field->standardField = 'msp_birthday';
$msp->fields->AddField($field);

// custom field for company name
$label = array(
  'nl' => 'Bedrijfsnaam', 
  'en' => 'Company', 
);
$field = new MspCustomField('company', 'textbox', $label);
$error = array(
  'nl' => 'Vul de bedrijfsnaam in', 
  'en' => 'Please enter your company name', 
);
$field->savevalue = 'true';

$validation = new MspCustomFieldValidation('regex', '^[a-zA-Z0-9 ]+$', $error);
$field->AddValidation($validation);
$msp->fields->AddField($field);


// sample field
$field = new MspCustomField('vraag', 'selectbox', 'Vraag');
$field->AddOption('-', '-');
$field->AddOption('1', 'Ja');
$field->AddOption('0', 'Nee');

$validation = new MspCustomFieldValidation('regex', '^[01]$', 'Vraag is leeg');
$field->AddValidation($validation);

$filter = new MspCustomFieldFilter();
$filter->AddAllowedPostalArea('NL');
//$filter->AddExcludedPostalArea('NL');
$field->AddRestrictions($filter);

$msp->fields->AddField($field);

// returns a payment url

$url = $msp->startCheckout();

//echo $msp->request_xml;

if ($msp->error){
  echo "Error " . $msp->error_code . ": " . $msp->error;
} elseif (!$msp->error){
  header("Location: ".$url);
}

// redirect
//header('Location: ' . $url);

?>