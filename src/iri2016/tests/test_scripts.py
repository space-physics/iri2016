import iri2016.time as time_profile
import iri2016.latitude as lat_profile
import iri2016.altitude as alt_profile


def test_latitude():
    lat_profile.main("2012-01-01", 300, (-60, 60, 2.0), -148)


def test_time():
    time_profile.main(("2012-01-01", "2012-01-02", 1.0), (100, 200, 20), 65, -148)


def test_alt():
    alt_profile.main("2012-01-01", (80, 1000, 10), 65, -148)
