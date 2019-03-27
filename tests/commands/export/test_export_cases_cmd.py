# -*- coding: utf-8 -*-

from scout.commands import app_cli
from scout.server.extensions import store

def test_export_cases(mock_app, case_obj):
    """Test the CLI command that exports cases"""

    runner = mock_app.test_cli_runner()
    assert runner

    # Test the command with no options
    result =  runner.invoke(app_cli, ['export', 'cases'])
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output

    # Test the command with --case-id option
    assert store.case_collection.find().count() > 0
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--case-id', case_obj['_id']
        ])

    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output


    # Test the command with -institute option
    assert store.case_collection.find().count() > 0
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-i', case_obj['owner']
        ])

    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output


    # Test the command with -reruns option
    assert store.case_collection.find().count() > 0
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-r'
        ])
    # Test case should NOT be found
    assert result.exit_code == 0
    assert 'INFO No cases could be found' in result.output

    # Set case to be rerunned:
    store.case_collection.find_one_and_update(
        {'_id' : case_obj['_id']},
        {'$set' : {'rerun_requested' : True} }
    )
    # repeat command
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-r'
        ])
    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output


    # Test the command with -finished option
    assert store.case_collection.find().count() > 0
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-f'
        ])
    # Test case should NOT be found
    assert result.exit_code == 0
    assert 'INFO No cases could be found' in result.output
    # Set case to finished: (archived or solved)
    store.case_collection.find_one_and_update(
        {'_id' : case_obj['_id']},
        {'$set' : {'status' : 'solved'} }
    )
    # repeat command
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-f'
        ])
    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output


    # Test cli querying for cases with a specifi status (solved)
    result =  runner.invoke(app_cli, ['export', 'cases',
        '-s', 'solved'
        ])
    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output

    # Use CLI to get cases with causative variants
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--causatives'
        ])
    # Test case should NOT be found
    assert result.exit_code == 0
    assert 'INFO No cases could be found' in result.output

    # register a causative for this case
    store.case_collection.find_one_and_update(
        {'_id' : case_obj['_id']},
        {'$set' : {'causatives' : ['causative_variant_id']} }
    )
    # repeat command
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--causatives'
        ])
    # Test case should be found
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output

    # Use CLI to get cases with research requested
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--research-requested'
        ])
    # Test case should NOT be found
    assert result.exit_code == 0
    assert 'INFO No cases could be found' in result.output

    # Use CLI to get research cases
    # Use CLI to get cases with research requested
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--is-research'
        ])
    # Test case should NOT be found
    assert result.exit_code == 0
    assert 'INFO No cases could be found' in result.output

    # Set case in database to is_research and research_requested:
    store.case_collection.find_one_and_update(
        {'_id' : case_obj['_id']},
        {'$set' : {'is_research' : True, 'research_requested': True} }
    )

    # Case should be found now using both params
    result =  runner.invoke(app_cli, ['export', 'cases',
        '--is-research'
        ])
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output

    result =  runner.invoke(app_cli, ['export', 'cases',
        '--research-requested'
        ])
    assert result.exit_code == 0
    assert 'scout/demo/643594' in result.output
