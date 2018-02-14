# pyslackdesc

## Simple script to generate [Slackware](http://www.slackware.com)'s [slack-desc](https://www.slackwiki.com/Slack-desc) files. Useful if you write [SlackBuilds](https://www.slackwiki.com/Writing_A_SlackBuild_Script)

### Usage

    usage: pyslackdesc [-h] [-i] [-o filename] [-V] [-n name]
                    [-s "short description" ["short description" ...]]
                    [-d "long description" ["long description" ...]] [-u url]

    optional arguments:
    -h, --help            show this help message and exit
    -i, --interactive     Run script in interactive mode
    -o filename, --output filename
                            Output file (default is slack-desc)
    -v, --verbose         Show generated file
    -V, --version         show program's version number and exit

    commandline mode:
    -n name, --name name  Program name (single word)
    -s "short description" ["short description" ...], --short "short description" ["short description" ...]
                            Program short description (one line)
    -d "long description" ["long description" ...], --description "long description" ["long description" ...]
                            Program description
    -u url, --url url     Program homepage URL
