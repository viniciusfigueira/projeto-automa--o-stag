resource "aws_instance" "my-ec2-instance" {
  ami           = "ami-123456"
  instance_type = "t2.micro"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "My EC2 instance"
  }
}
