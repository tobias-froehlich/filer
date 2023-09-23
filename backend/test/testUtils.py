def assertThatRaisedBy(func, text):
    raised = False
    try:
        func()
    except Exception as e:
        raised = True
        assert e.args[0] == text, 'Expected: %s, Actual: %s'%(text, e.args[0])
    assert raised, 'Expected to raise exception, but did not.'


