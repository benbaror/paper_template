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
    in_fig_env = False
    for l in lines:
        if 'begin{figure' in l:
            i = i + 1
            in_fig_env = True
            fig_env = []
            yield l
        elif in_fig_env:
            if 'end{figure' in l:
                yield reformat_fig_env(fig_env, i, target_dir)
                in_fig_env = False
                yield l
            else:
                fig_env.append(l)
        else:
            yield l


def reformat_fig_env(lines, i, target_dir):
    fig_env = "".join(lines)
    matches = [eps for eps_pattern in EPS_PATTERN for
                  eps in eps_pattern.findall(fig_env)]


    m = 0
    for _, eps_file in matches:
        dest = 'Figure{}{}'.format(i, ABC[m]) if len(matches) > 1 \
               else 'Figure{}'.format(i)
        m = m + 1
        print(i, m)
        shutil.copyfile(eps_file + '.eps',
                        os.path.join(target_dir, dest + '.eps'))
        fig_env = fig_env.replace(eps_file, dest)
    return fig_env


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
        lines = reformat(f.readlines(), args.target_dir)
    with open(args.target_dir + '/' + args.input_file, 'w') as f:
        f.writelines(lines)
    bbl_file = args.input_file.replace('tex', 'bbl')
    shutil.copyfile(bbl_file, os.path.join(args.target_dir, bbl_file))
