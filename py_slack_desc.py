#!/usr/bin/env python3
""" py_slack_desc - a simple script to generate Slackware's Slack-desc """
import textwrap as tw
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--comandline", default=False,
                    help="run script in comandline mode",
                    action="store_true")
cmd_parser = parser.add_argument_group('comandline mode')
cmd_parser.add_argument("-n", "--name", help="program name")
cmd_parser.add_argument("-s", "--short", nargs='+',
                        help="program short description (one line)")
cmd_parser.add_argument("-d", "--description", nargs='+',
                        help="program description")
cmd_parser.add_argument("-u", "--url",
                        help="program homepage URL")

args = parser.parse_args()


def get_pkg_name():
    """ Ask user for package name """
    pkg_name = input("package name (no spaces): ")
    if not pkg_name:
        print("Package name can't be empty. Try again.")
        return get_pkg_name()
    elif ' ' in pkg_name:
        print('Spaces are not allowed in package name. Use "-" instead. Try again.')
        return get_pkg_name()
    return pkg_name


def get_pkg_handy_ruler(pkg_name):
    """ Get a handy ruler """
    ruler_intend = len(pkg_name) * ' '
    ruler_start = '|-----handy-ruler'  # 17 chars
    ruler_extender = (79 - len(ruler_intend + ruler_start) - 1) * '-'
    ruler_end = '|'
    handy_ruler = ruler_intend + ruler_start + ruler_extender + ruler_end
    return handy_ruler


def get_pkg_short_desc(pkg_prefix):
    """ Ask user for package short description """
    pkg_short_desc = input("Package short description (one line) ")
    if not pkg_short_desc:
        print("Package short description can't be empty. Try again.")
        return get_pkg_short_desc(pkg_prefix)
    elif len(pkg_prefix + pkg_short_desc) > 79:
        print("Package short description is too long. Try again.")
        return get_pkg_short_desc(pkg_prefix)
    pkg_short_desc = pkg_prefix + pkg_short_desc
    return pkg_short_desc


def get_pkg_desc():
    """ Ask user for package description """
    pkg_desc = input("Package description: ")
    if not pkg_desc:
        print("Package name can't be empty. Try again.")
        return get_pkg_desc()
    return pkg_desc


def get_pkg_url(pkg_prefix):
    """ Ask user for package homepage """
    pkg_url = input("Package homepage: ")
    if len(pkg_prefix + pkg_url) > 79:
        print("URL is too long. Try again.")
        return get_pkg_url(pkg_prefix)
    return pkg_url


def pkg_desc_warp(pkg_prefix, pkg_desc, pkg_empty_line):
    """ Wrap 'pkg_desc' and ident it with 'pkg_prefix: ' """
    desc_width = (79 - len(pkg_prefix))
    desc_warpper = tw.TextWrapper(
        width=desc_width,
        initial_indent=pkg_prefix,
        subsequent_indent=pkg_prefix)

    pkg_desc = tw.dedent(pkg_desc)
    pkg_desc = desc_warpper.wrap(pkg_desc)

    if len(pkg_desc) > 6:
        print("Package description is to long. Try again.")
        return pkg_desc_warp(pkg_prefix, get_pkg_desc(), pkg_empty_line)
    elif len(pkg_desc) < 6:
        for _ in range(6 - len(pkg_desc)):
            pkg_desc.append(pkg_empty_line)
    return pkg_desc


def slack_desc_constructor(pkg_handy_ruler, pkg_short_desc, pkg_desc,
                           pkg_url, pkg_empty_line):
    """ Build Slack-desc as a list of lines """
    header = [
        "# HOW TO EDIT THIS FILE:",
        '# The "handy ruler" below makes it easier to edit a package description.  Line',
        "# up the first '|' above the ':' following the base package name, and the '|'",
        '# on the right side marks the last column you can put a character in.  You must',
        "# make exactly 11 lines for the formatting to be correct.  It's also",
        "# customary to leave one space after the ':'.",
        ''
    ]
    pkg_slack_desc = []
    pkg_slack_desc.extend(header)
    pkg_slack_desc.append(pkg_handy_ruler)
    pkg_slack_desc.append(pkg_short_desc)
    pkg_slack_desc.append(pkg_empty_line)
    pkg_slack_desc.extend(pkg_desc)
    pkg_slack_desc.append(pkg_empty_line)
    pkg_slack_desc.append(pkg_url)
    pkg_slack_desc.append(pkg_empty_line)
    return pkg_slack_desc


def write_slack_desc(slack_desc):
    """ Finally write file to current directory """
    with open('slack-desc', mode='w') as slack_desc_file:
        for line in slack_desc:
            slack_desc_file.write(line + '\n')


def interactive():
    """ Put everything together """
    # Get package name
    pkg_name = get_pkg_name()
    pkg_prefix = pkg_name + ': '
    pkg_empty_line = pkg_prefix[:-1]

    # Get handy ruler
    pkg_handy_ruler = get_pkg_handy_ruler(pkg_name)

    # Get short description
    pkg_short_desc = get_pkg_short_desc(pkg_prefix)

    # Get package description
    pkg_desc = get_pkg_desc()
    pkg_desc = pkg_desc_warp(pkg_prefix, pkg_desc, pkg_empty_line)

    # Get package URL
    pkg_url = get_pkg_url(pkg_prefix)
    pkg_url = pkg_prefix + pkg_url

    # Construct Slack-desc
    slack_desc = slack_desc_constructor(pkg_handy_ruler, pkg_short_desc,
                                        pkg_desc, pkg_url, pkg_empty_line)

    # Write Slack-desc file
    write_slack_desc(slack_desc)


if __name__ == "__main__":
    if args.comandline:
        pass
    else:
        interactive()
