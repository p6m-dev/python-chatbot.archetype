Before running the update-cred-ai.sh, make sure your user role can assume GlueDataConsumer or desired role. 
To do so, update the trust relationship of BlueDataConsumer or the desired role 
```
...
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:sts::<account-id>:<role-name>
            },
            "Action": "sts:AssumeRole"
        }
...        
```
such as the following (when running from a dev machine)

```
...
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:sts::120435196819:assumed-role/AWSReservedSSO_AdministratorAccess_ceec496a277b7895/jessica.chiang@p6m.dev"
            },
            "Action": "sts:AssumeRole"
        }
...        
```

To update local client cred (AWS token), 

```
./update-cred-ai.sh --account-id <account-id> --role <role-name> \
    --aws-profile <aws-profile> \
    --local-profile <local-profile>
./update-cred-ai.sh --account-id 288163945356 --role GlueDataConsumer \
    --aws-profile p6m-dev-dev \
    --local-profile local-profile
```