import requests
import json
import time
from datetime import datetime
from config import (
    user_auth_token,
    recon_report_load_webhook,
    recon_report_update_webhook,
)


def get_slack_messages(token, channel_id, limit=100):
    """
    Retrieves messages from a Slack channel.

    Parameters
    ----------
    token : str
        The Slack user authentication token.
    channel_id : str
        The ID of the Slack channel from which to retrieve messages.
    limit : int, optional
        The maximum number of messages to retrieve. Defaults to 100.

    Returns
    -------
    list
        A list of message objects retrieved from the Slack channel.
    """
    url = "https://slack.com/api/conversations.history"

    headers = {"Authorization": f"Bearer {token}"}

    params = {"channel": channel_id, "limit": limit}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200 and response.json().get("ok"):
        return response.json().get("messages", [])
    else:
        print(f"Failed to fetch messages: {response.status_code}, {response.text}")
        return []


def delete_slack_message(token, channel_id, ts):
    """
    Deletes a specific message from a Slack channel based on its timestamp.

    Parameters
    ----------
    token : str
        The Slack user authentication token.
    channel_id : str
        The ID of the Slack channel from which to delete the message.
    ts : str
        The timestamp of the message to be deleted.

    Returns
    -------
    None
    """
    url = "https://slack.com/api/chat.delete"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    payload = {"channel": channel_id, "ts": ts}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200 and response.json().get("ok"):
        print(f"Message {ts} deleted successfully")
    else:
        print(f"Failed to delete message {ts}: {response.status_code}, {response.text}")


def delete_all_messages(channel_id):
    """
    Deletes all messages from a specified Slack channel.

    This function retrieves all messages from the given Slack channel and
    deletes each message one by one using its timestamp. A delay is added
    between deletions to avoid rate limiting.

    Parameters
    ----------
    channel_id : str
        The ID of the Slack channel from which to delete all messages.

    Returns
    -------
    None
    """
    global user_auth_token
    messages = get_slack_messages(user_auth_token, channel_id)

    for message in messages:
        ts = message["ts"]
        delete_slack_message(user_auth_token, channel_id, ts)
        time.sleep(0.1)  # To avoid rate limiting


def send_slack_message(
    processname, filename, timestamp, status, logfile_loc, exception=None
):
    """
    Sends a Slack message to a specified webhook with information about a
    processed report.

    Parameters
    ----------
    processname : str
        The name of the process that processed the report, either
        'recon_report_load' or 'recon_report_update'.
    filename : str
        The name of the report file that was processed.
    timestamp : str
        The timestamp of the report file, if not provided, the current
        timestamp will be used.
    status : str
        The status of the report file, either 'Success' or 'Error'.
    logfile_loc : str
        The location of the log file for the report.
    exception : str, optional
        The exception message if the report failed, if not provided, no
        exception section will be added.

    Returns
    -------
    None
    """
    if processname == "recon_report_load":
        webhook_url = recon_report_load_webhook
    elif processname == "recon_report_update":
        webhook_url = recon_report_update_webhook

    # Set the color based on the status
    if status == "Success":
        color = "#36a64f"  # Green for success
    else:
        color = "#ff0000"  # Red for error

    # Use provided timestamp or generate current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Base payload structure
    payload = {
        "attachments": [
            {
                "color": color,  # Color for the border of the message
                "blocks": [
                    {"type": "divider"},  # Divider block to add space between messages
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"New File Detected: *`{filename}`*",
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"Status: *`{status}`*"},
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"TimeStamp: *`{timestamp}`*",
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"Log: *`{logfile_loc}`*"},
                    },
                ],
            }
        ]
    }

    # Add the exception section if status is 'Error' and exception is provided
    if status == "Error" and exception:
        payload["attachments"][0]["blocks"].append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Exception:* ```{exception}```"},
            }
        )

    # Add another divider at the end
    payload["attachments"][0]["blocks"].append({"type": "divider"})

    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, headers=headers, json=payload)

    if response.status_code == 200:
        pass
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
