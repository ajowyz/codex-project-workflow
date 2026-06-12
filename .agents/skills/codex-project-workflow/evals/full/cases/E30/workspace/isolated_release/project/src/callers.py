from session.entry import open_interactive_session


def sign_in(account_id, state):
    return open_interactive_session(account_id, state)
