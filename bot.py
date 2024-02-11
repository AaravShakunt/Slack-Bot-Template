import slack
from typing import List, Dict
import keys

class SlackHelper:
    def __init__(self, token: str):
        self.client = slack.WebClient(token=token)

    def send_message(self, channel: str, message: str) -> List:
        return self.client.chat_postMessage(channel=channel, text=message)

    def list_all_channels(self) -> List[Dict]:
        return self.client.conversations_list(types="public_channel,private_channel", exclude_archived=True)["channels"]

    def read_all_messages(self, channel: str) -> list:
        messages = []
        latest = None

        while True:
            # Fetch messages in batches using the conversations_history method
            response = self.client.conversations_history(channel=channel, latest=latest, limit=1000)

            if not response["ok"]:
                # Handle error, print a message, or raise an exception as needed
                print(f"Error fetching messages: {response['error']}")
                break

            # Add fetched messages to the list
            messages.extend(response["messages"])

            # Check if there are more messages to fetch
            if not response["has_more"]:
                break

            # Set the latest timestamp for the next batch
            latest = messages[-1]["ts"]

        return messages

def main():
    slack_helper = SlackHelper(token=keys.SLACK_KEY)

    # Example usage

    slack_helper.send_message(channel="client-tester1", message="Test Message")
    
    for data in slack_helper.list_all_channels():
        print(data["name"])
    
    all_messages = slack_helper.read_all_messages(channel="C03SMDRPARG")

    for message in all_messages:
        print(message['text'])

if __name__ == "__main__":
    main()
