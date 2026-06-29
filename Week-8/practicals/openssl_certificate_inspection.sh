#!/bin/bash
TARGET="google.com"
PORT=443
OUTPUT_FILE="certificate.pem"

echo "Downloading certificate from $TARGET..."
openssl s_client -connect "$TARGET:$PORT" -showcerts </dev/null 2>/dev/null \
  | openssl x509 -outform PEM > "$OUTPUT_FILE"

echo "Full Certificate Details:"
openssl x509 -in "$OUTPUT_FILE" -text -noout

echo "Summary:"
openssl x509 -in "$OUTPUT_FILE" -noout -issuer
openssl x509 -in "$OUTPUT_FILE" -noout -subject
openssl x509 -in "$OUTPUT_FILE" -noout -dates
