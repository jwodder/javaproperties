from   __future__     import unicode_literals
from   datetime       import datetime
import time
from   dateutil.tz    import tzstr
from   freezegun      import freeze_time
import pytest
from   javaproperties import java_timestamp

# Unix timestamps and datetime objects don't support leap seconds or month 13,
# so there's no need (and no way) to test handling of them here.

old_pacific = tzstr('PST8PDT,M4.1.0/M10.5.0')

@pytest.fixture(autouse=True)
def set_timezone(monkeypatch):
    monkeypatch.setenv('TZ', 'EST5EDT,M3.2.0/M11.1.0')
    time.tzset()

def test_java_timestamp_none():
    assert java_timestamp(None) == ''

def test_java_timestamp_false():
    assert java_timestamp(False) == ''

@freeze_time('2016-11-07 20:29:40')
def test_java_timestamp_now():
    assert java_timestamp() == 'Mon Nov 07 15:29:40 EST 2016'

def test_java_timestamp_zero():
    assert java_timestamp(0) == 'Wed Dec 31 19:00:00 EST 1969'

def test_java_timestamp_aware_before_spring_ahead():
    assert java_timestamp(datetime(2006, 4, 2, 1, 59, 59, 0, old_pacific)) == \
        'Sun Apr 02 01:59:59 PST 2006'

def test_java_timestamp_aware_skipped():
    assert java_timestamp(datetime(2006, 4, 2, 2, 30, 0, 0, old_pacific)) == \
        'Sun Apr 02 02:30:00 PDT 2006'

def test_java_timestamp_aware_after_spring_ahead():
    assert java_timestamp(datetime(2006, 4, 2, 3, 0, 1, 0, old_pacific)) == \
        'Sun Apr 02 03:00:01 PDT 2006'

def test_java_timestamp_aware_before_fall_back():
    assert java_timestamp(datetime(2006, 10,29, 0, 59, 59, 0, old_pacific)) == \
        'Sun Oct 29 00:59:59 PDT 2006'

def test_java_timestamp_aware_duplicated():
    # Times duplicated by DST are interpreted non-deterministically by Python
    # (cf. <https://git.io/vixsE>), so there are two possible return values for
    # this call.
    assert java_timestamp(datetime(2006, 10,29, 1, 30, 0, 0, old_pacific)) in \
        ('Sun Oct 29 01:30:00 PDT 2006', 'Sun Oct 29 01:30:00 PST 2006')
    ### Shouldn't this actually be well-defined (albeit dependent upon
    ### dateutil's implementation behavior)?

def test_java_timestamp_aware_after_fall_back():
    assert java_timestamp(datetime(2006, 10,29, 2, 0, 1, 0, old_pacific)) == \
        'Sun Oct 29 02:00:01 PST 2006'

def test_java_timestamp_low_fractional():
    assert java_timestamp(1234567890.101112) == 'Fri Feb 13 18:31:30 EST 2009'

def test_java_timestamp_high_fractional():
    assert java_timestamp(1234567890.987654) == 'Fri Feb 13 18:31:30 EST 2009'

def test_java_timestamp_january():
    assert java_timestamp(1451624400) == 'Fri Jan 01 00:00:00 EST 2016'

def test_java_timestamp_sunday():
    assert java_timestamp(1451818800) == 'Sun Jan 03 06:00:00 EST 2016'

def test_java_timestamp_monday():
    assert java_timestamp(1451883600) == 'Mon Jan 04 00:00:00 EST 2016'

def test_java_timestamp_tuesday():
    assert java_timestamp(1451973600) == 'Tue Jan 05 01:00:00 EST 2016'

def test_java_timestamp_wednesday():
    assert java_timestamp(1452063600) == 'Wed Jan 06 02:00:00 EST 2016'

def test_java_timestamp_thursday():
    assert java_timestamp(1452153600) == 'Thu Jan 07 03:00:00 EST 2016'

def test_java_timestamp_friday():
    assert java_timestamp(1452243600) == 'Fri Jan 08 04:00:00 EST 2016'

def test_java_timestamp_saturday():
    assert java_timestamp(1452333600) == 'Sat Jan 09 05:00:00 EST 2016'

def test_java_timestamp_february():
    assert java_timestamp(1454396522) == 'Tue Feb 02 02:02:02 EST 2016'

def test_java_timestamp_leap_day():
    assert java_timestamp(1456733655) == 'Mon Feb 29 03:14:15 EST 2016'

def test_java_timestamp_march():
    assert java_timestamp(1456992183) == 'Thu Mar 03 03:03:03 EST 2016'

def test_java_timestamp_before_spring_ahead():
    assert java_timestamp(1457852399) == 'Sun Mar 13 01:59:59 EST 2016'

def test_java_timestamp_naive_before_spring_ahead():
    assert java_timestamp(datetime(2016, 3, 13, 1, 59, 59)) == \
        'Sun Mar 13 01:59:59 EST 2016'

def test_java_timestamp_after_spring_ahead():
    assert java_timestamp(1457852401) == 'Sun Mar 13 03:00:01 EDT 2016'

def test_java_timestamp_naive_skipped():
    # I _think_ this behavior is guaranteed by something...
    assert java_timestamp(datetime(2016, 3, 13, 2, 30, 0)) == \
        'Sun Mar 13 03:30:00 EDT 2016'

def test_java_timestamp_naive_after_spring_ahead():
    assert java_timestamp(datetime(2016, 3, 13, 3, 0, 1)) == \
        'Sun Mar 13 03:00:01 EDT 2016'

def test_java_timestamp_april():
    assert java_timestamp(1459757044) == 'Mon Apr 04 04:04:04 EDT 2016'

def test_java_timestamp_may():
    assert java_timestamp(1462439105) == 'Thu May 05 05:05:05 EDT 2016'

def test_java_timestamp_pm():
    assert java_timestamp(1463159593) == 'Fri May 13 13:13:13 EDT 2016'

def test_java_timestamp_june():
    assert java_timestamp(1465207566) == 'Mon Jun 06 06:06:06 EDT 2016'

def test_java_timestamp_july():
    assert java_timestamp(1467889627) == 'Thu Jul 07 07:07:07 EDT 2016'

def test_java_timestamp_august():
    assert java_timestamp(1470658088) == 'Mon Aug 08 08:08:08 EDT 2016'

def test_java_timestamp_september():
    assert java_timestamp(1473426549) == 'Fri Sep 09 09:09:09 EDT 2016'

def test_java_timestamp_october():
    assert java_timestamp(1476108610) == 'Mon Oct 10 10:10:10 EDT 2016'

def test_java_timestamp_naive_before_fall_back():
    assert java_timestamp(datetime(2016, 11, 6, 0, 59, 59)) == \
        'Sun Nov 06 00:59:59 EDT 2016'

def test_java_timestamp_before_fall_back():
    assert java_timestamp(1478411999) == 'Sun Nov 06 01:59:59 EDT 2016'

def test_java_timestamp_naive_duplicated():
    # Times duplicated by DST are interpreted non-deterministically by Python
    # (cf. <https://git.io/vixsE>), so there are two possible return values for
    # this call.
    assert java_timestamp(datetime(2016, 11, 6, 1, 30, 0)) in \
        ('Sun Nov 06 01:30:00 EDT 2016', 'Sun Nov 06 01:30:00 EST 2016')

def test_java_timestamp_after_fall_back():
    assert java_timestamp(1478412001) == 'Sun Nov 06 01:00:01 EST 2016'

def test_java_timestamp_naive_after_fall_back():
    assert java_timestamp(datetime(2016, 11, 6, 2, 0, 1)) == \
        'Sun Nov 06 02:00:01 EST 2016'

def test_java_timestamp_november():
    assert java_timestamp(1478880671) == 'Fri Nov 11 11:11:11 EST 2016'

def test_java_timestamp_december():
    assert java_timestamp(1481562732) == 'Mon Dec 12 12:12:12 EST 2016'
