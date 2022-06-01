import boto3
def publishStock(url):
    arn = 'arn:aws:sns:us-west-2:729495428235:stock_alert'
    sns_client = boto3.client(
        'sns',
        region_name='us-west-2'
    )
    response = sns_client.publish(
        TopicArn=arn, Message="GPUS in Stock! Link: " + url)

def publishError():
    arn = 'arn:aws:sns:us-west-2:729495428235:code_broken_alert'
    sns_client = boto3.client(
        'sns',
        region_name='us-west-2'
    )
    response = sns_client.publish(
        TopicArn=arn, Message="Code caught an error.")