
# https://github.com/cloudtools/troposphere
# https://gist.github.com/jgstew/aff5da6a34c82e60fc75
# https://github.com/cloudtools/troposphere/blob/master/examples/VPC_single_instance_in_subnet.py

# region=us-west-1
# shutdown behavoir = stop
# Protect against accidental termination
from troposphere import GetAtt, Parameter, Output, Ref, Tags, Template

import troposphere.ec2 as ec2

if 0:
    from bf_cf_config import *

def make_bigfix_awscf_template():
    template = Template()

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
    print ""
    strResult = make_bigfix_awscf_template()
    print( strResult )
    print ""
    
    # http://stackoverflow.com/questions/15491417/how-to-overwrite-a-file-in-python
    f=open("bf_cf.template.json",'w')
    f.write(strResult+'\n')
    f.close();
