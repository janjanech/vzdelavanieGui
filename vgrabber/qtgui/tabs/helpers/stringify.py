from typing import Optional

from vgrabber.model import Grade


def points_or_none(points: Optional[float]):
    if points is None:
        return "?"
    else:
        return str(points)


def grade_or_none(grade: Optional[Grade]):
    if grade is None:
        return "?"
    else:
        return grade.name
