import boto3
region_name = "us-west-2"
sns_client = boto3.client('sns',region_name=region_name)
arns = sns_client.list_topics()['Topics']
def publishStock(url):
    arn = arns[1]['TopicArn']
    sns_client.publish(TopicArn=arn, Message="GPUS in Stock! Link: " + url)

def publishError():
    arn = arns[0]['TopicArn']
    sns_client.publish(TopicArn=arn, Message="Code caught an error.")
