from   datetime       import datetime
import sys
from   dateutil.tz    import tzstr
import pytest
from   javaproperties import java_timestamp

# Unix timestamps and datetime objects don't support leap seconds or month 13,
# so there's no need (and no way) to test handling of them here.

old_pacific = tzstr('PST8PDT,M4.1.0,M10.5.0')

@pytest.mark.parametrize('ts,s', [
    (None, ''),
    (False, ''),
    (0, 'Wed Dec 31 19:00:00 EST 1969'),
    (1234567890.101112, 'Fri Feb 13 18:31:30 EST 2009'),
    (1234567890.987654, 'Fri Feb 13 18:31:30 EST 2009'),

    # Months:
    (1451624400, 'Fri Jan 01 00:00:00 EST 2016'),
    (1454396522, 'Tue Feb 02 02:02:02 EST 2016'),
    (1456992183, 'Thu Mar 03 03:03:03 EST 2016'),
    (1459757044, 'Mon Apr 04 04:04:04 EDT 2016'),
    (1462439105, 'Thu May 05 05:05:05 EDT 2016'),
    (1465207566, 'Mon Jun 06 06:06:06 EDT 2016'),
    (1467889627, 'Thu Jul 07 07:07:07 EDT 2016'),
    (1470658088, 'Mon Aug 08 08:08:08 EDT 2016'),
    (1473426549, 'Fri Sep 09 09:09:09 EDT 2016'),
    (1476108610, 'Mon Oct 10 10:10:10 EDT 2016'),
    (1478880671, 'Fri Nov 11 11:11:11 EST 2016'),
    (1481562732, 'Mon Dec 12 12:12:12 EST 2016'),

    # Days of the week:
    (1451818800, 'Sun Jan 03 06:00:00 EST 2016'),
    (1451883600, 'Mon Jan 04 00:00:00 EST 2016'),
    (1451973600, 'Tue Jan 05 01:00:00 EST 2016'),
    (1452063600, 'Wed Jan 06 02:00:00 EST 2016'),
    (1452153600, 'Thu Jan 07 03:00:00 EST 2016'),
    (1452243600, 'Fri Jan 08 04:00:00 EST 2016'),
    (1452333600, 'Sat Jan 09 05:00:00 EST 2016'),

    # Leap day:
    (1456733655, 'Mon Feb 29 03:14:15 EST 2016'),

    # PM/24-hour time:
    (1463159593, 'Fri May 13 13:13:13 EDT 2016'),

    # Before spring ahead:
    (1457852399, 'Sun Mar 13 01:59:59 EST 2016'),
    (datetime(2016, 3, 13, 1, 59, 59), 'Sun Mar 13 01:59:59 EST 2016'),
    (
        datetime(2006, 4, 2, 1, 59, 59, 0, old_pacific),
        'Sun Apr 02 01:59:59 PST 2006',
    ),

    # Skipped by spring ahead:
    (datetime(2016, 3, 13, 2, 30, 0), 'Sun Mar 13 03:30:00 EDT 2016'),
    (
        datetime(2006, 4, 2, 2, 30, 0, 0, old_pacific),
        'Sun Apr 02 02:30:00 PDT 2006',
    ),

    # After spring ahead:
    (1457852401, 'Sun Mar 13 03:00:01 EDT 2016'),
    (datetime(2016, 3, 13, 3, 0, 1), 'Sun Mar 13 03:00:01 EDT 2016'),
    (
        datetime(2006, 4, 2, 3, 0, 1, 0, old_pacific),
        'Sun Apr 02 03:00:01 PDT 2006',
    ),

    # Before fall back:
    (1478411999, 'Sun Nov 06 01:59:59 EDT 2016'),
    (datetime(2016, 11, 6, 0, 59, 59), 'Sun Nov 06 00:59:59 EDT 2016'),
    (
        datetime(2006, 10,29, 0, 59, 59, 0, old_pacific),
        'Sun Oct 29 00:59:59 PDT 2006',
    ),

    # Duplicated by fall back:
    # Times duplicated by DST are interpreted non-deterministically by Python
    # pre-3.6 (cf. <https://git.io/vixsE>), so there are two possible return
    # values for these calls.
    (
        datetime(2016, 11, 6, 1, 30, 0),
        ('Sun Nov 06 01:30:00 EDT 2016', 'Sun Nov 06 01:30:00 EST 2016'),
    ),
    (
        datetime(2006, 10,29, 1, 30, 0, 0, old_pacific),
        ('Sun Oct 29 01:30:00 PDT 2006', 'Sun Oct 29 01:30:00 PST 2006'),
    ),

    # After fall back:
    (1478412001, 'Sun Nov 06 01:00:01 EST 2016'),
    (datetime(2016, 11, 6, 2, 0, 1), 'Sun Nov 06 02:00:01 EST 2016'),
    (
        datetime(2006, 10,29, 2, 0, 1, 0, old_pacific),
        'Sun Oct 29 02:00:01 PST 2006',
    ),
])
def test_java_timestamp(ts, s):
    r = java_timestamp(ts)
    if isinstance(s, tuple):
        assert r in s
    else:
        assert r == s

# Times duplicated by fall back, disambiguated with `fold`:
@pytest.mark.xfail(
    hasattr(sys, "pypy_version_info") and sys.pypy_version_info[:3] < (7,2,0),
    reason='Broken on this version of PyPy',
    # Certain versions of pypy3.6 (including the one on Travis as of
    # 2020-02-23) have a bug in their datetime libraries that prevents the
    # `fold` attribute from working correctly.  The latest known version to
    # feature this bug is 7.1.1 (Python version 3.6.1), and the earliest known
    # version to feature a fix is 7.2.0 (Python version 3.6.9); I don't *think*
    # there were any releases in between those two versions, but it isn't
    # entirely clear.
)
@pytest.mark.parametrize('ts,fold,s', [
    (datetime(2016, 11, 6, 1, 30, 0), 0, 'Sun Nov 06 01:30:00 EDT 2016'),
    (
        datetime(2006, 10,29, 1, 30, 0, 0, old_pacific),
        0,
        'Sun Oct 29 01:30:00 PDT 2006',
    ),
    (datetime(2016, 11, 6, 1, 30, 0), 1, 'Sun Nov 06 01:30:00 EST 2016'),
    (
        datetime(2006, 10,29, 1, 30, 0, 0, old_pacific),
        1,
        'Sun Oct 29 01:30:00 PST 2006',
    ),
])
def test_java_timestamp_fold(ts, fold, s):
    assert java_timestamp(ts.replace(fold=fold)) == s

def test_java_timestamp_now(fixed_timestamp):
    assert java_timestamp() == fixed_timestamp

def test_java_timestamp_dogfood_type_error():
    with pytest.raises(TypeError):
        java_timestamp('Mon Dec 12 12:12:12 EST 2016')
