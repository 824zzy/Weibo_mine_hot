# coding=utf-8
import re
from datetime import datetime,timedelta
def normalize_datetime(datetime_str):
    """
    Normalize datetime string to 'YYYY-MM-DD HH:MM:SS'
    :type datetime_str: unicode
    :rtype str
    """

    def match_and_convert(raw, pattern_converter_pairs):
        """
        :type raw: unicode
        :type pattern_converter_pairs: list
        :param raw: original datetime string
        :param pattern_converter_pairs: list of 2-tuples of patterns and corresponding converters.
        """
        for pattern, converter in pattern_converter_pairs:
            match_obj = re.match(pattern, raw)
            if match_obj:
                return converter(match_obj)

    now = datetime.now()

    _pattern_converter_pairs = [
        (u'(\d+)秒前',
            lambda m: now - timedelta(seconds=int(m.group(1)))),
        (u'(\d+)分钟前',
            lambda m: now - timedelta(seconds=60 * int(m.group(1)))),
        (u'今天 (\d\d):(\d\d)',
            lambda m: datetime(now.year, now.month, now.day, int(m.group(1)), int(m.group(2)))),
        (u' 今天(\d\d):(\d\d)',
            lambda m: datetime(now.year, now.month, now.day, int(m.group(1)), int(m.group(2)))),
        (u'(\d+)月(\d+)日 (\d\d):(\d\d)',
            lambda m: datetime(now.year, int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))),
        (u'(\d+)月(\d+)日',
            lambda m: datetime(now.year, int(m.group(1)), int(m.group(2)))),
        (u' (\d+)月(\d+)日 (\d\d):(\d\d)',
            lambda m: datetime(now.year, int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))),
        (u'(\d+)-(\d+)-(\d+) (\d\d):(\d\d)',
            lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)),int(m.group(5)))),
        (u'(\d+)-(\d+)-(\d+) (\d\d):(\d\d):(\d\d)',
            lambda m: datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)),
                            int(m.group(5)), int(m.group(6)))),
    ]

    return match_and_convert(datetime_str, _pattern_converter_pairs).strftime('%Y-%m-%d %H:%M:%S')
