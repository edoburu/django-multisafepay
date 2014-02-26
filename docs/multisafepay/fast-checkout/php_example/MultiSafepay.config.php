<?php

define('MSP_TEST_API',     true); // seperate testaccount needed
define('MSP_ACCOUNT_ID',   '');
define('MSP_SITE_ID',      '');
define('MSP_SITE_CODE',    '');

define('BASE_URL', ($_SERVER['SERVER_PORT'] == 443 ? 'https://' : 'http://') . $_SERVER['SERVER_NAME'] . ':' . $_SERVER['SERVER_PORT'] . dirname($_SERVER['SCRIPT_NAME']) . "/");

?>