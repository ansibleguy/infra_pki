#!/usr/bin/env bash

# ansibleguy.infra_pki
# script for certificate expiration-checking - can be used by monitoring systems like Zabbix

set -euo pipefail

CERT="$1"

expiration_date=$(openssl x509 -in "$CERT" -noout -dates | grep notAfter | cut -d '=' -f2)
expiration_ts=$(date --date="$expiration_date" +'%s')
current_ts=$(date +'%s')

seconds_left=$((expiration_ts - current_ts))
days_left=$((seconds_left / 86400))

echo "$days_left"
