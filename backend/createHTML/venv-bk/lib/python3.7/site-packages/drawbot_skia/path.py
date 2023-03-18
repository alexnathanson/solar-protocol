import logging
import math
import skia
from fontTools.misc.transform import Transform
from fontTools.pens.basePen import BasePen
from fontTools.pens.pointPen import PointToSegmentPen, SegmentToPointPen
from .gstate import TextStyle


# TODO:
# - textBox
# MAYBE:
# - contours
# - expandStroke
# - intersectionPoints
# - offCurvePoints
# - onCurvePoints
# - optimizePath
# - points
# - svgClass
# - svgID
# - svgLink
# - traceImage


class BezierPath(BasePen):

    def __init__(self, path=None, glyphSet=None):
        super().__init__(glyphSet)
        if path is None:
            path = skia.Path()
        self.path = path

    def _moveTo(self, pt):
        self.path.moveTo(*pt)

    def _lineTo(self, pt):
        self.path.lineTo(*pt)

    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = pt1
        x2, y2 = pt2
        x3, y3 = pt3
        self.path.cubicTo(x1, y1, x2, y2, x3, y3)

    def _qCurveToOne(self, pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        self.path.quadTo(x1, y1, x2, y2)

    def _closePath(self):
        self.path.close()

    def beginPath(self, identifier=None):
        self._pointToSegmentPen = PointToSegmentPen(self)
        self._pointToSegmentPen.beginPath()

    def addPoint(self, point, segmentType=None, smooth=False, name=None, identifier=None, **kwargs):
        if not hasattr(self, "_pointToSegmentPen"):
            raise AttributeError("path.beginPath() must be called before the path can be used as a point pen")
        self._pointToSegmentPen.addPoint(
            point,
            segmentType=segmentType,
            smooth=smooth,
            name=name,
            identifier=identifier,
            **kwargs
        )

    def endPath(self):
        if hasattr(self, "_pointToSegmentPen"):
            # We are drawing as a point pen
            pointToSegmentPen = self._pointToSegmentPen
            del self._pointToSegmentPen
            pointToSegmentPen.endPath()

    def arc(self, center, radius, startAngle, endAngle, clockwise):
        cx, cy = center
        diameter = radius * 2
        rect = (cx - radius, cy - radius, diameter, diameter)
        sweepAngle = (endAngle - startAngle) % 360
        if clockwise:
            sweepAngle -= 360
        self.path.arcTo(rect, startAngle, sweepAngle, False)

    def arcTo(self, point1, point2, radius):
        self.path.arcTo(point1, point2, radius)

    def rect(self, x, y, w, h):
        self.path.addRect((x, y, w, h))

    def oval(self, x, y, w, h):
        self.path.addOval((x, y, w, h))

    def line(self, pt1, pt2):
        points = [(x, y) for x, y in [pt1, pt2]]
        self.path.addPoly(points, False)

    def polygon(self, firstPoint, *points, close=True):
        points = [(x, y) for x, y in (firstPoint,) + points]
        self.path.addPoly(points, close)

    def pointInside(self, point):
        x, y = point
        return self.path.contains(x, y)

    def bounds(self):
        if self.path.countVerbs() == 0:
            return None
        return tuple(self.path.computeTightBounds())

    def controlPointBounds(self):
        if self.path.countVerbs() == 0:
            return None
        return tuple(self.path.getBounds())

    def reverse(self):
        path = skia.Path()
        path.reverseAddPath(self.path)
        self.path = path

    def appendPath(self, other):
        self.path.addPath(other.path)

    def copy(self):
        path = skia.Path(self.path)
        return BezierPath(path=path)

    def translate(self, x, y):
        self.path.offset(x, y)

    def scale(self, x, y=None, center=(0, 0)):
        if y is None:
            y = x
        self.transform((x, 0, 0, y, 0, 0), center=center)

    def rotate(self, angle, center=(0, 0)):
        t = Transform()
        t = t.rotate(math.radians(angle))
        self.transform(t, center=center)

    def skew(self, x, y=0, center=(0, 0)):
        t = Transform()
        t = t.skew(math.radians(x), math.radians(y))
        self.transform(t, center=center)

    def transform(self, transform, center=(0, 0)):
        cx, cy = center
        t = Transform()
        t = t.translate(cx, cy)
        t = t.transform(transform)
        t = t.translate(-cx, -cy)
        matrix = skia.Matrix()
        matrix.setAffine(t)
        self.path.transform(matrix)

    def drawToPen(self, pen):
        it = skia.Path.Iter(self.path, False)
        needEndPath = False
        for verb, points in it:
            penVerb, startIndex, numPoints = _pathVerbsToPenMethod.get(verb, (None, None, None))
            if penVerb is None:
                continue
            assert len(points) == numPoints, (verb, numPoints, len(points))
            if penVerb == "conicTo":
                # We should only call _convertConicToCubicDirty()
                # if it.conicWeight() == sqrt(2)/2, but skia-python doesn't
                # give the correct value.
                # https://github.com/kyamagu/skia-python/issues/116
                # if abs(it.conicWeight() - 0.707...) > 1e-10:
                #     logging.warning("unsupported conic form (weight != sqrt(2)/2): conic to cubic conversion will be bad")
                # TODO: we should fall back to skia.Path.ConvertConicToQuads(),
                # but that call is currently also not working.
                pen.curveTo(*_convertConicToCubicDirty(*points))
            elif penVerb == "closePath":
                needEndPath = False
                pen.closePath()
            else:
                if penVerb == "moveTo":
                    if needEndPath:
                        pen.endPath()
                    needEndPath = True
                pointArgs = ((x, y) for x, y in points[startIndex:])
                getattr(pen, penVerb)(*pointArgs)
        if needEndPath:
            pen.endPath()

    def drawToPointPen(self, pen):
        self.drawToPen(SegmentToPointPen(pen))

    def text(self, txt, offset=None, font=None, fontSize=10, align=None):
        if not txt:
            return
        textStyle = TextStyle(font=font, fontSize=fontSize)
        glyphsInfo = textStyle.shape(txt)
        textStyle.alignGlyphPositions(glyphsInfo, align)
        gids = sorted(set(glyphsInfo.gids))
        paths = [textStyle.skFont.getPath(gid) for gid in gids]
        for path in paths:
            path.transform(FLIP_MATRIX)
        paths = dict(zip(gids, paths))
        x, y = (0, 0) if offset is None else offset
        for gid, pos in zip(glyphsInfo.gids, glyphsInfo.positions):
            path = paths[gid]
            self.path.addPath(path, pos[0] + x, pos[1] + y)

    def _doPathOp(self, other, operator):
        from pathops import Path, op
        path1 = Path()
        path2 = Path()
        self.drawToPen(path1.getPen())
        other.drawToPen(path2.getPen())
        result = op(
            path1,
            path2,
            operator,
            fix_winding=True,
            keep_starting_points=True,
        )
        resultPath = BezierPath()
        result.draw(resultPath)
        return resultPath

    def union(self, other):
        from pathops import PathOp
        return self._doPathOp(other, PathOp.UNION)

    def intersection(self, other):
        from pathops import PathOp
        return self._doPathOp(other, PathOp.INTERSECTION)

    def difference(self, other):
        from pathops import PathOp
        return self._doPathOp(other, PathOp.DIFFERENCE)

    def xor(self, other):
        from pathops import PathOp
        return self._doPathOp(other, PathOp.XOR)

    def removeOverlap(self):
        from pathops import Path
        path = Path()
        self.drawToPen(path.getPen())
        path.simplify(
            fix_winding=True,
            keep_starting_points=False,
        )
        resultPath = BezierPath()
        path.draw(resultPath)
        self.path = resultPath.path

    __mod__ = difference

    def __imod__(self, other):
        result = self.difference(other)
        self.path = result.path
        return self

    __or__ = union

    def __ior__(self, other):
        result = self.union(other)
        self.path = result.path
        return self

    __and__ = intersection

    def __iand__(self, other):
        result = self.intersection(other)
        self.path = result.path
        return self

    __xor__ = xor

    def __ixor__(self, other):
        result = self.xor(other)
        self.path = result.path
        return self


FLIP_MATRIX = skia.Matrix()
FLIP_MATRIX.setAffine((1, 0, 0, -1, 0, 0))


def _convertConicToCubicDirty(pt1, pt2, pt3):
    #
    # NOTE: we do a crude conversion from a conic segment to a cubic bezier,
    # for two common cases, based on the following assumptions:
    # - drawbot itself does not allow conics to be drawn
    # - skia draws conics implicitly for oval(), arc() and arcTo()
    # - for oval the conic segments span 90 degrees
    # - for arc and arcTo the conic segments do not span more than 90 degrees
    # - for arc and arcTo the conic segments are circular, never elliptical
    # For all these cases, the conic weight will be (close to) zero.
    #
    # This no longer holds once a path has been transformed with skew or x/y
    # scale, in which case we need to fall back to
    # skia.Path.ConvertConicToQuads(), but that is blocked by
    # https://github.com/kyamagu/skia-python/issues/115
    # https://github.com/justvanrossum/drawbot-skia/issues/7
    #
    (x1, y1), (x2, y2), (x3, y3) = pt1, pt2, pt3
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x2 - x3
    dy2 = y2 - y3
    angle1 = math.atan2(dy1, dx1)
    angle2 = math.atan2(-dy2, -dx2)
    angleDiff = (angle1 - angle2) % (2 * math.pi)
    if angleDiff > math.pi:
        angleDiff = 2 * math.pi - angleDiff
    if abs(angleDiff - math.pi / 2) < 0.0001:
        # angle is close enough to 90 degrees, we use stupid old BEZIER_ARC_MAGIC
        handleRatio = 0.5522847498
    else:
        # Fall back to the circular assumption: |pt1 pt2| == |pt2 pt3|
        d1 = math.hypot(dx1, dy1)
        d2 = math.hypot(dx2, dy2)
        if abs(d1 - d2) > 0.00001:
            logging.warning("unsupported conic form (non-circular, non-90-degrees): conic to cubic conversion will be bad")
            # TODO: we should fall back to skia.Path.ConvertConicToQuads(),
            # but that call is currently not working.
        angleHalf = angleDiff / 2
        radius = d1 / math.tan(angleHalf)
        D = radius * (1 - math.cos(angleHalf))
        handleLength = (4 * D / 3) / math.sin(angleHalf)  # length of the bcp line
        handleRatio = handleLength / d1
    return (
        (x1 + dx1 * handleRatio, y1 + dy1 * handleRatio),
        (x3 + dx2 * handleRatio, y3 + dy2 * handleRatio),
        (x3, y3),
    )


_pathVerbsToPenMethod = {
    skia.Path.Verb.kMove_Verb: ("moveTo", 0, 1),
    skia.Path.Verb.kLine_Verb: ("lineTo", 1, 2),
    skia.Path.Verb.kCubic_Verb: ("curveTo", 1, 4),
    skia.Path.Verb.kQuad_Verb: ("qCurveTo", 1, 3),
    skia.Path.Verb.kConic_Verb: ("conicTo", 1, 3),
    skia.Path.Verb.kClose_Verb: ("closePath", 1, 1),
    # skia.Path.Verb.kDone_Verb: (None, None),  # "StopIteration", not receiving when using Python iterator
}
