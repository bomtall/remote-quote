import pytest
import knapsack

@pytest.mark.parametrize(
    'args, kwargs, expected',
    [
        # Testing optimisation
        ([], dict(capacity=8, values=[1,2,5,6], costs=[2,3,4,5]), [3,1]),


    ],
)
def test_optimal_knapsack(args, kwargs, expected):
    optimal_list = knapsack.optimal_knapsack(*args, **kwargs)
    assert optimal_list == expected