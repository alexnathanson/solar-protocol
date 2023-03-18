import logging
import os
import skia
from .errors import DrawbotError
from .font import makeTTFontFromSkiaTypeface, tagToInt
from .segmenting import textSegments, reorderedSegments
from .shaping import getShapeFuncForSkiaTypeface


class cached_property(object):

    # This exists in the stdlib in Python 3.8, but not earlier

    """A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property."""

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class GraphicsStateMixin:

    # Paint style

    def fill(self, *args):
        color = _colorArgs(args)
        if color is None:
            self.fillPaint = self.fillPaint.copy(somethingToDraw=False, shader=None)
        else:
            self.fillPaint = self.fillPaint.copy(color=color, somethingToDraw=True, shader=None)

    def stroke(self, *args):
        color = _colorArgs(args)
        if color is None:
            self.strokePaint = self.strokePaint.copy(somethingToDraw=False, shader=None)
        else:
            self.strokePaint = self.strokePaint.copy(color=color, somethingToDraw=True, shader=None)

    def blendMode(self, blendMode):
        if blendMode not in _blendModes:
            raise DrawbotError(f"blendMode must be one of: {_blendModesList}")
        self.fillPaint = self.fillPaint.copy(blendMode=blendMode)
        self.strokePaint = self.strokePaint.copy(blendMode=blendMode)

    def strokeWidth(self, strokeWidth):
        self.strokePaint = self.strokePaint.copy(strokeWidth=strokeWidth)

    def lineCap(self, lineCap):
        if lineCap not in _strokeCapMapping:
            raise DrawbotError(f"lineCap must be one of: {sorted(_strokeCapMapping)}")
        self.strokePaint = self.strokePaint.copy(lineCap=lineCap)

    def lineJoin(self, lineJoin):
        if lineJoin not in _strokeJoinMapping:
            raise DrawbotError(f"lineJoin must be one of: {sorted(_strokeJoinMapping)}")
        self.strokePaint = self.strokePaint.copy(lineJoin=lineJoin)

    def lineDash(self, firstValue=None, *values):
        if firstValue is None:
            if values:
                raise TypeError("lineDash() argument(s) should be None, or one or more numbers")
        if firstValue is None:
            assert not values
            self.strokePaint = self.strokePaint.copy(lineDash=None)
        else:
            self.strokePaint = self.strokePaint.copy(lineDash=(firstValue,) + values)

    def miterLimit(self, miterLimit):
        self.strokePaint = self.strokePaint.copy(miterLimit=miterLimit)

    def linearGradient(self, startPoint, endPoint, colors, locations=None):
        # MakeLinear(
        #   points: List[skia.Point],
        #   colors: List[int],
        #   positions: object = None,
        #   mode: skia.TileMode = TileMode.kClamp,
        #   flags: int = 0,
        #   localMatrix: skia.Matrix = None) -> skia.Shader
        colors = [_colorTupleToInt(_colorArgs(c)) for c in colors]
        shader = skia.GradientShader.MakeLinear(
            points=[startPoint, endPoint],
            colors=colors,
            positions=locations,
        )
        self.fillPaint = self.fillPaint.copy(shader=shader, fill=None, somethingToDraw=True)

    def radialGradient(self, startPoint, endPoint=None, colors=None, locations=None, startRadius=0, endRadius=100):
        # MakeRadial(
        #   center: skia.Point,
        #   radius: float,
        #   colors: List[int],
        #   positions: object = None,
        #   mode: skia.TileMode = TileMode.kClamp,
        #   flags: int = 0,
        #   localMatrix: skia.Matrix = None) → skia.Shader
        if startRadius != 0:
            logging.warning("radialGradient: startRadius != 0 ignored (it's not supported in drawbot-skia)")
        if endPoint is not None and endPoint != startPoint:
            logging.warning("radialGradient: endPoint argument ignored (it's not supported in drawbot-skia)")
        colors = [_colorTupleToInt(_colorArgs(c)) for c in colors]
        shader = skia.GradientShader.MakeRadial(
            center=startPoint,
            radius=endRadius,
            colors=colors,
            positions=locations,
        )
        self.fillPaint = self.fillPaint.copy(shader=shader, fill=None, somethingToDraw=True)

    def shadow(self, offset, blur=None, color=None):
        if offset is None:
            shadow = None
        else:
            shadow = (offset, blur, color)
        self.fillPaint = self.fillPaint.copy(shadow=shadow)
        self.strokePaint = self.strokePaint.copy(shadow=shadow)

    # Text style

    def font(self, fontNameOrPath, fontSize=None):
        if fontSize is not None:
            self.textStyle = self.textStyle.copy(font=fontNameOrPath, fontSize=fontSize)
        else:
            self.textStyle = self.textStyle.copy(font=fontNameOrPath)

    def fontSize(self, size):
        self.textStyle = self.textStyle.copy(fontSize=size)

    def openTypeFeatures(self, *, resetFeatures=False, **features):
        if resetFeatures:
            currentFeatures = {}
        else:
            currentFeatures = dict(self.textStyle.features)
        currentFeatures.update(features)
        self.textStyle = self.textStyle.copy(features=currentFeatures)
        return currentFeatures

    def fontVariations(self, *, resetVariations=False, **variations):
        if resetVariations:
            currentVariations = {}
        else:
            currentVariations = dict(self.textStyle.variations)
        currentVariations.update(variations)
        self.textStyle = self.textStyle.copy(variations=currentVariations)
        return currentVariations

    def language(self, language):
        self.textStyle = self.textStyle.copy(language=language)

    def listFontVariations(self):
        ttFont = self.textStyle.ttFont
        variations = {}
        if "fvar" in ttFont:
            nameTable = ttFont["name"]
            for axis in ttFont["fvar"].axes:
                axisName = _getName(nameTable, axis.axisNameID)
                variations[axis.axisTag] = dict(
                    name=axisName,
                    minValue=axis.minValue,
                    defaultValue=axis.defaultValue,
                    maxValue=axis.maxValue,
                )
        return variations

    def listNamedInstances(self):
        ttFont = self.textStyle.ttFont
        instances = {}
        if "fvar" in ttFont:
            nameTable = ttFont["name"]
            psName = _getName(nameTable, 6)
            for instance in ttFont["fvar"].instances:
                if instance.postscriptNameID != 0xFFFF:
                    name = _getName(nameTable, instance.postscriptNameID)
                else:
                    instanceStyleName = _getName(nameTable, instance.subfamilyNameID)
                    styleName = _getName(nameTable, 2)
                    # A dodgy heuristic here:
                    if instanceStyleName == styleName:
                        name = psName
                    else:
                        name = psName + "_" + instanceStyleName
                instances[name] = instance.coordinates
        return instances


def _getName(nameTable, nameID):
    nameRecord = nameTable.getName(nameID, 3, 1, 0x0409)
    if nameRecord is None:
        nameRecord = nameTable.getName(nameID, 1, 0, 0)
    if nameRecord is not None:
        return nameRecord.toUnicode()
    return None


class GraphicsState(GraphicsStateMixin):

    # The graphics state object only deals with paint and text properties,
    # other state, such as the current transformation and clip path is
    # managed by the Skia Canvas itself.

    def __init__(self, _doInitialize=True):
        if _doInitialize:
            # see self.copy()
            self.fillPaint = FillPaint()
            self.strokePaint = StrokePaint(somethingToDraw=False)
            self.textStyle = TextStyle()

    def copy(self):
        result = GraphicsState(_doInitialize=False)
        # Our main attributes are copy-on-write, so we can share them with
        # our copy
        result.fillPaint = self.fillPaint
        result.strokePaint = self.strokePaint
        result.textStyle = self.textStyle
        return result


class _ImmutableContainer:

    def __init__(self, **properties):
        self.__dict__.update(properties)
        self._names = set(properties)

    def copy(self, **properties):
        dct = {n: self.__dict__[n] for n in self._names}
        dct.update(properties)
        return self.__class__(**dct)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self._names != other._names:
            return False
        return all(getattr(self, n) == getattr(other, n) for n in self._names)

    def __repr__(self):
        args = ", ".join(f"{n}={self.__dict__[n]!r}" for n in sorted(self._names))
        return f"{self.__class__.__name__}({args})"


class FillPaint(_ImmutableContainer):

    somethingToDraw = True
    color = (255, 0, 0, 0)  # ARGB
    blendMode = "normal"
    shader = None
    shadow = None
    _skPaintStyle = skia.Paint.kFill_Style

    @cached_property
    def skPaint(self):
        return self._makePaint()

    def _makePaint(self):
        paint = skia.Paint(
            Color=0,
            AntiAlias=True,
            Style=self._skPaintStyle,
        )
        paint.setARGB(*self.color)
        paint.setBlendMode(_blendModeMapping[self.blendMode])
        if self.shader is not None:
            paint.setShader(self.shader)
        return paint

    @cached_property
    def skPaintShadowAndOffset(self):
        if self.shadow is None:
            return None, None
        offset, blur, color = self.shadow
        color = _colorTupleToInt(_colorArgs(color))
        if not blur:
            blur = 1
        # MaskFilter.MakeBlur(
        #   style: skia.BlurStyle,
        #   sigma: float,
        #   respectCTM: bool = True) → skia.MaskFilter
        blurMask = skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 0.5 * blur, False)

        paint = skia.Paint(
            Color=color,
            MaskFilter=blurMask,
            Style=self._skPaintStyle,
        )
        return paint, offset


class StrokePaint(FillPaint):

    miterLimit = 5
    strokeWidth = 1
    lineCap = "butt"
    lineJoin = "miter"
    lineDash = None
    _skPaintStyle = skia.Paint.kStroke_Style

    @cached_property
    def skPaint(self):
        paint = self._makePaint()
        paint.setStrokeMiter(self.miterLimit)
        paint.setStrokeWidth(self.strokeWidth)
        paint.setStrokeCap(_strokeCapMapping[self.lineCap])
        paint.setStrokeJoin(_strokeJoinMapping[self.lineJoin])
        if self.lineDash is not None:
            intervals = self.lineDash
            if len(intervals) % 2:
                # Skia requires the intervals list to be of even length;
                # doubling the list matches macOS/CoreGraphics behavior
                intervals = intervals * 2
            paint.setPathEffect(skia.DashPathEffect.Make(intervals, 0))
        return paint


_strokeCapMapping = dict(
    butt=skia.Paint.Cap.kButt_Cap,
    round=skia.Paint.Cap.kRound_Cap,
    square=skia.Paint.Cap.kSquare_Cap,
)

_strokeJoinMapping = dict(
    miter=skia.Paint.Join.kMiter_Join,
    round=skia.Paint.Join.kRound_Join,
    bevel=skia.Paint.Join.kBevel_Join,
)

# NOTE: 'plusDarker' is missing
_blendModeMapping = {
    "softLight": skia.BlendMode.kSoftLight,  # lighten or darken, depending on source
    "destinationOut": skia.BlendMode.kDstOut,  # destination trimmed outside source
    "clear": skia.BlendMode.kClear,  # replaces destination with zero: fully transparent
    "sourceIn": skia.BlendMode.kSrcIn,  # source trimmed inside destination
    "destinationOver": skia.BlendMode.kDstOver,  # destination over source
    "hardLight": skia.BlendMode.kHardLight,  # multiply or screen, depending on source
    # "???": skia.BlendMode.kDst,  # preserves destination
    "xOR": skia.BlendMode.kXor,  # each of source and destination trimmed outside the other
    "hue": skia.BlendMode.kHue,  # hue of source with saturation and luminosity of destination
    "screen": skia.BlendMode.kScreen,  # multiply inverse of pixels, inverting result; brightens destination
    # "???": skia.BlendMode.kLastMode,  # last valid value
    "difference": skia.BlendMode.kDifference,  # subtract darker from lighter with higher contrast
    "overlay": skia.BlendMode.kOverlay,  # multiply or screen, depending on destination
    # "???": skia.BlendMode.kModulate,  # product of premultiplied colors; darkens destination
    "colorBurn": skia.BlendMode.kColorBurn,  # darken destination to reflect source
    # "???": skia.BlendMode.kSrc,  # replaces destination
    "plusLighter": skia.BlendMode.kPlus,  # sum of colors
    "destinationIn": skia.BlendMode.kDstIn,  # destination trimmed by source
    "destinationAtop": skia.BlendMode.kDstATop,  # destination inside source blended with source
    "saturation": skia.BlendMode.kSaturation,  # saturation of source with hue and luminosity of destination
    # "???": skia.BlendMode.kLastSeparableMode,  # last blend mode operating separately on components
    "sourceAtop": skia.BlendMode.kSrcATop,  # source inside destination blended with destination
    "sourceOut": skia.BlendMode.kSrcOut,  # source trimmed outside destination
    # "???": skia.BlendMode.kLastCoeffMode,  # last porter duff blend mode
    "normal": skia.BlendMode.kSrcOver,  # source over destination
    "copy": skia.BlendMode.kSrcOver,  # source over destination
    "colorDodge": skia.BlendMode.kColorDodge,  # brighten destination to reflect source
    "darken": skia.BlendMode.kDarken,  # darker of source and destination
    "luminosity": skia.BlendMode.kLuminosity,  # luminosity of source with hue and saturation of destination
    "multiply": skia.BlendMode.kMultiply,  # multiply source with destination, darkening image
    "lighten": skia.BlendMode.kLighten,  # lighter of source and destination
    "color": skia.BlendMode.kColor,  # hue and saturation of source with luminosity of destination
    "exclusion": skia.BlendMode.kExclusion,  # subtract darker from lighter with lower contrast
}


class TextStyle(_ImmutableContainer):

    fontSize = 10
    features = {}  # won't get mutated
    variations = {}  # won't get mutated
    language = None
    font = None

    def __init__(self, **properties):
        super().__init__(**properties)

    @cached_property
    def skFont(self):
        typeface, ttFont = self._getTypefaceAndTTFont(self.font)
        if self.variations and "fvar" in ttFont:
            typeface = self._cloneTypeface(typeface, ttFont, self.variations)
        font = self._makeFontFromTypeface(typeface, self.fontSize)
        return font

    @property
    def ttFont(self):
        _, ttFont = self._getTypefaceAndTTFont(self.font)
        return ttFont

    @staticmethod
    def _getTypefaceAndTTFont(fontNameOrPath):
        cacheKey = fontNameOrPath
        if cacheKey not in _fontCache:
            if fontNameOrPath is None:
                typeface = skia.Typeface(None)
            else:
                fontNameOrPath = os.fspath(fontNameOrPath)
                if not os.path.exists(fontNameOrPath):
                    typeface = skia.Typeface(fontNameOrPath)
                else:
                    typeface = skia.Typeface.MakeFromFile(fontNameOrPath)
                    if typeface is None:
                        raise DrawbotError(f"can't load font: {fontNameOrPath}")
            ttFont = makeTTFontFromSkiaTypeface(typeface)
            _fontCache[cacheKey] = typeface, ttFont
        return _fontCache[cacheKey]

    @staticmethod
    def _makeFontFromTypeface(typeface, size):
        font = skia.Font(typeface, size)
        font.setForceAutoHinting(False)
        font.setHinting(skia.FontHinting.kNone)
        font.setSubpixel(True)
        font.setEdging(skia.Font.Edging.kAntiAlias)
        return font

    @staticmethod
    def _cloneTypeface(typeface, ttFont, variations):
        fvar = ttFont.get("fvar")
        defaultLocation = {a.axisTag: variations.get(a.axisTag, a.defaultValue) for a in fvar.axes}
        tags = [a.axisTag for a in fvar.axes]
        location = [(tag, variations.get(tag, defaultLocation[tag])) for tag in tags]
        makeCoord = skia.FontArguments.VariationPosition.Coordinate
        rawCoords = [makeCoord(tagToInt(tag), value) for tag, value in location]
        coords = skia.FontArguments.VariationPosition.Coordinates(rawCoords)
        pos = skia.FontArguments.VariationPosition(coords)
        fontArgs = skia.FontArguments()
        fontArgs.setVariationDesignPosition(pos)
        return typeface.makeClone(fontArgs)

    @cached_property
    def _shapeFunc(self):
        return getShapeFuncForSkiaTypeface(self.skFont.getTypeface())

    def shape(self, txt):
        segments, baseLevel = textSegments(txt)
        segments = reorderedSegments(segments, baseLevel % 2, lambda item: item[2] % 2)
        startPos = (0, 0)
        glyphsInfo = None
        for runChars, script, bidiLevel, index in segments:
            runInfo = self._shapeFunc(
                runChars,
                fontSize=self.skFont.getSize(),
                startPos=startPos,
                startCluster=index,
                flippedCanvas=True,
                features=self.features,
                variations=self.variations,
                language=self.language,
            )
            if glyphsInfo is None:
                glyphsInfo = runInfo
            else:
                glyphsInfo.gids += runInfo.gids
                glyphsInfo.clusters += runInfo.clusters
                glyphsInfo.positions += runInfo.positions
                glyphsInfo.endPos = runInfo.endPos
            startPos = runInfo.endPos
        glyphsInfo.baseLevel = baseLevel
        return glyphsInfo

    def alignGlyphPositions(self, glyphsInfo, align):
        textWidth = glyphsInfo.endPos[0]
        if align is None:
            align = "left" if not glyphsInfo.baseLevel else "right"
        xOffset = 0
        if align == "right":
            xOffset = -textWidth
        elif align == "center":
            xOffset = -textWidth / 2
        glyphsInfo.positions = [(x + xOffset, y) for x, y in glyphsInfo.positions]

    def makeTextBlob(self, glyphsInfo, align):
        self.alignGlyphPositions(glyphsInfo, align)
        builder = skia.TextBlobBuilder()
        builder.allocRunPos(self.skFont, glyphsInfo.gids, glyphsInfo.positions)
        return builder.make()


# Font cache dict
# - keys: font name or path string
# - values: (skTypeface, ttFont) tuples
_fontCache = {}


def clearFontCache():
    _fontCache.clear()


def _colorTupleToInt(color):
    intColor = 0
    for channel, shift in zip(color, (24, 16, 8, 0)):
        intColor |= channel << shift
    return intColor


def _colorArgs(args):
    """Convert drawbot-style fill/stroke arguments to a tuple containing
    ARGB int values."""
    if not args:
        return None
    alpha = 1
    if len(args) == 1:
        if args[0] is None:
            return None
        r = g = b = args[0]
    elif len(args) == 2:
        r = g = b = args[0]
        alpha = args[1]
    elif len(args) == 3:
        r, g, b = args
    elif len(args) == 4:
        r, g, b, alpha = args
    else:
        assert 0
    return tuple(min(255, max(0, round(v * 255))) for v in (alpha, r, g, b))


_blendModesList = [
    'normal',
    'multiply',
    'screen',
    'overlay',
    'darken',
    'lighten',
    'colorDodge',
    'colorBurn',
    'softLight',
    'hardLight',
    'difference',
    'exclusion',
    'hue',
    'saturation',
    'color',
    'luminosity',
    'clear',
    'copy',
    'sourceIn',
    'sourceOut',
    'sourceAtop',
    'destinationOver',
    'destinationIn',
    'destinationOut',
    'destinationAtop',
    'xOR',
    'plusDarker',
    'plusLighter',
]

_blendModes = set(_blendModesList)
