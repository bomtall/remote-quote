import core
import forms
import tab_structure
import ipywidgets as widgets


class RemoteQuoteForm(widgets.VBox):
    def __init__(self, form_widgets_dict):
        self.estimate_button = forms.EstimateButton()
        super.__init__(
            [self.form_widgets_dict['dropdown_num_rooms'], self.form_widgets_dict['tab'], self.estimate_button])
        self.job = core.Job()