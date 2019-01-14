from .actionexecutors import LoginActionExecutor, ExportSemestralPointsActionExecutor
from vgrabber.base.exportaction import ExportAction
from .syncer import Syncer


class Exporter(Syncer):
    actions = (
        (ExportAction.all, LoginActionExecutor),
        ({ExportAction.semestral_points_list}, ExportSemestralPointsActionExecutor),
    )
