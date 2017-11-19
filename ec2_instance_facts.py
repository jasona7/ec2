#!/usr/bin/python
#
# Bla bla bla i am a license fear me

DOCUMENTATION = '''
---
module: ec2_instance_facts
short_description: Gather facts about ec2 VPC in AWS
description:
    - Gather facts about ec2 VPC in AWS
version_added: "2.0"
author: ""
options:
  instance_id:
    description:
      - A list of instance_ids to gather facts about
    required: false
    default: null
  region:
    description:
      - The aws region
    required: false
    default: null
    aliases: [ 'aws_region', 'ec2_region' ]
extends_documentation_fragment: aws
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.
# Gather facts about ec2 instances
- ec2_instance_facts:
    instance_ids:
      - i-58d6da22
      - i-58d6da23
    region: us-west-7
'''

try:
    import boto.ec2
    from boto.exception import BotoServerError
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

def get_ec2_instance_info(instance):
    ec2_instance_info = {
        'ami_launch_index' : instance.ami_launch_index,
        'architecture' : instance.architecture,
        'instance_type' : instance.instance_type,
        'id' : instance.id,
        'image_id' : instance.image_id,
        'kernel' : instance.kernel,
        'key_name' : instance.key_name,
        'launch_time' : instance.launch_time,
        'platform' : instance.platform,
        'private_dns_name' : instance.private_dns_name,
        'private_ip_address' : instance.private_ip_address,
        'public_dns_name' : instance.public_dns_name,
        'public_ip_address' : instance.ip_address,
        'region' : instance.region.name,
        'root_device_name' : instance.root_device_name,
        'root_device_type' : instance.root_device_type,
        'state' : instance.state,
        'subnet_id' : instance.subnet_id,
        'tags' : instance.tags,
        'vpc_id' : instance.vpc_id,
    }
    return ec2_instance_info

def list_ec2_instance_facts(connection, module):
    ec2_instance_ids = module.params.get("instance_ids")
    ec2_instance_info_array = []

    try:
        all_ec2_instances = connection.get_only_instances(instance_ids=ec2_instance_ids)
    except BotoServerError as e:
        module.fail_json(msg=e.message)

    for instance in all_ec2_instances:
        ec2_instance_info_array.append(get_ec2_instance_info(instance))

    module.exit_json(ec2_instances=ec2_instance_info_array)

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            instance_ids = dict(default=None, type='list')
        )
    )

    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_BOTO:
        module.fail_json(msg='boto required for this module')

    region, ec2_url, aws_connect_params = get_aws_connection_info(module)

    if region:
        try:
            connection = connect_to_aws(boto.ec2, region, **aws_connect_params)
        except (boto.exception.NoAuthHandlerFound, StandardError), e:
            module.fail_json(msg=str(e))
    else:
        module.fail_json(msg="region must be specified")

    list_ec2_instance_facts(connection, module)

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
