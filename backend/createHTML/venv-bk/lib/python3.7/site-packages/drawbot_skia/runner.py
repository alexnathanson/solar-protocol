import os


def makeNamespace(*objects, **kwargs):
    namespace = kwargs
    for obj in objects:
        for name in dir(obj):
            if not name.startswith("_"):
                namespace[name] = getattr(obj, name)
    return namespace


def makeDrawbotNamespace(drawbot):
    from .path import BezierPath
    import math
    import random
    additionalNames = dict(BezierPath=BezierPath)
    for name in ["random", "randint", "choice", "shuffle"]:
        additionalNames[name] = getattr(random, name)
    return makeNamespace(math, drawbot, **additionalNames)


def runScript(sourcePath, namespace=None):
    with open(sourcePath, encoding="utf-8") as f:
        source = f.read()
    runScriptSource(source, sourcePath, namespace)


def runScriptSource(source, sourcePath, namespace=None):
    if namespace is None:
        namespace = {}
    if os.path.exists(sourcePath):
        sourcePath = os.path.normpath(os.path.abspath(sourcePath))
    namespace.update({"__name__": "__main__", "__file__": sourcePath})

    if sourcePath:
        sourcePath = os.path.normpath(os.path.abspath(sourcePath))
        parentDir = os.path.dirname(sourcePath)
        saveDir = os.getcwd()
    else:
        parentDir = None
        saveDir = None

    code = compile(source, sourcePath, "exec")

    if parentDir is not None:
        os.chdir(parentDir)
    try:
        exec(code, namespace)
    finally:
        if saveDir is not None:
            os.chdir(saveDir)
