import streamlit as st

class MultiApp:
    """
    Frameworks for running multiple Streamlit applications as a single app.
    referrencing https://github.com/upraneelnihar/streamlit-multiapps
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        assert isinstance(title, str)

        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
