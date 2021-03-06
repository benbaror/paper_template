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

FIG_PATTERN = (re.compile(r'.*?\\includegraphics(\[[^\]]*\])?{([^}]*)}.*?'),
               re.compile(r'.*?\\plotone(\[[^\]]*\])?{([^}]*)}.*?'))


ABC = string.ascii_lowercase


def reformat(lines, target_dir, figure_list):
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
                yield reformat_fig_env(fig_env, fig_number, target_dir,
                                       figure_list=figure_list)
                in_fig_env = False
                yield l
            else:
                fig_env.append(l)
        else:
            yield l


def reformat_fig_env(fig_env, fig_number, target_dir, figure_list):
    """Change the names of the figure file in used in `fig_env`,
       when the is more the one figures name add a letter {a,b,c,...}
       to the end of each sub_figure file_name
    """

    fig_env = "".join(fig_env)
    matches = [fig for fig_pattern in FIG_PATTERN for
               fig in fig_pattern.findall(fig_env)]
    sub_fig_number = 0
    for _, fig_file in matches:
        _, ext = os.path.splitext(fig_file)

        new_name = 'Figure{}{}'.format(fig_number, ABC[sub_fig_number]) \
               if len(matches) > 1 \
               else 'Figure{}'.format(fig_number)
        add_ext = ('.eps' if ext == '' else '')
        new_name += ext + add_ext
        print("Processed {} as {}".format(fig_file, new_name))
        figure_list += ["{} -> {}\n".format(fig_file, new_name)]
        sub_fig_number += 1
        shutil.copyfile(fig_file + add_ext,
                        os.path.join(target_dir, new_name))
        fig_env = fig_env.replace(fig_file, new_name)
    return fig_env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help='Input file name')
    parser.add_argument("target_dir", help='Output file name')
    args = parser.parse_args()
    figure_list = ["Figures:\n"]
    try:
        os.makedirs(args.target_dir)
    except OSError:
        pass
    with open(args.input_file) as input_file:
        lines = reformat(input_file.readlines(), args.target_dir,
                         figure_list=figure_list)

    with open(args.target_dir + '/' + args.input_file, 'w') as input_file:
        input_file.writelines(lines)

    # Write the figure list
    with open(args.target_dir + '/figures.txt', 'w') as fig_file:
        fig_file.writelines(figure_list)


if __name__ == '__main__':
    main()
