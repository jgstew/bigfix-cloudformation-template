
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

## the following define the default behavior
##   these values should be overriden using the bf_cf_config.py file
DEBUG = 0
BES_ROOT_SERVER_TYPE = "Windows"

# if bf_cf_config.py exists, import it to override / add configuration
if os.path.isfile("bf_cf_config.py"):
    from bf_cf_config import *


# MAIN function
def make_bigfix_awscf_template():
    template = Template()
    
    # http://stackoverflow.com/questions/843277/how-do-i-check-if-a-variable-exists-in-python
    # http://www.tutorialspoint.com/python/string_endswith.htm
    #   Only run the function to include the Meraki MSI installation if Windows Server + MERAKI_MSI_URL defined properly
    #   MERAKI_MSI_URL should be defined in the bf_cf_config.py file
    if "Windows" == BES_ROOT_SERVER_TYPE and 'MERAKI_MSI_URL' in globals() and MERAKI_MSI_URL.endswith('/MerakiPCCAgent.msi'):
        meraki_msi_url = MERAKI_MSI_URL
    else:
        meraki_msi_url = ""
        
    template.add_description("""\
BigFix Eval AWS CloudFormation Template within the resource limits of the AWS free tier.  \
**WARNING** This template creates Amazon EC2 & RDS instances. You may be billed \
for the AWS resources used if you create a stack from this template.""")

    template.add_version('2010-09-09')
    
    # define subnet
    
    # define DB Subnet Group
    
    # define RDS instance
    # https://github.com/cloudtools/troposphere/blob/master/troposphere/rds.py#L13
    
    # define EBS volume (to be attached to the EC2 instance)
    
    # define Metadata for EC2 instance
    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html#aws-resource-init-files
    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/deploying.applications.html
    # https://github.com/cloudtools/troposphere/issues/3
    metadata = {
        "AWS::CloudFormation::Init": {
            "config": {
                "packages": {
                    "msi" : {
                        #"awscli" : "https://s3.amazonaws.com/aws-cli/AWSCLI64.msi",
                        "meraki" : meraki_msi_url
                    },
                    
                },
            }
        }
    }
    
    # define EC2 instance with Metadata
    ec2_instance = ec2.Instance("BigFixEval", Metadata=metadata)
    ec2_instance.ImageId = "ami-6502e021"
    ec2_instance.InstanceType = "t2.micro"
    # https://github.com/cloudtools/troposphere/blob/master/troposphere/ec2.py#L134
    #ec2_instance.SubnetId = ""  # Ref(SubnetID)
    
    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-volumes
    # https://github.com/cloudtools/troposphere/blob/master/troposphere/ec2.py#L138
    #ec2_instance.Volumes = ""  # Ref(Volume)
    
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
