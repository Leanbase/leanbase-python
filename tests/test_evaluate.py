import unittest

from leanbase.storage import FeatureStore, SegmentStore
from leanbase.models.user import User
from leanbase.models.feature import FeatureDefinition, FeatureGlobalStatus
from leanbase.models.segment import SegmentDefinition
from leanbase.models.condition import Condition, Kinds, Operators
from leanbase.evaluate import evaluate

f_store = FeatureStore()
s_store = SegmentStore()

staff_condition = Condition(Kinds.STRING, 'email', Operators.ENDSWITH, 'leanbase.io')
staff_segment = SegmentDefinition(conditions=[staff_condition])
s_store.set_segment('staff', staff_segment)

indev_feature = FeatureDefinition('NByQa', FeatureGlobalStatus.DEV)
f_store.set_feature(indev_feature.id, indev_feature)

staff_feature = FeatureDefinition('QUYRT', FeatureGlobalStatus.STAFF, enabled_for_segments=[staff_segment])
f_store.set_feature(staff_feature.id, staff_feature)

ga_feature = FeatureDefinition('FGHJF', FeatureGlobalStatus.GA)
f_store.set_feature(ga_feature.id, ga_feature)


regular_user_attr = {'email': 'email@gmail.com', 'incarceration_count': 20}
staff_user_attr = {'email': 'email@leanbase.io'}

class EvaluateTestCase(unittest.TestCase):
    def test_evaluate_with_dev(self):
        result = evaluate(
            regular_user_attr,
            indev_feature,
        )
        self.assertEqual(False, result)

    def test_evaluate_with_staff(self):
        result = evaluate(
            regular_user_attr,
            staff_feature,
        )
        self.assertEqual(False, result)
        
        result = evaluate(
            staff_user_attr,
            staff_feature,
        )
        self.assertEqual(True, result)

    def test_evaluate_ga(self):
        result = evaluate(
            regular_user_attr,
            ga_feature
        )
        self.assertEqual(True, result)

        result = evaluate(
            staff_user_attr,
            ga_feature
        )
        self.assertEqual(True, result)
