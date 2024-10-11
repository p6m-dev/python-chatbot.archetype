#!/bin/bash

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --account-id)
        ACCOUNT_ID="$2"
        shift # past argument
        shift # past value
        ;;
        --role)
        ROLE="$2"
        shift # past argument
        shift # past value
        ;;
        --aws-profile)
        PROFILE_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        --local-profile)
        LOCAL_PROFILE_NAME="$2"
        shift # past argument
        shift # past value
        ;;
        *)    # unknown option
        shift # past argument
        ;;
    esac
done

echo "Account ID: $ACCOUNT_ID"
echo "Role: $ROLE"
echo "AWS Profile: $PROFILE_NAME"
echo "Local Profile: $LOCAL_PROFILE_NAME"

ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$ROLE"
SESSION_NAME="my-ai-session"

unset AWS_SECRET_KEY_ID
unset AWS_SECRET_KEY_ID
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY

aws sso login --sso-session p6m --profile $PROFILE_NAME


# Assume role and capture the output
OUTPUT=$(aws sts assume-role --role-arn $ROLE_ARN --role-session-name $SESSION_NAME)

# Use jq to parse the output and extract needed credentials
AWS_ACCESS_KEY_ID=$(echo $OUTPUT | jq -r .Credentials.AccessKeyId)
AWS_SECRET_ACCESS_KEY=$(echo $OUTPUT | jq -r .Credentials.SecretAccessKey)
AWS_SESSION_TOKEN=$(echo $OUTPUT | jq -r .Credentials.SessionToken)

# Write to AWS credentials file
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID" --profile $LOCAL_PROFILE_NAME
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY" --profile $LOCAL_PROFILE_NAME
aws configure set aws_session_token "$AWS_SESSION_TOKEN" --profile $LOCAL_PROFILE_NAME

echo "Credentials updated for $LOCAL_PROFILE_NAME"
echo "to use this profile, run: set AWS_PROFILE=$LOCAL_PROFILE_NAME"