import functools
import logging
import os
import re
import shutil
import urllib.request


LOGGER = logging.getLogger("root")
LOGGER.setLevel(logging.DEBUG)

FILENAME = "2018-05-20-benelux1-efteling.bb"
IMAGE_DIRECTORY = "assets/img"

# Regex definitions
IMAGE_RE = r"\[IMG\](.*)\[\/IMG\]"
ITALIC_RE = r"\[I\](.*)\[\/I\]"
IMAGE_W_CAPTION_RE = IMAGE_RE + "\n" + ITALIC_RE
MARKDOWN_IMG_RE = r"!\[(.*)\]\(.*/([a-zA-Z0-9]*).jpg\)"


def download_image(image_url, file_root):
    """Fetch image, placing it in the assets directory"""
    image_name = image_url.split("/")[-1]
    local_fname, _ = urllib.request.urlretrieve(image_url)
    shutil.copyfile(
        local_fname,
        os.path.join(IMAGE_DIRECTORY, file_root, image_name))
    return os.path.join("/", IMAGE_DIRECTORY, file_root, image_name)


def replace_image_and_caption(match, file_root, download=False):
    """Process image tag with following caption tag"""
    image_url = match.group(1)
    caption = match.group(2)

    if download:
        if not image_url:
            return ""

        image_url = download_image(image_url, file_root)

    return f"![]({image_url})\n*{caption}*"


def replace_image(match, file_root, download=False):
    """Process image tag on its own"""
    image_url = match.group(1)

    if not image_url:
        return ""

    if download:
        image_url = download_image(image_url, file_root)
    return f"![]({image_url})"


def replace_markdown_image(match):
    caption = match.group(1)
    img_url = match.group(2)

    return f"![](https://i.imgur.com/{img_url}.jpg)\n*{caption}*"


def process_bb_file(filename):
    """Process a .bb BBCode blog file, saving a markdown file in its place"""

    with open(f"_posts/{filename}") as f:
        blog_text = f.read()

    file_root = filename.replace(".bb", "")

    # if not os.path.exists(os.path.join(IMAGE_DIRECTORY, file_root)):
    #     os.mkdir(os.path.join(IMAGE_DIRECTORY, file_root))

    blog_text = re.sub(
        IMAGE_W_CAPTION_RE,
        functools.partial(replace_image_and_caption, file_root=file_root),
        blog_text,
        flags=re.I
        )

    blog_text = re.sub(
        IMAGE_RE,
        functools.partial(replace_image, file_root=file_root),
        blog_text,
        flags=re.I
    )

    with open(f"_posts/{filename.replace('.bb', '.md')}", "w") as f:
        f.write(blog_text)


def revert_images(filename):
    """Revert images"""
    with open(f"_posts/{filename}") as f:
        blog_text = f.read()

    blog_text = re.sub(
        MARKDOWN_IMG_RE,
        replace_markdown_image,
        blog_text,
        flags=re.I
        )

    with open(f"_posts/{filename.replace('.bb', '.md')}", "w") as f:
        f.write(blog_text)



if __name__ == "__main__":

    for file in [f for f in os.listdir("_posts") if f.endswith(".bb")]:
        LOGGER.info(f"Processing file {file}")
        process_bb_file(file)

    urllib.request.urlcleanup()
