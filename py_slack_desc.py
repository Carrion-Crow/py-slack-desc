import argparse
import os
import sys
import textwrap


def text_warpper(text, prefix, separator):
    """Wraps text

    Parameters:
    ----------
    text : {str}
        Text to be warped
    prefix : {str}
        Defines a name of the program to be used as a prefix for every line of text
    separator : {str}
        Defines the text inserted between prefix and text
    Returns
    -------
    list
        Returns a list of strings (lines)
    """

    pkg_prefix = prefix + separator
    # empty lines need a special care
    if text != '':
        max_line_width = (79 - len(pkg_prefix))
        text_warpper = textwrap.TextWrapper(
            width=max_line_width,
            initial_indent=pkg_prefix,
            subsequent_indent=pkg_prefix)
        warped_text = textwrap.dedent(text)
        warped_text = text_warpper.wrap(warped_text)
        return warped_text
    else:
        # single line doesn't need trailing spaces
        warped_text = pkg_prefix.rstrip()
        # ensure to always return list, not string
        return warped_text.split()


def text_validator(text, one_word=False, one_line=False, six_lines=False, pkg_name=None):
    """Validates the text that makes up the slack-desc file

    Parameters:
    ----------
    text : {str}
        Text for validation
    one_word : {bool}, optional
        Defines if text has to be a single word (the default is False)
    one_line : {bool}, optional
        Defines if text has to be maximally six line long (the default is False)
    six_lines : {bool}, optional
        Defines if text has to be maximally six lines long  (the default is False)
    pkg_name : {str}, optional
        Defines name of program (the default is None)

    Raises
    ------
    ValueError
        Raisers ValueError if text doesn't pass validation

    Returns
    -------
    bool
        True if text passes validation. Otherwise raises an error.
    """

    if not text:
        raise ValueError("Error: Input can't be empty. Try again.")
    elif one_word:
        if (' ' in text):
            raise ValueError("Error: Use one word. Try again.")
        elif (len(text) > 77):
            raise ValueError("Error: Text is too long. Try again.")
    elif one_line:
        if not pkg_name:
            sys.exit("Error: unknown program name.")
        elif (len(pkg_name + text) + 2) > 79:
            raise ValueError(
                "Error: Package short description is too long. Try again.")
    elif six_lines:
        if not pkg_name:
            sys.exit("Error: Unknown program name.")
        elif len(text_warpper(text, pkg_name, ': ')) > 6:
            raise ValueError(
                "Error: Package description is too long. Try again.")
    else:
        return True


def user_input(question, one_word=False, one_line=False, six_lines=False, pkg_name=None):
    """Asks user for input and pass it to validator

    Parameters:
    ----------
    question : {str}
        Content of the question asked to the user
    one_word : {bool}, optional
        Passed to the validator, defines if user input has to be a single word (the default is False)
    one_line : {bool}, optional
        Passed to the validator, defines if user input has to be maximally six line long (the default is False)
    six_lines : {bool}, optional
        Passed to the validator, defines if user input has to be maximally six lines long  (the default is False)
    pkg_name : {str}, optional
        Passed to the validator, defines name of a program (the default is None)

    Returns
    -------
    str
        Returns correct user input
    """

    var_name = input(question)

    try:
        text_validator(var_name, one_word, one_line, six_lines, pkg_name)
    except ValueError as error:
        print(error)
        return user_input(question, one_word, one_line, six_lines, pkg_name)
    else:
        return var_name


def header():
    """Header of slack-build file

    Returns
    -------
    list
        Returns a list of lines
    """

    header = [
        "# HOW TO EDIT THIS FILE:",
        '# The "handy ruler" below makes it easier to edit a package description.  Line',
        "# up the first '|' above the ':' following the base package name, and the '|'",
        '# on the right side marks the last column you can put a character in.  You must',
        "# make exactly 11 lines for the formatting to be correct.  It's also",
        "# customary to leave one space after the ':'.",
        '']
    return header


def handy_ruler(pkg_name):
    """Creates a handy ruler

    Parameters:
    ----------
    pkg_name : {str}
        Name
    Returns
    -------
    [type]
        Defines name of a program
    """

    ruler_intend = len(pkg_name) * ' '
    ruler_start = '|-----handy-ruler'  # 17 chars
    ruler_extender = (79 - len(ruler_intend + ruler_start) - 1) * '-'
    ruler_end = '|'
    handy_ruler = ruler_intend + ruler_start + ruler_extender + ruler_end
    # .split removes whitespaces
    handy_ruler = [handy_ruler]
    return handy_ruler


def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interactive", default=False,
                        help="run script in interactive mode",
                        action="store_true")
    parser.add_argument("-o", "--output", help="output directory")
    cmd_parser = parser.add_argument_group('commandline mode')
    cmd_parser.add_argument("-n", "--name", nargs=1, help="program name")
    cmd_parser.add_argument("-s", "--short", nargs='+',
                            help="program short description (one line)")
    cmd_parser.add_argument("-d", "--description", nargs='+',
                            help="program description")
    cmd_parser.add_argument("-u", "--url", nargs=1,
                            help="program homepage URL")
    args = parser.parse_args()
    return args


def program_dict(cli_mode, args):
    """Populate a dictionary with all lines of slack-desc file

    Parameters:
    ----------
    cli_mode : {bool}
        Dictionary populating mode.
    args : {argparse.Namespace}
        Argparse Namespace
    Returns
    -------
    dict
        Returns a dictionary with all lines of slack-desc file
    """

    program = dict()
    # check mode
    if cli_mode:
        # commandline mode (default)
        program['name'] = text_validator(args.name)
        program['short_desc'] = text_validator(
            args.short, one_line=True, pkg_name=program['name'])
        program['desc'] = text_validator(
            args.description, six_lines=True, pkg_name=program['name'])
        program['url'] = text_validator(
            args.url, one_word=True, one_line=True, pkg_name=program['name'])
    else:
        # interactive mode
        program['name'] = user_input(
            'Program name (single word): ', one_word=True)
        program['short_desc'] = user_input(
            'Short description (one line): ', one_line=True, pkg_name=program['name'])
        program['desc'] = user_input(
            'Description (up to six lines): ', six_lines=True, pkg_name=program['name'])
        program['url'] = user_input(
            'Program homepage URL: ', one_word=True, one_line=True, pkg_name=program['name'])
    # common part
    program['header'] = header()
    program['ruler'] = handy_ruler(program['name'])
    program['empty'] = ''

    # warping text
    for key in ('short_desc', 'desc', 'url', 'empty'):
        program[key] = text_warpper(program[key], program['name'], ': ')

    return program


def write_file(file_path, dictionary):
    file_path = os.path.join(file_path, 'slack-desc')

    dict_list = list()
    dict_list.extend(dictionary['header'])
    dict_list.extend(dictionary['ruler'])
    dict_list.extend(dictionary['short_desc'])
    dict_list.extend(dictionary['empty'])
    dict_list.extend(dictionary['desc'])
    # add some empty lines to get total of 11
    if len(dictionary['desc']) < 6:
        for _ in range(6 - len(dictionary['desc'])):
            dict_list.extend(dictionary['empty'])
    dict_list.extend(dictionary['empty'])
    dict_list.extend(dictionary['url'])
    dict_list.extend(dictionary['empty'])

    with open(file_path, mode='w') as slack_desc:
        for line in dict_list:
            slack_desc.write(line + '\n')


def main():
    args = arguments()

    if (len(sys.argv) == 1) or args.interactive:
        cli_mode = False

    program = program_dict(cli_mode, args)

    print(program['ruler'])

    if args.output:
        file_path = os.path.expandvars(args.output)
        file_path = os.path.expanduser(file_path)
        file_path = os.path.abspath(file_path)
    else:
        file_path = ''

    write_file(file_path, program)


if __name__ == '__main__':
    main()
