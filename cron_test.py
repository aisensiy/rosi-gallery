import unittest
import cron


class CronTest(unittest.TestCase):

    def test_calculate_popular(self):
        source = r"""
[IMAGE_VIEW] image view 48/26.JPEG at 1353828876
[IMAGE_VIEW] image view 48/26.JPEG at 1353828876
[IMAGE_VIEW] image view 48/27.JPEG at 1353828876
[IMAGE_VIEW] image view 48/3.JPEG at 1353828876
[IMAGE_VIEW] image view e:\rosi\48\4.JPEG at 1353829195
[IMAGE_VIEW] image view e:\rosi\48\5.JPEG at 1353829195
[IMAGE_VIEW] image view e:\rosi\48\6.JPEG at 1353829196
        """
        lines = [m.strip() for m in source.split('\n') if m.strip()]
        base_dir = 'e:\\rosi'
        counter = cron.calculate_popular(base_dir, lines)
        assert type(counter) is dict
        assert counter['48/26.JPEG'] == 2
        assert counter['48/5.JPEG'] == 1

if __name__ == "__main__":
    unittest.main()
