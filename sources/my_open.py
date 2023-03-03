import os
import pathlib
import json


def openw(path, **kwargs):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w', encoding='utf-8', **kwargs)


def tmp_path(path):
    pathobj = pathlib.Path(path)
    # e.g. from /dfoo/dbar/stem.ext return /dfoo/dbar/stem.tmp.ext
    # where suffix = .ext
    return pathobj.parent / (str(pathobj.stem) + '.tmp' + pathobj.suffix)


def with_tmp_openw(path, callback, **kwargs):
    tpath = tmp_path(path)
    with openw(tpath, **kwargs) as outfp:
        retval = callback(outfp)
    os.replace(tpath, path)
    return retval


def std_json_dump_to_file_pointer(dumpable, pointer):
    json.dump(dumpable, pointer, indent=0, ensure_ascii=False)
    pointer.write('\n')


def std_json_dump_to_file_path(dumpable, path):
    def _write_callback(fp):
        std_json_dump_to_file_pointer(dumpable, fp)
    with_tmp_openw(path, _write_callback)


# For most generated files, particularly .fea files generated from .sym.fea
# files, we want to make the file read-only after writing it, to remind the
# user not to edit it, since those edits will get blown away the next time
# we regenerate!
#
# Another measure that could be taken, in addition or instead of this, would
# be to make one or more backups of the file before it is overwritten.
#
# Here are some ideas:
#
# import os
# import stat
#
# mode = os.stat(filename).st_mode
# ro_mask = 0o777 ^ (stat.S_IWRITE | stat.S_IWGRP | stat.S_IWOTH)
# os.chmod(filename, mode & ro_mask)
#
# st_file_attributes member returned by os.stat()
# stat.FILE_ATTRIBUTE_READONLY
