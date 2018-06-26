"""
Copy all eps figure and tex file to a target directory and change
the file reference in the tex file accordingly.
"""


import re
import argparse
import shutil
import os
import random
import string

EPS_PATTERN = (re.compile(r'.*?\\includegraphics(\[[^\]]*\])?{([^}]*)}.*?'),
               re.compile(r'.*?\\plotone(\[[^\]]*\])?{([^}]*)}.*?'))

ABC = string.ascii_lowercase


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def reformat(lines, target_dir):
    # Add non-braking spaces
    i = 0
    m = 0
    for line in lines:
        if 'begin{figure' in line:
            i = i + 1
            m = 0
        matches = set(eps for eps_pattern in EPS_PATTERN for
                      eps in eps_pattern.findall(line))

        for _, eps_file in matches:
            dest = 'Figure{}{}'.format(i, ABC[m]) if len(matches) > 1 \
                   else 'Figure{}'.format(i)
            m = m + 1
            shutil.copyfile(eps_file + '.eps',
                            os.path.join(target_dir, dest + '.eps'))
            line = line.replace(eps_file, dest)
        yield line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help='Input file name')
    parser.add_argument("target_dir", help='Output file name')
    args = parser.parse_args()
    try:
        os.makedirs(args.target_dir)
    except OSError:
        pass
    with open(args.input_file) as f:
        relines = reformat(f.readlines(), args.target_dir)
    with open(args.target_dir + '/' + args.input_file, 'w') as f:
        f.writelines(relines)
    bbl_file = args.input_file.replace('tex', 'bbl')
    shutil.copyfile(bbl_file, os.path.join(args.target_dir, bbl_file))
