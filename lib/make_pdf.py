from __future__ import print_function
import subprocess
import os


def make_pdf(input_md, template="default"):
    """Given a valid string of markdown, returns bytes of a pdf rendered from given markdown."""
    orig_dir = os.getcwd()
    work_dir = subprocess.Popen(["mktemp", "-d"], stdout=subprocess.PIPE).communicate()[0].strip()

    os.chdir(work_dir)

    with open('input.md', 'w') as md_file:
        md_file.write(input_md)

    done = subprocess.call(['pandoc', '-o', 'temp.pdf', work_dir+'/input.md', '--template', template])
    toReturn = ""
    with open('temp.pdf', 'r') as pdf:
        toReturn = pdf.read()

    # Cleanup temporary files
    os.chdir(orig_dir)
    subprocess.call(['rm','-r', work_dir])

    return toReturn


def test_make_pdf():
    '''Tests the make_pdf() function'''
    testStr = """
Title
=====

A paragraph.

Subtitle
--------

- Unordered list
- continued
- more

### Sub-sub heading

1. ordered list
2. contnued
3. more

"""

    with open('test.pdf', 'w') as test:
        test.write(make_pdf(testStr))


if __name__ == "__main__":
    test_make_pdf()




