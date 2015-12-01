from abc import abstractmethod


class Component:
    def __init__(self):
        pass

    @abstractmethod
    def render_content(self) -> str:
        pass

    @abstractmethod
    def get_settings_url(self) -> str:
        pass

    @abstractmethod
    def get_css_url(self) -> str:
        pass

    @abstractmethod
    def get_js_url(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass
