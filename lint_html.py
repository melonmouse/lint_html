#!/usr/bin/python
"""(Ab)use Tidy to lint HTML files."""

import argparse
import re
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('--unwrapped-html', action='store_true',
    help='If set, ignore warnings about missing DOCTYPE, body, and title tags.')
parser.add_argument('--custom-block-tags', type=str, nargs='+', default=[])
parser.add_argument('--custom-inline-tags', type=str, nargs='+', default=[])
parser.add_argument('--custom-empty-tags', type=str, nargs='+', default=[])
args = parser.parse_args()

WARNING_PREFIX_PATTERN = r'line \d+ column \d+ - Warning: '


def run_and_get_result(cmd:str, allow_nonzero_return_code=False) -> str:
    """Run a command and return its output (stderr and stdout)."""
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, shell=True) as process:
        result = process.communicate()[0]
        return_code = process.wait()
    if not allow_nonzero_return_code and return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)
    return result


def run_tidy() -> str:
    """Run tidy with a config file that allows custom tags."""
    tidy_config = (
        f'new-blocklevel-tags: {", ".join(args.custom_block_tags)}\n'
        f'new-inline-tags: {", ".join(args.custom_inline_tags)}\n'
        f'new-empty-tags: {", ".join(args.custom_empty_tags)}\n'
        'show-info: no')
    tidy_config_path = run_and_get_result('mktemp').strip()
    with open(tidy_config_path, 'w', encoding='utf-8') as tidy_config_file:
        tidy_config_file.write(tidy_config)

    return run_and_get_result(
        f'tidy -o /dev/null -config {tidy_config_path} {args.file}',
        allow_nonzero_return_code=True)


def get_ignore_patterns() -> list[str]:
    """Return a list of regex patterns to ignore in tidy output."""
    custom_tags = (args.custom_block_tags +
                    args.custom_inline_tags +
                    args.custom_empty_tags)

    custom_tag_warning_patterns = [
        f'{WARNING_PREFIX_PATTERN}<{tag}> is not approved by W3C'
        for tag in custom_tags]

    unwrapped_html_warning_patterns = [
        f'{WARNING_PREFIX_PATTERN}missing <!DOCTYPE> declaration',
        f'{WARNING_PREFIX_PATTERN}inserting implicit <body>',
        f'{WARNING_PREFIX_PATTERN}inserting missing \'title\' element',
    ]

    # Remove counts output, which is incorrect if we ignore any warnings.
    tidy_counts_pattern = r'Tidy found \d+ warnings? and \d+ errors?!'
    tidy_no_error_pattern = f'No warnings or errors were found.'

    ignore_patterns = (custom_tag_warning_patterns +
        [tidy_counts_pattern, tidy_no_error_pattern])

    if args.unwrapped_html:
        ignore_patterns += unwrapped_html_warning_patterns

    # Match complete lines (including newline when possible.)
    return [r'^' + pattern + r'\n?' for pattern in ignore_patterns]


def remove_patterns(string:str, patterns:list[str]) -> str:
    """Apply ignore paterns to tidy output and return the cleaned result."""
    for pattern in patterns:
        string = re.sub(pattern, '', string, flags=re.MULTILINE)

    return string.strip()


tidy_result:str = remove_patterns(run_tidy(), get_ignore_patterns())


if tidy_result:
    print(f'\033[31;1mTidy found problems in [{args.file}].\033[0m\n')
    print(f'{tidy_result}')
    sys.exit(1)
else:
    sys.exit(0)
