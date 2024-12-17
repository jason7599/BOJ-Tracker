from enum import Enum
from dataclasses import dataclass
from PyQt5.QtGui import QColor

@dataclass
class SubmissionResult:

    class Type(Enum):
        PENDING = ('', QColor('black')) # should never see this
        ACCEPTED = ('ac', QColor('green'))
        PARTIAL = ('pa', QColor('yellow'))
        WRONG = ('wa', QColor('red'))
        ERROR = ('er', QColor('purple'))
        LIMIT_EXCEEDED = ('le', QColor('orange'))

        def __init__(self, json_name: str, display_color: QColor):
            self.json_name = json_name # name to be stored in json
            self.display_color = display_color

        # can't find a workaround.
        @classmethod
        def from_json_name(cls, json_name: str):
            for type in cls:
                if type.json_name == json_name:
                    return type

    message: str
    type: Type

    _RESULT_CLASS_MAPPING = {
        'result-wait':      Type.PENDING,
        'result-judging':   Type.PENDING,
        'result-compile':   Type.PENDING,
        'result-ac':        Type.ACCEPTED,
        'result-pac':       Type.PARTIAL,
        'result-wa':        Type.WRONG,
        'result-ce':        Type.ERROR,
        'result-rte':       Type.ERROR,
        'result-tle':       Type.LIMIT_EXCEEDED,
        'result-mle':       Type.LIMIT_EXCEEDED,
        'result-ole':       Type.LIMIT_EXCEEDED
    }

    @classmethod
    def get_type(cls, result_class: str):
        return cls._RESULT_CLASS_MAPPING.get(result_class)

    def to_json(self):
        return {
            'message': self.message,
            'type': self.type.json_name
        }
    
    @classmethod
    def from_json(cls, json):
        return SubmissionResult(
            message=json['message'],
            type=cls.Type.from_json_name(json['type'])
        )
