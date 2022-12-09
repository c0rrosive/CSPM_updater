import boto3

stack_name = 'STACK_NAME'
stackset_name = 'stacksetNAME'
AWS_OU = 'ORG_OU'
cloudformation_client = boto3.client('cloudformation')

def get_stack_params():
    response = cloudformation_client.describe_stacks(
        StackName= stack_name
    )
    return(response['Stacks'][0]['Parameters'])

def get_stackset_params():
    response = cloudformation_client.describe_stack_set(
        StackSetName= stackset_name,
    )
    return(response['StackSet']['Parameters'])

def update_stack():
    cloudformation_client.update_stack(
          StackName=stack_name,
          TemplateURL='https://redlock-public.s3.amazonaws.com/cft/rl-read-and-write.template',
          UsePreviousTemplate=False,
          Parameters=stack_params,
          DisableRollback=True,
          Capabilities=[
            'CAPABILITY_NAMED_IAM'
        ]

    )

def update_stackset():
    cloudformation_client.update_stack_set(
        StackSetName=stackset_name,
        TemplateURL='https://redlock-public.s3.amazonaws.com/cft/rl-read-and-write-member.template',
        UsePreviousTemplate=False,
        Parameters=stackset_params,
        Capabilities=[
    'CAPABILITY_NAMED_IAM'
        ],

        OperationPreferences={
            'RegionConcurrencyType':'PARALLEL',
            'FailureTolerancePercentage': 100,
            'MaxConcurrentPercentage': 100
        },


        DeploymentTargets={

            'OrganizationalUnitIds': [
                AWS_OU,
            ],

        },
        PermissionModel='SERVICE_MANAGED',
        AutoDeployment={
            'Enabled': True,
            'RetainStacksOnAccountRemoval': False
        },
        Regions=[
            'us-east-1',
        ]

    )

stack_params = get_stack_params()
stackset_params = get_stackset_params()

def lambda_handler(event, context):
    update_stack()
    update_stackset()









