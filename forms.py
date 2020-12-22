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