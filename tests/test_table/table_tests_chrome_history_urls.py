from pathlib import Path
import test_table as tt


table_arg_no_excep = tt.TableArgs(table='urls',
                               path=Path(
		                               'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
                               browser='chrome',
                               filename='History',
                               profile='Profile 1',
                               copies_subpath=None,
                               empty=False,
                               )


project_root = Path(__file__).parents[2]
table_chrome_history_urls_no_excep = tt.TestTable(project_root, table_arg_no_excep)
tt.test_suite_no_exceptions_raised(table_chrome_history_urls_no_excep)
