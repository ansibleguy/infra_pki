<a href="https://en.wikipedia.org/wiki/Public_key_infrastructure">
  <img src="https://github.com/O-X-L/ansible-role-pki/blob/latest/docs/pki.svg" alt="Public Key Infrastructure" width="600"/>
</a>

# Ansible Role - Public Key Infrastructure (PKI)

Role to provision and manage one or multiple [PKI's](https://en.wikipedia.org/wiki/Public_key_infrastructure) on the target server.

The [EasyRSA script](https://easy-rsa.readthedocs.io/en/latest/) is used as 'backend' to simplify the automation process.

[![Lint](https://github.com/O-X-L/ansible-role-pki/actions/workflows/lint.yml/badge.svg)](https://github.com/O-X-L/ansible-role-pki/actions/workflows/lint.yml)
[![Ansible Galaxy](https://badges.oss.oxl.app/galaxy.badge.svg)](https://galaxy.ansible.com/ui/standalone/roles/oxlorg/pki)

**Molecule Integration-Tests**:

* Status: [![Molecule Test Status](https://badges.oss.oxl.app/infra_pki.molecule.svg)](https://github.com/O-X-L/ansible-role-oxl-cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2) |
[![Functional-Tests](https://github.com/O-X-L/ansible-role-pki/actions/workflows/integration_test_result.yml/badge.svg)](https://github.com/O-X-L/ansible-role-pki/actions/workflows/integration_test_result.yml)
* Logs: [API](https://ci.oss.oxl.app/api/job/ansible-test-molecule-infra_pki/logs?token=2b7bba30-9a37-4b57-be8a-99e23016ce70&lines=1000) | [Short](https://badges.oss.oxl.app/log/molecule_infra_pki_test_short.log) | [Full](https://badges.oss.oxl.app/log/molecule_infra_pki_test.log)

Internal CI: [Tester Role](https://github.com/O-X-L/ansible-role-oxl-cicd) | [Jobs API](https://github.com/O-X-L/github-self-hosted-jobs-systemd)

**Tested:**
* Debian 11
* Debian 12

----

## Install

```bash
# latest
ansible-galaxy role install git+https://github.com/O-X-L/ansible-role-pki

# from galaxy
ansible-galaxy install oxlorg.pki

# or to custom role-path
ansible-galaxy install oxlorg.pki --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

----

## Advertisement

* Need **professional support** using Ansible? Contact us:

  E-Mail: [contact@oxl.at](mailto:contact@oxl.at)

  Tel: [+43 3115 40 900 0](tel:+433115409000)

  Web: [EN](https://www.o-x-l.com) | [DE](https://www.oxl.at)

  Language: German or English

* You want a simple **Ansible GUI**?

  Check-out this [Ansible WebUI](https://github.com/O-X-L/ansible-webui)

----

## Usage

### Config

Define the config as needed:

### Example

You can find a more detailed example here: [Example](https://github.com/O-X-L/ansible-role-pki/blob/latest/Example.md)

#### Minimal setup

```yaml
pki:
  crl_distribution:
    domain: 'crl.oxl.at'

  instances:
    root:
      pwd_ca: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        ...

      sub_cas:
        main:
          pwd_ca: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            ...

          certs:
            server:  # server certificates
              oxl_at:
                cn: 'OXL Website'
                san:
                  dns: ['www.oxl.at', 'oxl.at']
                  ip: '135.181.170.217'
                  uri: 'https://www.oxl.at'

            client:  # client certificates
              workstation1:
                cn: 'OXL Workstation'
```


You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook_pki.yml
```

There is also an 'entrypoint' for managing single certificates - that can be useful if they are automagically managed by other roles.
```bash
# to run it interactively
ansible-playbook -K -D -i inventory/hosts.yml playbook_single_cert.yml
```


There are also some useful **tags** available:
* instances => skip basic tasks but process all PKI-instances (RootCA's)
* subcas => skip basic and instance (RootCA) tasks but process all SubCA tasks
* certs => only process task related to managing certificates
* certs_create => create non-existent certificates
* certs_renew => renew certificates that have the state 'renewed' set
* certs_revoke => revoke certificates that have the state 'revoked' or 'absent' set

To debug errors - you can set the 'debug' variable at runtime:
```bash
# WARNING: Will log passwords!
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```

Note: `--check` mode is not supported by this role as it heavily depends on scripted command-tasks.

----

## Functionality

* **Package installation**
  * OpenSSL


* **Configuration**
  * Usage of a group to allow read-only access to public-keys


  * **Default config**:
    * Paths:
      * PKI base: '/var/local/lib/pki'
      * Script: '/usr/local/sbin/easyrsa'
    * PKI user: 'pki'
    * Read-only group: 'pki_read'
    * **EasyRSA vars**:
      * Expiration:
        * Root-CA: 20 years
        * Sub-CA: 15 years
        * Certificates: 3 years
      * Digest:
        * Root-CA: sha512
        * Sub-CA/Certificates: sha256
      * Algorithm: rsa
      * Key size: 4096
    * Certificates:
      * Don't password-encrypt certificate private-keys
      * Export formats:
        * pkcs12 (_private/<cert>.p12_)
        * certificate chain (_issued/<cert>.chain.crt_)
 

  * **Default opt-ins**:
    * Adding dedicated PKI-user and read-only group
    * Saving CA/Sub-CA/Certificate passwords to files for easier automation
      * See the information below for alternatives
    * Installation and configuration of a Nginx webserver to server CRL's and CA-PublicKey's (_not yet implemented_)


  * **Default opt-outs**:
    * Purging of orphaned (_existing but not configured_) certificates
    * Encryption of certificate private-keys (_non CA/Sub-CA_)

----

## Info


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the [default-config located in the main defaults-file](https://github.com/O-X-L/ansible-role-pki/blob/latest/defaults/main/1_main.yml)!


* **Info:** To make sure the role config 'behaves' as expected - it tested by this role using molecule!

  Per example: The certificate-attributes, file- & directory-permissions & -ownership are checked after generating multiple certificates using multiple Root- & Sub-CA's.

  See [Verification Tests](https://github.com/O-X-L/ansible-role-pki/blob/latest/molecule/default/verify.yml)


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Note:** If you want to read more about PKI's and certificates:

  * The EasyRSA project has a [nice documentation](https://easy-rsa.readthedocs.io/en/latest/intro-to-PKI/)
  * For (_x509_) certificates check out the [OpenSSL documentation](https://www.openssl.org/docs/man1.0.2/man5/x509v3_config.html).
  * If you want to read a good explanation of how 'keyUsage' and 'extendedKeyUsage' are to be used - check out this StackExchange answer: [LINK](https://superuser.com/questions/738612/openssl-ca-keyusage-extension/1248085#1248085)
  * If you want to know how to manually create a PKI/SubCA's using EasyRSA - check out [@QueuingKoala](https://gist.github.com/QueuingKoala)'s clean example on how to do that: [GitHub Gist](https://gist.github.com/QueuingKoala/e2c1c067a312384915b5) 


* **Warning:** For gained security against CA-compromise you should:

  1. Make sure all your needed Sub-CA's are created by the role
  2. Copy the CA private-key (_${path_base}/ca/private/ca.key_) to an offline medium (_keep redundancy in mind_)
  3. Save the password you used to initialize the CA (_not on the same medium_)
  4. Remove the ca.key file from your Online-system using a 'secure-deletion' tool like 'shred':
  
      ```bash
      shred -vzu -n10 ca.key
      ```


* **Note:** You have multiple options to supply the CA/Sub-CA/Certificate passwords:

  * if 'save_passwords' is set to true - the saved password will be retrieved after the CA is initialized
  * as inventory variable (_ansible-vault encrypted to be decrypted at runtime_)
  * --extra-vars at runtime
  * if no password was set, the role will prompt for one at runtime


* **Note:** Certificate variables you set on:

  * global level will be inherited by all instances and their sub-ca's
  * instance-level will be inherited by its sub-ca's
  * specific config on instance/subca level will always override the inherited one


* **Note:** You can find scripts for automated certificate-expiration monitoring that can be integrated with monitoring systems like [Zabbix](https://www.zabbix.com/documentation/current/en/manual/discovery/low_level_discovery) at [files/usr/local/bin/monitoring](https://github.com/O-X-L/ansible-role-pki/tree/latest/files/usr/local/bin/monitoring).


* **Warning:** The CRL-Distribution settings **CANNOT BE CHANGED** easily.

  All existing certificates would have to be re-generated once the settings are changed.


* **Note:** The 'cert_expire' variable of the root-ca will set the runtime of the sub-ca's!


* **Note:** Passwords used for CA/Sub-CA/Certificate encryption are checked for complexity rules:

  * min. 8 characters long
  * must contain
    * number
    * uppercase letter
    * lowercase letter


* **Note:** **Certificates states** can be set to either:

  * 'present' or 'created' to make sure a certificate exists
  * 'absent' or 'revoked' to make sure a certificate does not exist
  * 'renewed' to renew a certificate
