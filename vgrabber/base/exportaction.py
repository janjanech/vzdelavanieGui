from enum import Enum, auto


class ExportAction(Enum):
    semestral_points_list = auto()


ExportAction.semestral_points_list.depends = set()

ExportAction.default = ()
ExportAction.all = frozenset(ExportAction)
