import enum

from .condition import Condition

class ConditionCombinator(enum.Enum):
    """ How are conditions joined together? """
    
    OR = 'or'
    AND = 'and'


class SegmentDefinition(object):
    """ Describes the matching criteria for a segment. """

    def __init__(self, conditions=[], combinator=ConditionCombinator.OR):
        self.conditions = conditions
        self.combinator = combinator
