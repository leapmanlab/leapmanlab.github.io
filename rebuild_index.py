"""Rebuild the snapshot index file.

"""
import json
import os

import numpy as np

from datetime import datetime

from typing import Any, Dict, Sequence, Tuple

HISTORY = 'eval_history.json'
STATS = 'stats.json'
METRICS = ['ari', 'miou', 'accuracy', 'n_params']


def summarize_dir(root_dir: str):
    """Recursively summarize a directory tree, beginning at `root_dir` (and
    ignoring media directories).

    Leaf dirs contain media and statistics from a neural network
    training session. Leaf dirs have this structure:
        .
        +-- media
        |   +-- [data, label, segmentation, and stat images]
        +-- eval_history.json
        +-- README.md

    To dir_ and each child dir, this function adds:
        (1) stats.json containing summary statistics and links to summary
            images.
    To each non-leaf dir, this function adds:
        (2) README.md displaying summaries of child dirs.

    Args:
        root_dir (str):

    Returns: None

    """
    #
    def media_check(d):
        files = os.listdir(d)
        return any(['summary.png' in fl for fl in files])

    child_dirs = [os.path.join(root_dir, d) for d in os.listdir(root_dir)
                  if os.path.isdir(os.path.join(root_dir, d))
                  and not media_check(os.path.join(root_dir, d))]
    for d in child_dirs:
        summarize_dir(d)

    if len(child_dirs) == 0:
        # No child dirs, assume dir_ is a base dir: contains a 'media' subdir
        # and an 'eval_history.json'
        with open(os.path.join(root_dir, HISTORY), 'r') as f:
            # Eval history for the net in dir_
            eval_history = json.load(f)
        e = eval_history[-1]
        stats = {'leaf': True,
                 'dir': root_dir,
                 'n_nets': 1,
                 'name': e['name'],
                 'ari': (e['adj_rand_idx'],),
                 'miou': [e['mean_iou']],
                 'accuracy': [e['accuracy']],
                 'n_params': [e['n_trainable_params']],
                 'n_iterations': e['global_step']}

    else:
        # For non-leaf dirs, build up a summary of child dirs and write it to
        #  a README.md file
        # Get a list of child stats
        child_stats = []
        for d in child_dirs:
            with open(os.path.join(d, STATS), 'r') as f:
                child_stats.append(json.load(f))
        children_are_leafs = child_stats[0]['leaf']

        stats = {metric: {'min': 0, 'max': 0, 'mean': 0, 'dir': ''}
                 for metric in METRICS}
        stats['leaf'] = False
        stats['n_nets'] = sum([s['n_nets'] for s in child_stats])

        if children_are_leafs:
            for metric in METRICS:
                vals = np.array([s[metric] for s in child_stats])
                stats[metric]['min'] = vals.min().item()
                stats[metric]['max'] = vals.max().item()
                stats[metric]['mean'] = vals.mean().item()
                argmax_idx = vals.argmax()
                stats[metric]['dir'] = \
                    child_stats[argmax_idx]['dir']

        else:
            for metric in METRICS:
                stats[metric]['min'] = \
                    min([s[metric]['min'] for s in child_stats])
                stats[metric]['max'] = \
                    max([s[metric]['max'] for s in child_stats])
                stats[metric]['mean'] = sum([s['n_nets'] * s[metric]['mean']
                                             for s in child_stats]) \
                    / stats['n_nets']
                argmax_idx = np.array([s[metric]['max']
                                       for s in child_stats]).argmax()
                stats[metric]['dir'] = child_stats[argmax_idx][metric]['dir']

        # Assemble an index file for `root_dir`
        index_text = build_index(root_dir, child_dirs, child_stats)
        index_file = os.path.join(root_dir, 'README.md')
        if os.path.exists(index_file):
            os.remove(index_file)
        with open(os.path.join(root_dir, 'README.md'), 'w') as f:
            f.write(index_text)

    stats_file = os.path.join(root_dir, STATS)
    if os.path.exists(stats_file):
        os.remove(stats_file)
    with open(stats_file, 'w') as f:
        json.dump(stats, f)

    pass


def build_index(root_dir: str,
                child_dirs: Sequence[str],
                child_stats: Sequence[Dict[str, Any]]) -> str:
    """

    Args:
        root_dir (str):
        child_dirs (Sequence[str]):
        child_stats (Sequence[Dict[str, Any]]):

    Returns:
        (str):

    """
    # Build the index file as a header and sequence of summary divs
    index_parts = [f'\n## {root_dir.replace("snapshots/", "")}']
    # Get a list of child dirs and their creation and last-modified times
    dirs_info = [(d, os.path.getctime(d), os.path.getmtime(d), i)
                 for i, d in enumerate(child_dirs)]
    # Sort dirs by creation time, most-recent first
    dirs_info = sorted(dirs_info, reverse=True, key=lambda d: d[1])
    for d_info in dirs_info:
        index_parts.append(gen_summary_text(root_dir,
                                            d_info[:-1],
                                            child_stats[d_info[-1]]))

    return '\n\n'.join(index_parts)


def gen_summary_text(root_dir: str,
                     child_dir_info: Tuple[str, float, float],
                     stats: Dict[str, Any]) -> str:
    """

    Args:
        root_dir:
        child_dir_info:
        stats:

    Returns:
        (str):

    """
    # Directory name, creation, and last-modified times
    d_name = child_dir_info[0].replace('snapshots/', '')
    d_ctime = datetime.fromtimestamp(child_dir_info[1]).strftime(
        'Created %d %b %Y, %H:%M:%S')
    d_mtime = datetime.fromtimestamp(child_dir_info[2]).strftime(
        'Modified %d %b %Y, %H:%M:%S')

    child_link = os.path.basename(d_name)
    disp_n = d_name.replace('/', ' / ')

    if stats['leaf']:
        # Leaf directories have simpler stats

        summary_image = os.path.join(child_link,
                                     'media',
                                     'summary.png')

        # Summary image links to the child_dir's README.md
        image_text = f'<div class="thumbnail"><a href="{child_link}">' \
                     f'<h2>{disp_n}</h2></a><p>({d_ctime}. {d_mtime})\n</p>' \
                     f'<a href="{child_link}"><img src="{summary_image}"' \
                     f' align="center">' \
                     f'</a><p>\n<i>Click for more details</i>\n</p></div>'

        stat_text_parts = [f'**{m}**: {stats[m][0]:.4f}. ' for m in METRICS]
        stat_text = ''.join(stat_text_parts)
        summary_text = '\n\n'.join([image_text, stat_text, '---'])
        return summary_text

    else:
        # Image is the summary from the net with highest mean IOU
        summary_image = os.path.relpath(os.path.join(stats['miou']['dir'],
                                                     'media',
                                                     'summary.png'),
                                        root_dir)

        # Summary image links to the child_dir's README.md
        image_text = f'<div class="thumbnail"><a href="{child_link}">' \
                     f'<h2>{disp_n}</h2></a><p>({d_ctime}. {d_mtime})\n</p>' \
                     f'<a href="{child_link}"><img src="{summary_image}"' \
                     f' align="center">' \
                     f'</a><p><i>Click image for more details</i>\n</p></div>'

        # Performance stat info
        stat_text_parts = [f'**{m}**: min {stats[m]["min"]:.4f}. '
                           f'max {stats[m]["max"]:.4f}. '
                           f'mean {stats[m]["mean"]:.4f}.  '
                           f'([best net]({os.path.relpath(stats[m]["dir"], root_dir)}))'
                           for m in METRICS]
        stat_text = '\n\n'.join([f'{stats["n_nets"]} nets'] + stat_text_parts)
        summary_text = '\n\n'.join([image_text, stat_text, '---'])
        return summary_text


if __name__ == '__main__':
    summarize_dir('snapshots')
