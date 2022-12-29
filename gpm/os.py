import os
import shlex
import subprocess


def ls(path, recursive=False, returnfilesonly=False):
    files = [os.path.join(path, file) for file in os.listdir(path)]
    if recursive:
        for file in files:
            if os.path.isdir(file):
                files = files + ls(file, recursive)

    if returnfilesonly:
        for index, file in enumerate(files):
            if os.path.isdir(file):
                files.pop(index)

    return files


def get_parent_folder(file):
    return os.path.dirname(os.path.abspath(file))


def get_file_extension(file):
    ext = os.path.splitext(file)[-1].lower()
    if ext == '':
        ext = None
    elif ext == '.':
        ext = None
    elif ext[0] == '.':
        ext = ext[1:]
    else:
        ext = None

    return ext


def get_filename_wo_extension(file):
    name = os.path.splitext(os.path.basename(file))[0]
    if name == '':
        name = None

    return name


def get_filename_only(file):
    return os.path.basename(file)


def run(cmd):
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy())

    # surrogateescape fixes the decoding errors otherwise
    stdout, stderr = [x.decode('utf-8', errors='surrogateescape') for x in proc.communicate()]

    return {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stderr}
