from enum import Enum
from PyQt5.QtGui import QColor

class ResultType(Enum):

    WAIT = QColor("orange")
    COMPILE = QColor("orange")
    JUDGING = QColor("orange")
    AC = QColor("green")
    PAC = QColor("yellow")
    WA = QColor("red")
    CE = QColor("blue")
    RTE = QColor("blue")
    TLE = QColor("darkorange")
    MLE = QColor("darkorange")
    OLE = QColor("darkorange")

    def __init__(self, color: QColor):
        self.color = color

    @staticmethod
    def from_result_class_str(result_class_str: str):
        match result_class_str:
            case 'result-wait':     return ResultType.WAIT
            case 'result-compile': return ResultType.COMPILE
            case 'result-judging': return ResultType.JUDGING
            case 'result-ac':   return ResultType.AC
            case 'result-pac': return ResultType.PAC
            case 'result-wa': return ResultType.WA
            case 'result-ce': return ResultType.CE
            case 'result-rte': return ResultType.RTE
            case 'result-tle': return ResultType.TLE
            case 'result-mle': return ResultType.MLE
            case 'result-ole': return ResultType.OLE
            case _:
                raise NameError(f"result_class_str {result_class_str} not listed")


class SubmissionResult:
    def __init__(self, result_class: str, message: str):
        self.message = message
        self.result_type = ResultType.from_result_class_str(result_class)