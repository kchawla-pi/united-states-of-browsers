from united_states_of_browsers.db_merge.table import Table


def test_suite_no_exceptions_chromium(create_chromium_data):
    chromium_db_path = create_chromium_data
    table_obj = Table(table='urls',
                      path=chromium_db_path,
                      browser='chrome',
                      filename='History',
                      profile='Profile 1',
                      copies_subpath=None,
                      )
    table_obj.make_records_yielder()
    for entry in table_obj.records_yielder:
        entry


def test_suite_no_exceptions_mozilla(create_mozilla_data):
    mozilla_db_path = create_mozilla_data
    table_obj = Table(table='moz_places',
                      path=mozilla_db_path,
                      browser='firefox',
                      filename='places.sqlite',
                      profile='test_profile0',
                      copies_subpath=None,
                      )
    table_obj.make_records_yielder()
    for entry in table_obj.records_yielder:
        entry
