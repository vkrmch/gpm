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


# 0.0.8a0 introduces new changes
def run(cmd, stream=False, logger=None):
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),
        encoding='utf8'
    )

    stdout = ""

    while True:
        output = proc.stdout.readline().strip()
        if output == '' and proc.poll() is not None:
            break
        if output:
            stdout = '\n'.join([output, stdout])
            if logger is not None:
                logger.info(output)
            if stream:
                print(output)

    return {'returncode': proc.returncode, 'stdout': stdout, 'stderr': stdout}

# 0.0.9
# returns the os.stat() as a dict
def get_file_stats(file):
    stats_object = os.stat(file)
    return {k: getattr(stats_object, k) for k in dir(stats_object) if k.startswith('st_')}
