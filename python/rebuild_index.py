"""Rebuild the snapshot index file.

"""
import os
import sys

from datetime import datetime

from typing import Tuple


def main():
    """

    Returns: None

    """
    if len(sys.argv) < 2:
        raise IndexError('No snapshot directory supplied')
    else:
        # Root dir is emsegment/docs/snapshots
        root_dir = sys.argv[1]

    # Get a list of dirs and their last-modified times
    dirs = [(d, os.path.getmtime(os.path.join(root_dir, d)))
            for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d))]
    # Index file path
    index_file = os.path.join(root_dir, 'README.md')
    # Generate the index file, line by line
    index_parts = []

    if len(dirs) > 0:
        # Sort dirs by last-modified time, most-recent first
        dirs = sorted(dirs, reverse=True, key=lambda d: d[1])
        # Append dir info to the index file
        for d in dirs:
            index_parts.append(gen_thumbnail_text(root_dir, d))

    # Join parts together
    index_text = '\n\n'.join(index_parts)

    # Create index file
    with open(index_file, 'w') as fl:
        fl.write(index_text)

    pass


def gen_thumbnail_text(root_dir: str,
                       d: Tuple[str, int]) -> str:
    """Generate the markdown text needed to make a thumbnail image link
    for directory `d`.

    Args:
        root_dir (str): Root directory where snapshot directories are saved.
        d (Tuple[str, int]): Directory name, last-modified-time tuple.


    Returns:
        (str): Thumbnail generation markdown text.

    """
    # Directory name
    d_name = d[0]
    # Directory last-modified time
    d_mtime = datetime.fromtimestamp(d[1]).strftime(
        '%d %B %Y, %H:%M:%S')
    # Full path to the directory thumbnail
    thumb = os.path.join(d_name, 'media', 'thumbnail.png')

    if os.path.isfile(os.path.join(root_dir, thumb)):
        # Return an image link if the thumbnail exists
        return f'<div class="thumbnail"><a href="{d_name}">' \
               f'<h2>{d_name}</h2></a><p>({d_mtime})\n</p>' \
               f'<a href="{d_name}"><img src="{thumb}" align="center">' \
               f'</a><p><i>Click for more details</i></p></div>\n\n' \
               f'---'
    else:
        # Return a text link
        return f'[{d_name}]({d_name}) ({d_mtime})'


if __name__ == '__main__':
    main()
