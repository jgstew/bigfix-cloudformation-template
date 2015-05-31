
# https://forum.bigfix.com/t/automate-bigfix-evaluation-setup-on-aws-free-tier/13438
# https://github.com/jgstew/bigfix-cloudformation-template
# https://github.com/cloudtools/troposphere
# https://github.com/cloudtools/troposphere/blob/master/examples/VPC_single_instance_in_subnet.py
# http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resources-section-structure.html

# region=us-west-1
# shutdown behavior = stop
# Protect against accidental termination
from troposphere import GetAtt, Parameter, Output, Ref, Tags, Template
from troposphere import cloudformation
import troposphere.ec2 as ec2
import os.path
import boto.cloudformation

## the following define the default behavior
##   these values should be overriden using the bf_cf_config.py file
DEBUG = 0
BES_ROOT_SERVER_TYPE = "Windows"

# if bf_cf_config.py exists, import it to override / add configuration
if os.path.isfile("bf_cf_config.py"):
    from bf_cf_config import *

def add_meraki_installer(template):
    print "add_meraki_installer(template)"
    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html#aws-resource-init-files
    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/deploying.applications.html
    # https://github.com/cloudtools/troposphere/issues/3
    return "not yet implimented"

# MAIN function
def make_bigfix_awscf_template():
    template = Template()
    
    # http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python
    # http://www.tutorialspoint.com/python/string_endswith.htm
    #   Only run the function to include the Meraki MSI installation if Windows Server + MERAKI_MSI_URL defined properly
    if "Windows" == BES_ROOT_SERVER_TYPE and 'MERAKI_MSI_URL' in globals() and MERAKI_MSI_URL.endswith('/MerakiPCCAgent.msi'):
        add_meraki_installer(template)
        
    template.add_description("""\
BigFix Eval AWS CloudFormation Template within the resource limits of the AWS free tier.  \
**WARNING** This template creates Amazon EC2 & RDS instances. You may be billed \
for the AWS resources used if you create a stack from this template.""")

    template.add_version('2010-09-09')

    ec2_instance = ec2.Instance("BigFixEval")
    ec2_instance.ImageId = "ami-6502e021"
    ec2_instance.InstanceType = "t2.micro"
    
    template.add_resource(ec2_instance)


    template.add_output([
        Output(
            "AZ",
            Description="Availability Zone of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "AvailabilityZone"),
        ),
        Output(
            "PublicDNS",
            Description="Public DNSName of the newly created EC2 instance",
            Value=GetAtt(ec2_instance, "PublicDnsName"),
        ),
    ])

    template.add_parameter(
        Parameter(
            'RootServerDomain',
            Description=' The domain name the BigFix root server will use ',
            Type='String',
            Default='bigfixeval.organization.tld'
        ))

    return template.to_json()


if __name__ == '__main__':
    strResult = make_bigfix_awscf_template()
    
    if DEBUG:
        print ""
        print( strResult )
        print ""
    

    # http://stackoverflow.com/questions/15491417/how-to-overwrite-a-file-in-python
    f=open("bf_cf.template.json",'w')
    f.write(strResult+'\n')
    f.close();
