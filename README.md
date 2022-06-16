Django Example
====

An example [Django](https://www.djangoproject.com) website.

- [X] MIT licensed
- [X] Dependency management with [Poetry](https://python-poetry.org/docs/master/)
- [X] Using a [custom User model](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model))
- [X] Extensible local settings
- [X] Example app using a namespaced URL
- [X] Example model, view, and admin classes
- [X] Example unit tests for models and views
- [ ] Example template tags
- [X] Form-rendering with [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- [X] Usage of [ManifestStaticFilesStorage](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#manifeststaticfilesstorage)
- [ ] Example JS bundling with [esbuild](https://esbuild.github.io)
- [ ] Example [SCSS](https://sass-lang.com) to CSS transpilation
- [X] Code formatting with [Black](https://github.com/psf/black)
- [ ] Dockerfile
- [X] Terraform configuration for AWS with IPv6 support
- [X] Deployment via Ansible
- [X] Support for ARM architecture
- [ ] Emails with [AWS SES](https://aws.amazon.com/ses/)
- [ ] HTTPS support via Let's Encrypt


This projects is tested on Python 3.10, but may support older Python versions.


### Python Dependency Management with Poetry

To install the project's dependencies, first install [Poetry](https://python-poetry.org/docs/#installation) and then run:

    poetry install

Once installed, you can start a virtual environment with:

    poetry shell

To create a `requirements.txt` file for the production dependencies:

    poetry export -f requirements.txt --output requirements.txt --without-hashes


### Customized Bootstrap CSS via SCSS

A custom version of Bootstrap 5.1 can be produced by modifying `custom.scss` in the static folder and then running:

    npm run bootstrap


### Provision AWS Infrastructure via Terraform

Add a key named `django-key` or change the `key_name` variable.

The first run requires initializing with:

    terraform init

Then (or on subsequent runs):

    terraform plan --out=plan.tmp
    terraform apply "plan.tmp"

The configuration is for the `us-west-2` region. You can deploy to other region by changing the `aws_region` and `instance_ami` variables. [Here is the list of available Ubuntu AMIs.](https://cloud-images.ubuntu.com/locator/ec2/)

To destroy the provisioned infrastructure:

    terraform plan -destroy --out=plan.tmp
    terraform apply "plan.tmp"


### Configure Server via Ansible

Add a [deploy key to your Github repository](https://docs.github.com/en/developers/overview/managing-deploy-keys).

Ansible variables that may need to be updated in `site.yml` or in `ansible-playbook` with the `--extra-vars` flag:

- domain
- deploy_key

You can add your AWS access key to your current shell with:

    ssh-add path/to/key.pem

You may need to add your current IP address to the AWS security group.

Ansible deployment is performed with:

    ansible-playbook -e 'ansible_python_interpreter=python3' -i aws_ec2.yml -u ubuntu site.yml

Ansible inventory can be viewed with:

    ansible-inventory -i aws_ec2.yml --list
