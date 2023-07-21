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
    # cert_expire: 5475  # 15 years; sub-ca runtime

  instances:
    test_pki:
      ca_cn: 'AnsibleGuy CA'
      vars:
        algo: 'ec'
        curve: 'secp384r1'
        # ca_expire: 5475  # 15 years
        # cert_expire: 1095  # 3 years
        # key_size: 4096
        # digest: 'sha512'
        req_org: 'Ultra Company'
        req_ou: 'IT'

      sub_cas:
        internal:
          ca_cn: 'AnsibleGuy Internal SubCA'

          pwd_ca: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            ...

          pwd_cert: !vault |
            $ANSIBLE_VAULT;1.1;AES256
            ...

          vars:    # vars to inherit to all child-certificates
            req_org: 'Internal Org'
            req_city: 'Graz'
            # key_size: 2048

          # export:  # export formats for all child-certificates
          #   p12: true
          #   p7: true

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
                state: 'renewed'
                cn: 'AnsibleGuy Mail'
                san:
                  email: 'guy@ansibleguy.net'
                req:
                  org: 'AnsibleGuy Mailing'
                  email: 'random@ansibleguy.net'

            client:
              workstation1:
                cn: 'Workstation 1'
                export:
                  pkcs8: true  # creates 'client_workstation.p8'
              test2:
                state: 'absent'

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


### Directory structure

This is how the PKI is structured on the filesystem:

```bash
guy@ansible:~# tree -d /var/local/lib/pki/test_pki
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

### Permissions

```bash
ls -l /var/local/lib/pki/test_pki/                                                
> drwxr-x--- 9 pki pki_read 4096 Jul 21 08:30 ca
> drwxr-x--- 9 pki pki_read 4096 Jul 21 08:35 subca_internal
> drwxr-x--- 9 pki pki_read 4096 Jul 21 08:30 subca_vpn

root@test-ag-infrapki-1:/# ls -l /var/local/lib/pki/test_pki/subca_internal/
> -rw-r----- 1 pki  pki_read  1305 Jul 21 08:27 COPYING.md
> -rw-r----- 1 pki  pki_read   895 Jul 21 08:28 ca.crt
> drwxr-x--- 2 pki  pki_read  4096 Jul 21 08:35 certs_by_serial
> -rw-r----- 1 pki  pki_read   524 Jul 21 08:35 crl.pem
> -rw-r----- 1 pki  pki_read 18092 Jul 21 08:27 gpl-2.0.txt
> -rw-r----- 1 pki  pki        598 Jul 21 08:35 index.txt
> -rw-r----- 1 pki  pki         20 Jul 21 08:35 index.txt.attr
> -rw-r----- 1 pki  pki         20 Jul 21 08:35 index.txt.attr.old
> -rw-r----- 1 pki  pki        517 Jul 21 08:35 index.txt.old
> drwxr-x--- 2 pki  pki       4096 Jul 21 08:28 inline
> drwxr-x--- 2 pki  pki_read  4096 Jul 21 08:35 issued
> -rw-r----- 1 pki  pki       5043 Jul 21 08:27 openssl-easyrsa.cnf
> drwxr-x--- 2 pki  pki       4096 Jul 21 08:35 private
> drwxr-x--- 2 pki  pki       4096 Jul 21 08:35 reqs
> drwxr-x--- 5 pki  pki       4096 Jul 21 08:28 revoked
> -rw-r----- 1 pki  pki         33 Jul 21 08:35 serial
> -rw-r----- 1 pki  pki         33 Jul 21 08:35 serial.old
> -rw-r----- 1 pki  pki        764 Jul 21 08:28 vars
> drwxr-x--- 2 pki  pki       4096 Jul 21 08:28 x509-types

root@test-ag-infrapki-1:/# ls -l /var/local/lib/pki/test_pki/subca_internal/issued/
> -rw-r----- 1 pki pki_read 2738 Jul 21 08:29 client_wkst1.chain.crt
> -rw-r----- 1 pki pki_read  944 Jul 21 08:29 client_wkst1.crt
> -rw-r----- 1 pki pki_read 2807 Jul 21 08:29 email_guy.chain.crt
> -rw-r----- 1 pki pki_read 1013 Jul 21 08:29 email_guy.crt
> -rw-r----- 1 pki pki_read 2856 Jul 21 08:29 server_ansibleguynet.chain.crt
> -rw-r----- 1 pki pki_read 1062 Jul 21 08:29 server_ansibleguynet.crt
> -rw-r----- 1 pki pki_read 2783 Jul 21 08:29 client_workstation1.chain.crt
> -rw-r----- 1 pki pki_read  989 Jul 21 08:29 client_workstation1.crt
> -rw-r----- 1 pki pki_read 2819 Jul 21 08:29 server_tester.chain.crt
> -rw-r----- 1 pki pki_read 1025 Jul 21 08:29 server_tester.crt

root@test-ag-infrapki-1:/# ls -l /var/local/lib/pki/test_pki/subca_internal/private/
> -rw-r----- 1 pki pki  464 Jul 21 08:28 ca.key
> -rw-r----- 1 pki pki  452 Jul 21 08:29 client_workstation1.key
> -rw-r----- 1 pki pki 1882 Jul 21 08:29 client_workstation1.p8
> -rw-r----- 1 pki pki 1882 Jul 21 08:29 client_workstation1.p12
> -rw-r----- 1 pki pki  452 Jul 21 08:29 email_guy.key
> -rw-r----- 1 pki pki 1938 Jul 21 08:29 email_guy.p12
> -rw-r----- 1 pki pki  452 Jul 21 08:29 server_ansibleguynet.key
> -rw-r----- 1 pki pki 1970 Jul 21 08:29 server_ansibleguynet.p12
> -rw-r----- 1 pki pki  452 Jul 21 08:29 server_tester.key
> -rw-r----- 1 pki pki 1946 Jul 21 08:29 server_tester.p12
> -rw-r----- 1 pki pki  288 Jul 21 08:29 server_tester.unencrypted.key
```

### Certificate content

```bash
# ROOT-CA CERTIFICATE
guy@ansible:~# openssl x509 -in /var/local/lib/pki/test_pki/ca/ca.crt -text
> Certificate:
>     Data:
>         Version: 3 (0x2)
>         Serial Number:
>             55:ac:47:4a:9b:7c:7b:23:67:bf:96:cb:0f:c2:b3:01:b0:ba:57:ce
>         Signature Algorithm: ecdsa-with-SHA512
>         Issuer: C = AT, ST = Styria, O = Ultra Company, OU = IT, CN = AnsibleGuy CA, emailAddress = pki@ansibleguy.net
>         Validity
>             Not Before: Jul 21 08:27:01 2023 GMT
>             Not After : Jul 16 08:27:01 2043 GMT
>         Subject: C = AT, ST = Styria, O = Ultra Company, OU = IT, CN = AnsibleGuy CA, emailAddress = pki@ansibleguy.net
>         Subject Public Key Info:
>             Public Key Algorithm: id-ecPublicKey
>                 Public-Key: (384 bit)
>                 pub:
>                     ...
>                 ASN1 OID: secp384r1
>                 NIST CURVE: P-384
>         X509v3 extensions:
>             X509v3 Basic Constraints: 
>                 CA:TRUE
>             X509v3 Subject Key Identifier: 
>                 2E:DC:27:F2:88:A9:A6:F4:2A:DB:53:42:44:E6:64:40:77:56:A8:78
>             X509v3 Authority Key Identifier: 
>                 keyid:2E:DC:27:F2:88:A9:A6:F4:2A:DB:53:42:44:E6:64:40:77:56:A8:78
>                 DirName:/C=AT/ST=Styria/O=Ultra Company/OU=IT/C=AT/ST=Styria/O=Ultra Company/OU=IT/CN=AnsibleGuy CA/emailAddress=pki@ansibleguy.net/emailAddress=pki@ansibleguy.net
>                 serial:55:AC:47:4A:9B:7C:7B:23:67:BF:96:CB:0F:C2:B3:01:B0:BA:57:CE
> 
>             X509v3 Key Usage: 
>                 Certificate Sign, CRL Sign
>             X509v3 CRL Distribution Points: 
> 
>                 Full Name:
>                   URI:http://crl.ansibleguy.net/ca.crl
> 
>             Authority Information Access: 
>                 CA Issuers - URI:http://crl.ansibleguy.net/ca.crt
> 
>     Signature Algorithm: ecdsa-with-SHA512
>          ...
> -----BEGIN CERTIFICATE-----
> ...
> -----END CERTIFICATE-----

# SUB-CA CERTIFICATE

guy@ansible:~# openssl x509 -in /var/local/lib/pki/test_pki/subca_internal/ca.crt -text                       
> Certificate:
>     Data:
>         Version: 3 (0x2)
>         Serial Number:
>             f7:47:59:8f:e3:fa:50:b6:d6:ca:95:cb:fa:e5:d0:cd
>         Signature Algorithm: ecdsa-with-SHA256
>         Issuer: C = AT, ST = Styria, O = Ultra Company, OU = IT, CN = AnsibleGuy CA, emailAddress = pki@ansibleguy.net
>         Validity
>             Not Before: Jul 21 08:28:22 2023 GMT
>             Not After : Jul 20 08:28:22 2026 GMT
>         Subject: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = AnsibleGuy Internal SubCA, emailAddress = pki@ansibleguy.net
>         Subject Public Key Info:
>             Public Key Algorithm: id-ecPublicKey
>                 Public-Key: (384 bit)
>                 pub:
>                     ...
>                 ASN1 OID: secp384r1
>                 NIST CURVE: P-384
>         X509v3 extensions:
>             X509v3 CRL Distribution Points: 
> 
>                 Full Name:
>                   URI:http://crl.ansibleguy.net/ca.crl
> 
>             Authority Information Access: 
>                 CA Issuers - URI:http://crl.ansibleguy.net/ca.crt
> 
>             X509v3 Basic Constraints: 
>                 CA:TRUE
>             X509v3 Subject Key Identifier: 
>                 3C:1E:F4:65:1A:2C:73:DB:F0:FB:C2:0B:14:E9:13:C3:D5:32:70:60
>             X509v3 Authority Key Identifier: 
>                 keyid:2E:DC:27:F2:88:A9:A6:F4:2A:DB:53:42:44:E6:64:40:77:56:A8:78
>                 DirName:/C=AT/ST=Styria/O=Ultra Company/OU=IT/C=AT/ST=Styria/O=Ultra Company/OU=IT/CN=AnsibleGuy CA/emailAddress=pki@ansibleguy.net/emailAddress=pki@ansibleguy.net
>                 serial:55:AC:47:4A:9B:7C:7B:23:67:BF:96:CB:0F:C2:B3:01:B0:BA:57:CE
> 
>             X509v3 Key Usage: 
>                 Certificate Sign, CRL Sign
>     Signature Algorithm: ecdsa-with-SHA256
>          ...
> -----BEGIN CERTIFICATE-----
> ...
> -----END CERTIFICATE-----

# SERVER CERTIFICATE

guy@ansible:~# openssl x509 -in /var/local/lib/pki/test_pki/subca_internal/issued/server_ansibleguynet.crt  -text
> Certificate:
>     Data:
>         Version: 3 (0x2)
>         Serial Number:
>             bd:c3:1f:f0:ee:ad:00:b6:86:7b:7d:dc:56:e2:33:55
>         Signature Algorithm: ecdsa-with-SHA256
>         Issuer: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = AnsibleGuy Internal SubCA, emailAddress = pki@ansibleguy.net
>         Validity
>             Not Before: Jul 21 08:29:01 2023 GMT
>             Not After : Jul 20 08:29:01 2026 GMT
>         Subject: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = AnsibleGuy Website, emailAddress = pki@ansibleguy.net
>         Subject Public Key Info:
>             Public Key Algorithm: id-ecPublicKey
>                 Public-Key: (384 bit)
>                 pub:
>                     ...
>                 ASN1 OID: secp384r1
>                 NIST CURVE: P-384
>         X509v3 extensions:
>             X509v3 CRL Distribution Points: 
> 
>                 Full Name:
>                   URI:http://crl.ansibleguy.net/subca_internal.crl
> 
>             Authority Information Access: 
>                 CA Issuers - URI:http://crl.ansibleguy.net/subca_internal.crt
> 
>             X509v3 Basic Constraints: 
>                 CA:FALSE
>             X509v3 Subject Key Identifier: 
>                 9F:E1:5D:61:A7:65:18:9B:64:5B:69:59:F7:6F:90:90:91:F0:6F:D6
>             X509v3 Authority Key Identifier: 
>                 keyid:3C:1E:F4:65:1A:2C:73:DB:F0:FB:C2:0B:14:E9:13:C3:D5:32:70:60
>                 DirName:/C=AT/ST=Styria/O=Ultra Company/OU=IT/C=AT/ST=Styria/O=Ultra Company/OU=IT/CN=AnsibleGuy CA/emailAddress=pki@ansibleguy.net/emailAddress=pki@ansibleguy.net
>                 serial:F7:47:59:8F:E3:FA:50:B6:D6:CA:95:CB:FA:E5:D0:CD
> 
>             X509v3 Extended Key Usage: 
>                 TLS Web Server Authentication
>             X509v3 Key Usage: 
>                 Digital Signature, Key Encipherment
>             X509v3 Subject Alternative Name: 
>                 DNS:www.ansibleguy.net, DNS:ansibleguy.net, IP Address:135.181.170.217, URI:https://www.ansibleguy.net
>     Signature Algorithm: ecdsa-with-SHA256
>          ...
> -----BEGIN CERTIFICATE-----
> ...
> -----END CERTIFICATE-----

# SERVER CHAIN-CERTIFICATE

guy@ansible:~# cat /var/local/lib/pki/test_pki/subca_internal/issued/server_ansibleguynet.chain.crt
> -----BEGIN CERTIFICATE-----
> ... (ROOT CA)
> -----END CERTIFICATE-----
> -----BEGIN CERTIFICATE-----
> ... (SUB CA)
> -----END CERTIFICATE-----
> -----BEGIN CERTIFICATE-----
> ... (FINAL CERT)
> -----END CERTIFICATE-----

# CLIENT CERTIFICATE

guy@ansible:~# openssl x509 -in /var/local/lib/pki/test_pki/subca_internal/issued/client_workstation1.crt -text
> Certificate:
>     Data:
>         Version: 3 (0x2)
>         Serial Number:
>             c6:d4:fc:17:e6:09:1b:8e:25:07:64:73:0b:0a:05:3b
>         Signature Algorithm: ecdsa-with-SHA256
>         Issuer: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = AnsibleGuy Internal SubCA, emailAddress = pki@ansibleguy.net
>         Validity
>             Not Before: Jul 21 08:29:10 2023 GMT
>             Not After : Jul 20 08:29:10 2026 GMT
>         Subject: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = Workstation 1, emailAddress = pki@ansibleguy.net
>         Subject Public Key Info:
>             Public Key Algorithm: id-ecPublicKey
>                 Public-Key: (384 bit)
>                 pub:
>                     ...
>                 ASN1 OID: secp384r1
>                 NIST CURVE: P-384
>         X509v3 extensions:
>             X509v3 CRL Distribution Points: 
> 
>                 Full Name:
>                   URI:http://crl.ansibleguy.net/subca_internal.crl
> 
>             Authority Information Access: 
>                 CA Issuers - URI:http://crl.ansibleguy.net/subca_internal.crt
> 
>             X509v3 Basic Constraints: 
>                 CA:FALSE
>             X509v3 Subject Key Identifier: 
>                 25:53:D5:C1:A5:0B:22:AC:D9:C7:20:C9:04:67:59:3F:18:39:40:E9
>             X509v3 Authority Key Identifier: 
>                 keyid:3C:1E:F4:65:1A:2C:73:DB:F0:FB:C2:0B:14:E9:13:C3:D5:32:70:60
>                 DirName:/C=AT/ST=Styria/O=Ultra Company/OU=IT/CN=AnsibleGuy CA/emailAddress=pki@ansibleguy.net
>                 serial:F7:47:59:8F:E3:FA:50:B6:D6:CA:95:CB:FA:E5:D0:CD
> 
>             X509v3 Extended Key Usage: 
>                 TLS Web Client Authentication
>             X509v3 Key Usage: 
>                 Digital Signature
>     Signature Algorithm: ecdsa-with-SHA256
>          ...
> -----BEGIN CERTIFICATE-----
> ...
> -----END CERTIFICATE-----

# EMAIL CERTIFICATE

guy@ansible:~# openssl x509 -in /var/local/lib/pki/test_pki/subca_internal/issued/email_guy.crt -text
> Certificate:
>     Data:
>         Version: 3 (0x2)
>         Serial Number:
>             f5:6f:9e:0d:d8:c1:e9:f2:a0:27:c4:f1:c6:2e:bc:31
>         Signature Algorithm: ecdsa-with-SHA256
>         Issuer: C = AT, ST = Styria, L = Graz, O = Internal Org, CN = AnsibleGuy Internal SubCA, emailAddress = pki@ansibleguy.net
>         Validity
>             Not Before: Jul 21 08:29:18 2023 GMT
>             Not After : Jul 20 08:29:18 2026 GMT
>         Subject: C = AT, ST = Styria, L = Graz, O = AnsibleGuy Mailing, CN = AnsibleGuy Mail, emailAddress = random@ansibleguy.net
>         Subject Public Key Info:
>             Public Key Algorithm: id-ecPublicKey
>                 Public-Key: (384 bit)
>                 pub:
>                     ...
>                 ASN1 OID: secp384r1
>                 NIST CURVE: P-384
>         X509v3 extensions:
>             X509v3 CRL Distribution Points: 
> 
>                 Full Name:
>                   URI:http://crl.ansibleguy.net/subca_internal.crl
> 
>             Authority Information Access: 
>                 CA Issuers - URI:http://crl.ansibleguy.net/subca_internal.crt
> 
>             X509v3 Basic Constraints: 
>                 CA:FALSE
>             X509v3 Subject Key Identifier: 
>                 3B:D7:5F:B2:DB:6D:7C:35:3E:A4:68:03:45:4A:E8:D6:28:F3:30:10
>             X509v3 Authority Key Identifier: 
>                 keyid:3C:1E:F4:65:1A:2C:73:DB:F0:FB:C2:0B:14:E9:13:C3:D5:32:70:60
>                 DirName:/C=AT/ST=Styria/O=Ultra Company/OU=IT/CN=AnsibleGuy CA/emailAddress=pki@ansibleguy.net
>                 serial:F7:47:59:8F:E3:FA:50:B6:D6:CA:95:CB:FA:E5:D0:CD
> 
>             X509v3 Extended Key Usage: 
>                 E-mail Protection
>             X509v3 Key Usage: 
>                 Digital Signature, Non Repudiation, Key Encipherment
>             X509v3 Subject Alternative Name: 
>                 email:guy@ansibleguy.net
>     Signature Algorithm: ecdsa-with-SHA256
>          ...
> -----BEGIN CERTIFICATE-----
> ...
> -----END CERTIFICATE-----
```

### Services

```bash
guy@ansible:~# systemctl status pki-crl-updater.service
> * pki-crl-updater.service - Service to update the PKI's Certificate-Revocation-Lists so they don't expire
>      Loaded: loaded (/etc/systemd/system/pki-crl-updater.service; static)
>      Active: inactive (dead) since Fri 2023-07-21 09:03:33 UTC; 2s ago
> TriggeredBy: * pki-crl-updater.timer
>        Docs: https://github.com/ansibleguy/infra_pki
>     Process: 12487 ExecStart=/bin/bash /usr/local/sbin/pki_crl_update.sh (code=exited, status=0/SUCCESS)
>    Main PID: 12487 (code=exited, status=0/SUCCESS)
>         CPU: 218ms
> 
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12626]: An updated CRL has been created.
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12626]: CRL file: /var/local/lib/pki/test2/ca/crl.pem
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: * Using SSL: openssl OpenSSL 1.1.1n  15 Mar 2022
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: * Using Easy-RSA configuration: /var/local/lib/pki/pki_test/subca_internal/vars
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12697]: Using configuration from /var/local/lib/pki/pki_test/subca_internal/2bc49a42/temp.40772b28
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: Notice
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: ------
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: An updated CRL has been created.
> Jul 21 09:03:33 test-ag-infrapki-1 pki_crl_update[12656]: CRL file: /var/local/lib/pki/pki_test/subca_internal/crl.pem
> Jul 21 09:03:33 test-ag-infrapki-1 systemd[1]: pki-crl-updater.service: Succeeded.

guy@ansible:~# systemctl status backup-pki.service
> * backup-pki.service - Service to create a local backup of the PKI directories
>      Loaded: loaded (/etc/systemd/system/backup-pki.service; static)
>      Active: inactive (dead) since Fri 2023-07-21 09:12:10 UTC; 41s ago
> TriggeredBy: * backup-pki.timer
>        Docs: https://github.com/ansibleguy/infra_pki
>     Process: 12850 ExecStart=/bin/bash -c tar cJf "/var/backups/pki/$$(date +'%Y-%m-%d_%H-%M-%S').tar.xz" /var/local/lib/pki (code=exited, status=0/SUCCESS)
>     Process: 12854 ExecStop=/bin/bash -c chmod 600 /var/backups/pki/*.tar.xz (code=exited, status=0/SUCCESS)
>    Main PID: 12850 (code=exited, status=0/SUCCESS)
>         CPU: 51ms
> 
> Jul 21 09:12:10 test-ag-infrapki-1 systemd[1]: Started Service to create a local backup of the PKI directories.
> Jul 21 09:12:10 test-ag-infrapki-1 pki_backup[12850]: tar: Removing leading / from member names
> Jul 21 09:12:10 test-ag-infrapki-1 systemd[1]: backup-pki.service: Succeeded.


guy@ansible:~# ls -l /var/backups/pki/
> -rw------- 1 root root 47392 Jul 21 09:12 2023-07-21_09-12-10.tar.xz
```
