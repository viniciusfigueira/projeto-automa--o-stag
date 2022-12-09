resource "aws_route53_record" "my-record" {
  zone_id = "ZONE_ID"
  name    = "mydomain.com"
  type    = "A"
  overwrite = true

  alias {
    name                   = "${aws_instance.my-ec2-instance.public_dns}"
    zone_id                = "${aws_instance.my-ec2-instance.zone_id}"
    evaluate_target_health = true
  }
}
