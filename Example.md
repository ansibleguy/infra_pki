# Extended PKI Example

## Config

For all available options - see the [default-config located in the main defaults-file](https://github.com/ansibleguy/infra_pki/blob/latest/defaults/main/1_main.yml)!

```yaml
pki:
  manage:
    users: true  # if set to false - the users and groups will need to be created BEFORE running the initialization
  save_passwords: true  # save ca/sub-ca passwords to file (only root read-access)

  crl_distribution:
    domain: 'crl.ansibleguy.net'  # domain that will be added to all certificates as CRL-distribution-point

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

          pwd_ca: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            ...

          pwd_cert: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            ...

          vars:
            key_size: 2048

          export:  # different formats to export certificates to
            p12: true
            p7: true

          certs:
            server:  # server certificates
              ansibleguy_net:
                cn: 'AnsibleGuy Website'
                san:  # subject-alternative-names
                  dns: ['www.ansibleguy.net', 'ansibleguy.net']
                  ip: '135.181.170.217'
                  uri: 'https://www-ansibleguy.net'

              tester:
                cn: 'AnsibleGuy Test Server'
                san:
                  dns: 'test.ansibleguy.net'
                export:
                  unencrypted: true  # creates 'server_tester.unencrypted.key'

              old:
                state: absent  # present/created/renewed/revoked/absent

            email:  # mail certificates
              guy:
                cn: 'AnsibleGuy Mail'
                san:
                  email: 'guy@ansibleguy.net'

        vpn:
          ca_cn: 'AnsibleGuy VPN SubCA'
          vars:
            cert_expire: 365

          certs:
            client:  # client certificates
              workstation1:
                cn: 'AnsibleGuy Workstation 1'
```

----

## Outcome

This is how the PKI is structured on the filesystem:

```bash
  /var/local/lib/pki/pki_name
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
