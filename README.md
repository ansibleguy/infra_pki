<a href="https://en.wikipedia.org/wiki/Public_key_infrastructure">
  <img src="https://github.com/ansibleguy/infra_pki/blob/latest/docs/pki.svg" alt="Public Key Infrastructure" width="600"/>
</a>

# WORK-IN-PROGRESS!!

# Ansible Role - Public Key Infrastructure (PKI)

Role to provision and manage one or multiple [PKI's](https://en.wikipedia.org/wiki/Public_key_infrastructure) on the target server.

The [EasyRSA script](https://easy-rsa.readthedocs.io/en/latest/) is used as 'backend' to simplify the automation process.

# REPLACE: GALAXY_ID & ROLE

[![Molecule Test Status](https://badges.ansibleguy.net/infra_pki.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_pki.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_pki.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_pki.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://img.shields.io/ansible/role/GALAXY_ID)](https://galaxy.ansible.com/ansibleguy/infra_pki)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2FGALAXY_ID%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_pki)


**Tested:**
* Debian 11

## Install

```bash
ansible-galaxy install ansibleguy.infra_pki

# or to custom role-path
ansible-galaxy install ansibleguy.infra_pki --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

## Functionality

* **Package installation**
  * Ansible dependencies (_minimal_)


* **Configuration**
  * 


  * **Default config**:
    * 
 

  * **Default opt-ins**:
    * 


  * **Default opt-outs**:
    * 

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Note:** If you want to read a good explanation of how 'keyUsage' and 'extendedKeyUsage' is to be used - check out this StackExchange answer: [LINK](https://superuser.com/questions/738612/openssl-ca-keyusage-extension/1248085#1248085)


## Setup

For this role to work - you must install its dependencies first:

```
ansible-galaxy install -r requirements.yml
```


## Usage

### Config

Define the config as needed:

```yaml
pki:
  instances:
    internal:
      ca:
      sub_cas:
```

You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* 
*

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
