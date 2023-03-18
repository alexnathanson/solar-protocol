import os
import subprocess
import sys


# Monkeypatch this variable to override the ffmpeg executable location
FFMPEG_PATH = None


def generateMP4(
        imageTemplate,
        mp4path,
        frameRate,
        codec="libx264",
        preferPyFFmpeg=False):
    ffmpegPath = FFMPEG_PATH
    if ffmpegPath is None and not preferPyFFmpeg:
        ffmpegPath = findExecutable("ffmpeg")
    if ffmpegPath is None:
        ffmpegPath = getPyFFmpegPath()
    imageTemplate = os.fspath(imageTemplate)
    mp4path = os.fspath(mp4path)
    cmds = [
        ffmpegPath,             # path to the ffmpeg executable
        "-y",                   # overwrite existing files
        "-loglevel", "16",      # 'error, 16' Show all errors, including ones which can be recovered from.
        "-r", str(frameRate),   # frame rate
        "-i", imageTemplate,    # input sequence
        "-c:v", codec,          # codec
        "-crf", "20",           # Constant Rate Factor
        "-pix_fmt", "yuv420p10le",  # pixel format. 8bit: yuv420p 10bit: yuv420p10le, yuv422p10le, yuv444p10le
        mp4path,                # output path
    ]
    runExternalProcess(cmds)


def getPyFFmpegPath():
    try:
        import pyffmpeg
    except ImportError:
        raise ImportError("ffmpeg not found: install ffmpeg manually, or do 'pip install pyffmpeg==1.6.1'")
    ffmpegPath = os.path.normpath(pyffmpeg.FFmpeg().get_ffmpeg_bin())
    st = os.stat(ffmpegPath)
    if sys.platform != "win32" and not st.st_mode & 0o00100:
        # https://github.com/deuteronomy-works/pyffmpeg/issues/33
        os.chmod(ffmpegPath, st.st_mode | 0o00100)
    return ffmpegPath


def findExecutable(name):
    """
        >>> import sys
        >>> findExecutable("python") == sys.executable
        True
        >>> findExecutable("ls")
        '/bin/ls'
    """
    if sys.platform == "win32":
        name += ".exe"
    path = os.getenv("PATH")
    if path:
        path = path.split(os.pathsep)
        if sys.platform != "win32" and "/usr/local/bin" not in path:
            path.append("/usr/local/bin")
        for p in path:
            ep = os.path.join(p, name)
            if os.path.exists(ep):
                return ep
    return None


def runExternalProcess(cmds, cwd=None):
    r"""
        >>> stdout, stderr = runExternalProcess(["which", "ls"])
        >>> stdout
        '/bin/ls\n'
        >>> assert stdout == '/bin/ls\n'
        >>> runExternalProcess(["which", "fooooo"])
        Traceback (most recent call last):
            ...
        subprocess.CalledProcessError: Command '['which', 'fooooo']' returned non-zero exit status 1.
        >>> stdout, stderr = runExternalProcess(["python", "-S", "-c", "print('hello')"])
        >>> stdout
        'hello\n'
    """
    p = subprocess.Popen(
        cmds,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
        universal_newlines=True,
    )
    stdoutdata, stderrdata = p.communicate()
    assert p.returncode is not None
    if p.returncode != 0:
        sys.stdout.write(stdoutdata)
        sys.stderr.write(stderrdata)
        raise subprocess.CalledProcessError(p.returncode, cmds)
    return stdoutdata, stderrdata


if __name__ == "__main__":
    import doctest
    doctest.testmod()
