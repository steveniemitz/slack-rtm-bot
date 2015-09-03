# slack-rtm-bot

[Slack](https://slack.com/) [RTM](https://api.slack.com/rtm) bot.

## Setup

    pip install slack-rtm-bot

## Usage

    SLACK_RTM_BOT_API_TOKEN="foobar" slack-rtm-bot

To use a different settings file, copy
[`settings_local.py`](slack_rtm_bot/settings_local.py) to some
`/path/to/settings_local.py`, and set `SLACK_RTM_BOT_SETTINGS_FILE`:

    SLACK_RTM_BOT_SETTINGS_FILE="/path/to/settings_local.py" slack-rtm-bot

## License

Licensed under the [MIT License](http://www.opensource.org/licenses/MIT).
