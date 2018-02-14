# pyslackdesc

## Simple script to generate [Slackware](http://www.slackware.com)'s [slack-desc](https://www.slackwiki.com/Slack-desc) files. Useful if you write [SlackBuilds](https://www.slackwiki.com/Writing_A_SlackBuild_Script)

### Usage

    usage: pyslackdesc [-h] [-i] [-o filename] [-v] [-V] [-n name]
                    [-s "short description" ["short description" ...]]
                    [-d "long description" ["long description" ...]] [-u url]

    pyslackdesc - simple, interactive script to generate Slack-desc files

    optional arguments:
    -h, --help            show this help message and exit
    -i, --interactive     run script in interactive mode
    -o filename, --output filename
                            output file (default is slack-desc)
    -v, --verbose         show generated file
    -V, --version         show program's version number and exit
    commandline mode:
    -n name, --name name  program name (single word)
    -s "short description" ["short description" ...], --short "short description"
    ["short description" ...]
                            program short description (one line)
    -d "long description" ["long description" ...], --description "long description"
    ["long description" ...]
                            program long description (up to 6 lines)
    -u url, --url url     program URL
