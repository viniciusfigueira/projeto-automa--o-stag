import boto3

ec2 = boto3.client('ec2')

TAG_KEY="Name"
TAG_VALUE="banco"
AMI_ID="ami-0d5bf08bc8017c83b"
response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['banco']
        },
        {
            'Name': 'instance-state-code',
            'Values': ['16']
        },
    ]
)

if len(response['Reservations']) > 0:
    # Existe uma instância EC2 com o nome "banco".
    # Você pode prosseguir com a exclusão e criação de uma nova instância.
    # Obtenha o ID da instância EC2 com o nome "banco"
    instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

    # Exclua a instância EC2 com o ID obtido
    print("Excluindo maquina atual para a criação de uma nova máquina")

    ec2.terminate_instances(
    InstanceIds=[instance_id]
    )

    # Crie uma nova instância EC2 usando a mesma AMI
    new_instance= ec2.run_instances(
    ImageId=AMI_ID,
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1
    )
    #Consultando valores
    instance_id = new_instance['Instances'][0]['InstanceId']
        
    # Adicione a tag para a nova instancia
    ec2.create_tags(Resources=[instance_id],
                Tags=[{'Key': TAG_KEY, 'Value': TAG_VALUE}])
    
    print(f'Created instance with ID: {instance_id} and added tag: {TAG_KEY}={TAG_VALUE}')
    
    #Consultando Ip da Instância
    instance_info = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = instance_info['Reservations'][0]['Instances'][0]['PublicIpAddress']

    route53 = boto3.client('route53')

    response = route53.change_resource_record_sets(
        HostedZoneId='Z0258487VDOF3ZBHBHJO',
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'site.viniciuslabs.com',
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': public_ip
                            },
                        ]
                    }
                },
            ]
        }
    )

    print('Ip alterado na rota DNS - Route53. Novo IP:',public_ip) 
else:
    print("Não existe instâncias com a Tag (Banco), criando máquina...")


    # Crie uma nova instância EC2 usando a mesma AMI
    response_new = ec2.run_instances(
    ImageId=AMI_ID,
    InstanceType="t3.micro",
    MinCount=1,
    MaxCount=1
    # Adicione aqui as opções desejadas, como tipo de instância, tamanho da EBS, etc.
    )
    #Consultando id da instancia
    instance_id = response_new['Instances'][0]['InstanceId']
    
    # Adicione a tag para a nova instancia
    ec2.create_tags(Resources=[instance_id],
                Tags=[{'Key': TAG_KEY, 'Value': TAG_VALUE}])

    print(f'Created instance with ID: {instance_id} and added tag: {TAG_KEY}={TAG_VALUE}')
    
    #Consultando Ip da Instância
    instance_inf = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip_new = instance_inf['Reservations'][0]['Instances'][0]['PublicIpAddress']
    

    route53 = boto3.client('route53')

    response = route53.change_resource_record_sets(
        HostedZoneId='Z0258487VDOF3ZBHBHJO',
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'site.viniciuslabs.com',
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': public_ip_new
                            },
                        ]
                    }
                },
            ]
        }
    )
    print('Ip alterado na rota DNS - Route53. Novo IP:',public_ip_new) 
    