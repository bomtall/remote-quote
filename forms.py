import ipywidgets as widgets

class AreaInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=10,
            min=0,
            max=1000.0,
            step=1.0,
            description='msq:',
            disabled=False,)

class SurfaceSelector(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=['Wall', 'Ceiling', 'Door', 'Doorframe', 'Skirting Board', 'Elaborate Cornice', 'Window',
                     'Windowsill', 'Spindle', 'Radiator'],
            value='Wall',
            description='Surface:',
            disabled=False)

class PaintTypeButtons(widgets.ToggleButtons):
    def __init__(self):
        super().__init__(
            options=['Emulsion Paint', 'Oil Paint', 'Custom Input'],
            description='Paint Type:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Water Based Emulsion', 'Solvent Based Paint', 'Input custom Paint Parameters'],
            value = None)



class FinishChoices(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=['Vinyl Matt Emulsion', 'Diamond Matt Emulsion', 'Silk Emulsion'],
            value='Vinyl Matt Emulsion',
            description='Finish:',
            disabled=False,)

    def get_finish_options(self, paint_type):
        if paint_type == 'Emulsion Paint':
            self.layout.visibility = 'visible'
            self.options = ['Vinyl Matt Emulsion', 'Diamond Matt Emulsion', 'Silk Emulsion']
        elif paint_type == 'Oil Paint':
            self.layout.visibility = 'visible'
            self.options = ['Eggshell', 'Gloss', 'Satinwood']
        elif paint_type == 'Custom Input':
            self.layout.visibility = 'hidden'
