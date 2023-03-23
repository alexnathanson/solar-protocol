from abc import ABC, abstractmethod
import logging
import os
import pathlib
import tempfile
import skia


class Document(ABC):

    # pageWidth
    # pageHeight

    @property
    @abstractmethod
    def isDrawing(self):
        return ...

    @abstractmethod
    def beginPage(self, width: int, height: int) -> skia.Canvas:
        return ...

    @abstractmethod
    def endPage(self):
        ...

    @abstractmethod
    def setFrameDuration(self, duration):
        ...

    @abstractmethod
    def saveImage(self, path, **kwargs):
        ...


DEFAULT_FRAMEDURATION = 1/10


class RecordingDocument(Document):

    def __init__(self):
        self._pictures = []
        self._frameDurations = []
        self._currentRecorder = None
        self._currentFrameDuration = DEFAULT_FRAMEDURATION
        self.pageWidth = self.pageHeight = None

    @property
    def isDrawing(self):
        return self._currentRecorder is not None

    def beginPage(self, width, height):
        assert self._currentRecorder is None
        self.pageWidth = width
        self.pageHeight = height
        self._currentRecorder = skia.PictureRecorder()
        return self._currentRecorder.beginRecording(width, height)

    def endPage(self):
        self._pictures.append(self._currentRecorder.finishRecordingAsPicture())
        self._frameDurations.append(self._currentFrameDuration)
        self._currentRecorder = None
        self._currentFrameDuration = DEFAULT_FRAMEDURATION
        self.pageWidth = self.pageHeight = None

    def setFrameDuration(self, duration):
        self._currentFrameDuration = duration

    def saveImage(self, path, **kwargs):
        path = pathlib.Path(path).resolve()
        suffix = path.suffix.lower().lstrip(".")
        methodName = f"_saveImage_{suffix}"
        method = getattr(self, methodName, None)
        if method is None:
            raise ValueError(f"unsupported file type: {suffix}")
        method(path, **kwargs)

    def _saveImage_pdf(self, path, **kwargs):
        stream = skia.FILEWStream(os.fspath(path))
        with skia.PDF.MakeDocument(stream) as document:
            for picture in self._pictures:
                x, y, width, height = picture.cullRect()
                assert x == 0 and y == 0
                with document.page(width, height) as canvas:
                    canvas.drawPicture(picture)
        stream.flush()

    def _saveImage_svg(self, path, **kwargs):
        for picture, framePath in _iteratePictures(self._pictures, path):
            x, y, width, height = picture.cullRect()
            assert x == 0 and y == 0
            stream = skia.FILEWStream(os.fspath(framePath))
            canvas = skia.SVGCanvas.Make((width, height), stream)
            canvas.drawPicture(picture)
            del canvas
            stream.flush()

    def _saveImage_png(self, path, **kwargs):
        _savePixelImages(self._pictures, path, skia.kPNG)

    def _saveImage_jpeg(self, path, **kwargs):
        _savePixelImages(self._pictures, path, skia.kJPEG, whiteBackground=True)

    _saveImage_jpg = _saveImage_jpeg

    def _saveImage_mp4(self, path, codec="libx264", **kwargs):
        from .ffmpeg import generateMP4
        if not self._pictures:
            # Empty mp4?
            return
        frameRate = max(1, round(1 / self._frameDurations[-1]))
        if len(set(self._frameDurations)) != 1:
            logging.warning("ignoring varying frame durations for mp4 export")
        with tempfile.TemporaryDirectory(prefix="drawbot-skia-") as tempDir:
            tempDir = pathlib.Path(tempDir)
            imagePath = tempDir / "frame.png"
            _savePixelImages(
                self._pictures,
                imagePath,
                skia.kPNG,
                whiteBackground=True,
                singlePage=False,
            )
            imagesTemplate = tempDir / "frame_%d.png"
            generateMP4(imagesTemplate, path, frameRate, codec=codec)


def _savePixelImages(pictures, path, format, whiteBackground=False, singlePage=None):
    for picture, framePath in _iteratePictures(pictures, path, singlePage):
        _savePixelImage(picture, framePath, format, whiteBackground=whiteBackground)


def _iteratePictures(pictures, path, singlePage=None):
    if singlePage is None:
        singlePage = len(pictures) == 1
    for index, picture in enumerate(pictures):
        if singlePage:
            framePath = path
        else:
            framePath = path.parent / f"{path.stem}_{index}{path.suffix}"
        yield picture, framePath


def _savePixelImage(picture, path, format, whiteBackground=False):
    x, y, width, height = picture.cullRect()
    assert x == 0 and y == 0
    surface = skia.Surface(int(width), int(height))
    with surface as canvas:
        if whiteBackground:
            canvas.clear(skia.ColorWHITE)
        canvas.drawPicture(picture)
    image = surface.makeImageSnapshot()
    image.save(os.fspath(path), format)


class PixelDocument(Document):
    ...


class MP4Document(PixelDocument):
    ...


class PDFDocument(Document):
    ...


class SVGDocument(Document):
    ...
