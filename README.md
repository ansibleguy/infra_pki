<a href="https://en.wikipedia.org/wiki/Public_key_infrastructure">
  <img src="https://github.com/ansibleguy/infra_pki/blob/latest/docs/pki.svg" alt="Public Key Infrastructure" width="600"/>
</a>

# WORK-IN-PROGRESS!!

# Ansible Role - Public Key Infrastructure (PKI)

Role to provision and manage one or multiple [PKI's](https://en.wikipedia.org/wiki/Public_key_infrastructure) on the target server.

The [EasyRSA script](https://easy-rsa.readthedocs.io/en/latest/) is used as 'backend' to simplify the automation process.

[![Molecule Test Status](https://badges.ansibleguy.net/infra_pki.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/infra_pki.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/infra_pki.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/infra_pki.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://img.shields.io/ansible/role/61525)](https://galaxy.ansible.com/ansibleguy/infra_pki)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F61525%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/infra_pki)


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
  * Python3 '[pexpect](https://pexpect.readthedocs.io/en/stable/)' module as required by the [ansible.builtin.expect](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/expect_module.html) module.
  * OpenSSL


* **Configuration**
  * 


  * **Default config**:
    * Expiration:
      * Root-CA: 20 years
      * Sub-CA: 15 years
      * Certificates: 3 years
 

  * **Default opt-ins**:
    * 


  * **Default opt-outs**:
    * 

## Info


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Note:** If you want to read more about (_x509_) certificates check out the [OpenSSL documentation](https://www.openssl.org/docs/man1.0.2/man5/x509v3_config.html).


* **Note:** If you want to read a good explanation of how 'keyUsage' and 'extendedKeyUsage' are to be used - check out this StackExchange answer: [LINK](https://superuser.com/questions/738612/openssl-ca-keyusage-extension/1248085#1248085)


* **Note:** If you want to know how to manually create a PKI/SubCA's using EasyRSA - check out [@QueuingKoala](https://gist.github.com/QueuingKoala)'s clean example on how to do that: [GitHub Gist](https://gist.github.com/QueuingKoala/e2c1c067a312384915b5) 


* **Warning:** For gained security against CA-compromise you should:

  1. Make sure all your needed Sub-CA's are created by the role
  2. Copy the CA private-key (_${path_base}/ca/pki/private/ca.key_) to an offline medium (_keep redundancy in mind_)
  3. Save the password you used to initialize the CA (_not on the same medium_)
  4. Remove the ca.key file from your Online-system using a 'secure-deletion' tool like 'shred':
  
      ```bash
      shred -vzu -n10 ca.key
      ```


* **Note:** You have multiple options to supply the CA/SubCA/Certificate passwords:

  * if 'save_passwords' is set to true - the saved password will be retrieved after the CA is initialized
  * as inventory variable (_ansible-vault encrypted to be decrypted at runtime_)
  * --extra-vars at runtime
  * if no password was set, the role will prompt for one at runtime


* **Note:** Certificate variables you set on:

  * global level will be inherited by all instances and their sub-ca's
  * instance-level will be inherited by its sub-ca's
  * specific config on instance/subca level will always override the inherited one


* **Note:** You can find scripts for automated certificate-expiration monitoring that can be integrated with monitoring systems like [Zabbix](https://www.zabbix.com/documentation/current/en/manual/discovery/low_level_discovery) at [files/usr/local/bin/monitoring](https://github.com/ansibleguy/infra_pki/tree/latest/files/usr/local/bin/monitoring).


* **Warning:** The CRL-Distribution settings **CANNOT BE CHANGED** easily.

  All existing certificates would have to be re-generated once the settings are changed.


* **Note:** The 'cert_expire' variable of the root-ca will set the runtime of the sub-ca's!


* **Note:** Passwords used for CA/SubCA/Certificate encryption are checked for complexity rules:

  * min. 8 characters long
  * must contain
    * number
    * uppercase letter
    * lowercase letter


* **Note:** Some systems like docker-containers seem to have time-issues when the default timezone is set.

  In that case an error like this will occur: ```start date is invalid, it should be YYMMDDHHMMSSZ or YYYYMMDDHHMMSSZ```


## Usage

### Config

Define the config as needed:

```yaml
pki:
  save_passwords: true  # save ca/sub-ca passwords to file (only root read-access)
  crl_distribution:
    domain: 'crl.ansibleguy.net'  # domain that will be added to all certificates as CRL-distribution-point
    protocol: 'http'
  timezone: 'Europe/Vienna'
  
  vars:
    req_country: 'AT'
    req_province: 'Styria'
    req_org: 'AnsibleGuy'
    req_email: 'pki@ansibleguy.net'
    ca_expire: 9125  # 25 years
    cert_expire: 5475  # 15 years; sub-ca runtime

  instances:
    pki_name:
      ca_cn: 'AnsibleGuy CA'
      vars:
        ca_expire: 5475  # 15 years
        cert_expire: 1095  # 3 years
        key_size: 4096
        digest: 'sha512'

      sub_cas:
        internal:
          ca_cn: 'AnsibleGuy Internal SubCA'
          vars:
            key_size: 2048
          
        vpn:
          ca_cn: 'AnsibleGuy VPN SubCA'
          vars:
            cert_expire: 365
```

This is how the PKI is structured on the filesystem:

  ```bash
  /var/lib/pki/pki_name
  ├── ca
  │   ├── certs_by_serial
  │   ├── inline
  │   ├── issued
  │   ├── private
  │   ├── reqs
  │   └── revoked
  ├── subca_internal
  │   ├── certs_by_serial
  │   ├── inline
  │   ├── issued
  │   ├── private
  │   ├── reqs
  │   └── revoked
  └── subca_vpn
      ├── certs_by_serial
      ├── inline
      ├── issued
      ├── private
      ├── reqs
      └── revoked
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
