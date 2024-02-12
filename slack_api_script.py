import os
# from slack_sdk import WebClient
import requests
import csv

# Slack token set in zshrc
slack_token = os.environ["SLACK_API_TOKEN"]

# Specify the channel ID
channel_id = "CVCFBQLB1"
limit=1000


# Retrieve all messages that mention from the x-eng channel
response = requests.get(
    f"https://slack.com/api/conversations.history?channel={channel_id}&limit={limit}",
    headers={"Authorization": f"Bearer {slack_token}"}
)
data = response.json()

if not data["ok"]:
    print(f"Error: {data['error']}")
else:
    messages = data["messages"]
    print(f"Number of messages in the channel: {len(messages)}")

messages = data["messages"]

# # Filter messages with mentions
mentions = []
timestamps = []
# Iterate through the object returning all the conversations and filter it down to the messages that mention qta
for message in messages:
    if "@quick-tech-answers" in message["text"]:
        mention_data = {
            "questions": message["text"].replace("<!subteam^S054JNQRGPP|@quick-tech-answers>", "").strip(),
            "timestamp": message["ts"],
            "thread": []
        }
        timestamps.append(message['ts'])
        mentions.append(mention_data)
        
# Iterate through the mentions object and make a call to retrieve the thread history for each mention
for response in mentions: 
    individualMessageResponse = requests.get(
        f"https://slack.com/api/conversations.replies?channel={channel_id}&ts={response['timestamp']}",
        headers={"Authorization": f"Bearer {slack_token}"},
    )
    data = individualMessageResponse.json()["messages"]
    # Push each thread until thread array execpt the original message at index 0
    for index, message in enumerate(data):
        if index > 0:
            response["thread"].append(message["text"])
    # Join the thread list so we just return a newline separated string for better readability
    s = "\n\n"        
    response["thread"] = s.join(response["thread"])

# Save object to csv file
with open('questions.csv', 'w') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames =["questions", "thread"], extrasaction='ignore') 
    writer.writeheader() 
    writer.writerows(mentions) 

