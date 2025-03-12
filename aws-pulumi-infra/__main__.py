
import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True
)

# Create an Internet Gateway
internet_gateway = aws.ec2.InternetGateway("my-igw",
    vpc_id=vpc.id
)

# Create a Public Subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True
)

# Create a Private Subnet
private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    map_public_ip_on_launch=False
)

# Create a Route Table for the Public Subnet
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=internet_gateway.id,
    )]
)

# Associate the Public Subnet with the Public Route Table
public_route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id
)

# Create a route table for the private subnet
private_route_table = aws.ec2.RouteTable("private-route-table",
    vpc_id=vpc.id,
    tags={
        "Name": "my-private-route-table"
    }
)

# Allocate an Elastic IP for the NAT Gateway
eip = aws.ec2.Eip("nat-eip", vpc=True)

# Create the NAT Gateway
nat_gateway = aws.ec2.NatGateway("nat-gateway",
    subnet_id=public_subnet.id,
    allocation_id=eip.id,
    tags={
        "Name": "my-nat-gateway"
    }
)

# Create a route in the route table for the NAT Gateway
private_route = aws.ec2.Route("nat-route",
    route_table_id=private_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    nat_gateway_id=nat_gateway.id
)

# Associate the route table with the private subnet
private_route_table_association = aws.ec2.RouteTableAssociation("private-route-table-association",
    subnet_id=private_subnet.id,
    route_table_id=private_route_table.id
)

# Create a Security Group for the Bastion Host
bastion_sg = aws.ec2.SecurityGroup("bastion-sg",
    vpc_id=vpc.id,
    description="Allow SSH from all IPs",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],  # Allow SSH from anywhere
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],  # Allow all outbound traffic
        ),
    ],
)

# Create a Security Group for the MySQL Server
mysql_sg = aws.ec2.SecurityGroup("mysql-sg",
    vpc_id=vpc.id,
    description="Allow SSH from Bastion Host and MySQL from Bastion Host",
    ingress=[
        # Allow SSH from the Bastion Host
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            security_groups=[bastion_sg.id],  # Restrict SSH to the Bastion Host
        ),
        # Allow MySQL from the Bastion Host
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=3306,
            to_port=3306,
            security_groups=[bastion_sg.id],  # Restrict MySQL to the Bastion Host
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],  # Allow all outbound traffic
        ),
    ],
)

# Create the Bastion Host in the Public Subnet
bastion_host = aws.ec2.Instance("bastion-host",
    instance_type="t2.micro",
    ami="ami-0672fd5b9210aa093",  # Replace with your desired AMI ID
    vpc_security_group_ids=[bastion_sg.id],
    subnet_id=public_subnet.id,
    key_name="key-pair-poridhi-poc",  # Replace with your key pair name
    tags={
        "Name": "bastion-host",
    }
)

# Create the MySQL Server in the Private Subnet
mysql_server = aws.ec2.Instance("mysql-server",
    instance_type="t2.micro",
    ami="ami-0672fd5b9210aa093",  # Replace with your desired AMI ID
    vpc_security_group_ids=[mysql_sg.id],
    subnet_id=private_subnet.id,
    key_name="key-pair-poridhi-poc",  # Replace with your key pair name
    tags={
        "Name": "mysql-server",
    }
)

# Output the Public IP of the Bastion Host
pulumi.export("bastion_host_public_ip", bastion_host.public_ip)

# Output the Private IP of the MySQL Server
pulumi.export("mysql_server_private_ip", mysql_server.private_ip)

