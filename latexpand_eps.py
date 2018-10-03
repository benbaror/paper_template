"""
Copy all eps figures and the tex file to a target directory and change
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


def reformat(lines, target_dir):
    """Identify the figure sections in the tex file and reformat them"""
    fig_number = 0
    in_fig_env = False
    for l in lines:
        if 'begin{figure' in l:
            fig_number += 1
            in_fig_env = True
            fig_env = []
            yield l
        elif in_fig_env:
            if 'end{figure' in l:
                yield reformat_fig_env(fig_env, fig_number, target_dir)
                in_fig_env = False
                yield l
            else:
                fig_env.append(l)
        else:
            yield l


def reformat_fig_env(fig_env, fig_number, target_dir):
    """Change the names of the figure file in used in `fig_env`,
       when the is more the one figures name add a letter {a,b,c,...}
       to the end of each sub_figure file_name
    """

    fig_env = "".join(fig_env)
    matches = [eps for eps_pattern in EPS_PATTERN for
               eps in eps_pattern.findall(fig_env)]

    sub_fig_number = 0
    for _, eps_file in matches:
        new_name = 'Figure{}{}'.format(fig_number, ABC[sub_fig_number]) \
               if len(matches) > 1 \
               else 'Figure{}'.format(fig_number)
        print("Processed {} as eps_file {}".format(eps_file, new_name))
        sub_fig_number += 1
        shutil.copyfile(eps_file + '.eps',
                        os.path.join(target_dir, new_name + '.eps'))
        fig_env = fig_env.replace(eps_file, new_name)
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
