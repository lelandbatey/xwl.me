# -*- coding: utf-8 -*-
"""Code for generating pdf's from markdown. Requires pandoc be installed."""

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
