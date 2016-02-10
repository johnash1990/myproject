from myproject.basic_utils import multiply_by_10
from numpy import inf

def test_multiply_by_10():
    assert multiply_by_10(3) == 30
    assert multiply_by_10(-1) == -10
    assert multiply_by_10(inf) == inf
    assert multiply_by_10(-inf) == -inf
