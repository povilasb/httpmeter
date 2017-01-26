from unittest.mock import MagicMock, patch

from hamcrest import assert_that, is_

from httpmeter import net


def describe_make_event_loops():
    @patch('asyncio.new_event_loop', MagicMock(side_effect=['l1', 'l2', 'l3']))
    def it_returns_iterable_of_event_loops():
        loops = net.make_event_loops(3)

        assert_that(list(loops), is_(['l1', 'l2', 'l3']))
