import hypothesis

from united_states_of_browsers.db_merge import browser_setup


@hypothesis.given(hypothesis.strategies.text(), hypothesis.strategies.text())
@hypothesis.seed(336502342435997634440008456922605754849)
def test_hyp_setup_profile_paths(browser_ref, profiles):
	actual_output = browser_setup.setup_profile_paths(browser_ref=browser_ref, profiles=profiles)
	print(actual_output)
	# assert expected_output == actual_output
# pytest.main('united_states_of_browsers')

