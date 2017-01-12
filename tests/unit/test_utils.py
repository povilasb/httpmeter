from hamcrest import assert_that, is_

from httpmeter import utils


def describe_count():
    def describe_when_iterable_yields_some_results():
        def it_returns_iterable_element_count():
            elements = utils.count(iter([1, 2, 3]))

            assert_that(elements, is_(3))

    def describe_when_iterable_yields_no_results():
        def it_returns_0():
            elements = utils.count(iter([]))

            assert_that(elements, is_(0))


def describe_avg():
    def describe_when_iterable_has_no_elements():
        def it_returns_0():
            result = utils.avg(iter([]))

            assert_that(result, is_(0))

    def it_returns_average_of_iterable_elements():
        result = utils.avg(iter([1, 2, 3]))

        assert_that(result, is_(2))
