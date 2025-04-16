export DB_HOST="$(echo "$VCAP_SERVICES" | jq --raw-output --arg service_name "example-website-api-database" ".[][] | select(.name == \$service_name) | .credentials.host")"
