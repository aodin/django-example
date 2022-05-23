Django Example
====

An example [Django](https://www.djangoproject.com) website.

- [x] Using a [custom User model](https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model)
- [x] Extensible local settings
- [x] Form-rendering with [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [x] [ManifestStaticFilesStorage](https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#manifeststaticfilesstorage)
- [ ] Dependency management with [Poetry](https://python-poetry.org/docs/master/)
- [ ] Emails with [AWS SES](https://aws.amazon.com/ses/)
- [ ] Dockerfile
- [x] Deployment via Ansible
- [x] Support ARM architecture
- [x] Terraform configuration for deploy to AWS with IPv6 support
- [ ] HTTPS support via Let's Encrypt


### Provision AWS Infrastructure via Terraform

Add a key named `django-key` or change the `key_name` variable.

The first run requires initializing with:

    terraform init

Then - or on subsequent runs:

    terraform plan --out=plan.tmp
    terraform apply "plan.tmp"


The configuration is for the `us-west-2` region. You can deploy to other region by changing the `aws_region` and `instance_ami` variables. [Here is the list of available Ubuntu AMIs.](https://cloud-images.ubuntu.com/locator/ec2/)


### Configure Server via Ansible

Add a [deploy key to your Github repository](https://docs.github.com/en/developers/overview/managing-deploy-keys).

Ansible variables that may need to be updated in `site.yml` or in `ansible-playbook` with the `--extra-vars` flag:

- domain
- deploy_key

You can add your AWS access key to your current shell with:

    ssh-add path/to/key.pem

Ansible deployment is performed with:

    ansible-playbook -e 'ansible_python_interpreter=python3' -i aws_ec2.yml -u ubuntu site.yml

Ansible inventory can be viewed with:

    ansible-inventory -i aws_ec2.yml --list
