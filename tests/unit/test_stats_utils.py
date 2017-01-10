from hamcrest import assert_that, is_

from httpmeter import stats


def describe_inc():
    def describe_when_specified_key_is_not_in_dict():
        def it_sets_1_for_the_key():
            d = {}

            stats.inc(d, 404)

            assert_that(d[404], is_(1))

    def describe_when_specified_key_is_in_dict():
        def it_increases_key_value_by_one():
            d = {404: 2}

            stats.inc(d, 404)

            assert_that(d[404], is_(3))
