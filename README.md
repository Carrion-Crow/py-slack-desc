# py-slack-desc
### py_slack_desc - a simple, script to generate [Slackware](http://www.slackware.com)'s [Slack-descs](https://www.slackwiki.com/Slack-desc). Useful if you write [SlackBuilds](https://www.slackwiki.com/Writing_A_SlackBuild_Script).

### Usage:
```
py_slack_desc.py [-h] [-c] [-n NAME] [-s SHORT [SHORT ...]]
                        [-d DESCRIPTION [DESCRIPTION ...]] [-u URL]

optional arguments:
  -h, --help            show this help message and exit
  -c, --comandline      run script in comandline mode

comandline mode:
  -n NAME, --name NAME  program name
  -s SHORT [SHORT ...], --short SHORT [SHORT ...]
                        program short description (one line)
  -d DESCRIPTION [DESCRIPTION ...], --description DESCRIPTION [DESCRIPTION ...]
                        program description
  -u URL, --url URL     program homepage URL
```

Script will generate slack-desc file in your current working directory.
