from abc import ABC, abstractmethod
import gradio as gr


class AbstractBaseUI(UIPage):
    '''Base class for the GUI. This class is responsible for creating the UI and launching the server.'''
    max_choices = 20
    ui_asset_dataframe = gr.Dataframe(interactive=False)
    LOGO_PATH = "http://localhost:31415/file=public/logo.png"
    LOGO_DIM = 64

    def __init__(self, ui_name='default'):
        super().__init__()
        self.ui_name = ui_name
        self.content_automation = None
        self.asset_library_ui = None
        self.config_ui = None

    @abstractmethod
    def init_components(self):
        """Initialize UI components"""
        pass

    @abstractmethod
    def create_ui(self):
        """Create the UI layout"""
        pass

    def launch(self, **kwargs):
        """Launch the UI"""
        if not self.interface:
            self.interface = self.create_ui()
        self.interface.launch(**kwargs)

    def queue(self):
        """Enable queueing for the UI"""
        if self.interface:
            self.interface.queue()

    def get_interface(self):
        """Get the Gradio interface"""
        if not self.interface:
            self.interface = self.create_ui()
        return self.interface

    def create_interface(self):
        raise NotImplementedError
