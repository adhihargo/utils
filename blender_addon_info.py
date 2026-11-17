import logging
import os
import sys
import tokenize
import zipfile
from pprint import pformat, pprint

import toml

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


def tokenize_bl_info(file_obj):
    """
    Generator that parses Python script file `file_obj` and yields
    tokens corresponding to the value of the file's bl_info.

    :param file_obj: Python script file object
    """
    capture_level = -1  # 0 = name found, 1 = capture
    for t in tokenize.tokenize(file_obj.readline):
        if t.type == tokenize.NAME and t.string == "bl_info":
            capture_level += 1
        elif t.type == tokenize.OP:
            if t.string == "=" and capture_level == 0:
                capture_level = 1
                continue
            if t.string == "{":
                capture_level += 1
            if t.string == "}":
                capture_level -= 1

        if capture_level > 1:
            yield t
        elif capture_level == 1:
            yield t
            break


def extract_bl_info(file_obj) -> dict:
    bl_info_str = tokenize.untokenize((t.type, t.string) for t in tokenize_bl_info(file_obj))
    if not bl_info_str:
        logger.error("File have no bl_info structure")
        return {}

    bl_info = eval(bl_info_str)
    filtered_bl_info = {k: v for k, v in bl_info.items() if k in "author blender description location name version"}
    return filtered_bl_info


def extract_manifest(sf):
    manifest = toml.loads(sf.read().decode("utf-8"))
    filtered_manifest = {k: v for k, v in manifest.items()
                         if k in "id name tags tagline blender_version_min version".split()}
    # return filtered_manifest
    return manifest


def print_bl_info(path_string, bl_info):
    print("FILE: {}".format(path_string))
    print("BL_INFO: {}".format(pformat(bl_info)))


def print_manifest(path_string, manifest):
    print("FILE: {}".format(path_string))
    print("MANIFEST: {}".format(pformat(manifest)))


def read_zipfile(file_path):
    with zipfile.ZipFile(file_path, 'r') as zf:
        logger.info("Reading ZIP file: {}".format(file_path))
        read_zipobj(zf)


def read_zipobj(zf):
    """
    Recursively read ZIP file, find and process Python scripts at root
    (any name) or immediate subfolders (named __init__.py), manifest
    files.

    :param zf: ZIP file object
    """
    script_list = []
    manifest_list = []
    archive_list = []
    for zi in filter((lambda zi_: not zi_.is_dir()), zf.infolist()):
        dir_path: str
        filename = zi.filename
        dir_path, file_name = os.path.split(filename)
        if (dir_path.count("/") < 1 and file_name in {"__init__.py"}) or \
                (dir_path == "" and file_name.lower().endswith(".py")):
            logger.info("Module script in ZIP file: {}".format(filename))
            script_list.append(filename)
        elif file_name in {"blender_manifest.toml"}:
            manifest_list.append(filename)
        elif file_name.lower().endswith(".zip"):
            archive_list.append(filename)

    file_path = zf.filename
    for fn in script_list:
        with zf.open(fn) as sf:
            path_string = '"{}" ({})'.format(file_path, fn)
            bl_info = extract_bl_info(sf)
            print_bl_info(path_string, bl_info)
    for fn in manifest_list:
        with zf.open(fn) as sf:
            path_string = '"{}" ({})'.format(file_path, fn)
            manifest = extract_manifest(sf)
            print_manifest(path_string, manifest)
    for fn in archive_list:
        with zf.open(fn) as zzf_obj:
            with zipfile.ZipFile(zzf_obj) as zzf:
                read_zipobj(zzf)


def main():
    for file_path in sys.argv[1:]:
        if not os.path.isfile(file_path):
            logger.error("Not a file: {}".format(file_path))
            continue

        if zipfile.is_zipfile(file_path):
            read_zipfile(file_path)
        elif os.path.splitext(file_path)[1].lower() == ".py":
            with open(file_path, "rb") as sf:
                path_string = '"{}"'.format(file_path)
                bl_info = extract_bl_info(sf)
                print_bl_info(path_string, bl_info)
        print()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
