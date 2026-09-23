# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 
import boto3
import json

def lambda_handler(event, context):
    contact_data = event['Details']['ContactData']
    
    # The region to filter on - could come from contact attributes,
    # a database lookup, be passed as a parameter, or be based on DTMF entry from caller
    region = event['Details']['Parameters'].get('region', 'america')
    
    # Extract session info from the contact
    connect_client = boto3.client('connect')
    contact = connect_client.describe_contact(
        InstanceId=contact_data['InstanceARN'].split('/')[-1],
        ContactId=contact_data['ContactId']
    )['Contact']
    
    session_arn = contact['WisdomInfo']['SessionArn']
    assistant_id = session_arn.split('/')[1]
    session_id = session_arn.split('/')[2]
    print(session_arn)
    
    # Update session data with the region tag
    # Namesmpace *must* be Custom
    qconnect_client = boto3.client('qconnect')
    qconnect_client.update_session_data(
        assistantId=assistant_id,
        sessionId=session_id,
        namespace='Custom',
        data=[
            {
                'key': 'region',
                'value': {
                    'stringValue': region
                }
            }
        ]
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Session updated with region={region}"})
    }