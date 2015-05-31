
## THIS IS NOT CURRENTLY USED by make_bigfix_awscf_template.py but it will be in the future.

## This is an optional config file to predefine values for the CloudFormation Template
##    This must be renamed to bf_cf_config.py and filled out with proper values.

DEBUG = 1
# BES_ROOT_SERVER_DNS  = "BigFixEval.ORGANIZATION.TLD"
BES_ROOT_SERVER_PORT = "52311"

## Default to Windows, code not written for Linux yet
# BES_ROOT_SERVER_TYPE = "Linux"

# Dev assumes all connected clients are for testing & debugging and should have BigFix / IEM tools deployed. (QnA, etc...)
# Eval, PoC, Dev
BES_ROOT_SERVER_PURPOSE = "Eval"

# MERAKI_MSI_URL = "https://"

