import ipywidgets as widgets
import core
import tab_structure
import paint_link

SURFACE_TYPE_TO_CLASS_DICT = {
            'Ceiling': core.Ceiling,
            'Door': core.Door,
            'Doorframe': core.Doorframe,
            'Skirtingboard': core.Skirtingboard,
            'Elaborate Cornice': core.ElaborateCornice,
            'Window': core.Window,
            'Windowsill': core.Windowsill,
            'Spindle': core.Spindle,
            'Radiator': core.Radiator,
            'Wall': core.Wall,
        }

PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT = {
            'Vinyl Matt Emulsion': paint_link.MattEmulsionPaint,
            'Diamond Matt Emulsion': paint_link.DiamondMattEmulsion,
            'Silk Emulsion': paint_link.SilkEmulsionPaint,
            'Eggshell': paint_link.OilEggshell,
            'Gloss': paint_link.OilGloss,
            'Satinwood': paint_link.OilSatin,

}
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
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT

    def get_surface_class_from_value(self):
        if self.value in self.surface_type_to_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = 'Wall'
        surface = self.surface_type_to_class_dict[dict_key]
        return surface


class PaintTypeButtons(widgets.ToggleButtons):
    def __init__(self):
        super().__init__(
            options=['Emulsion Paint', 'Oil Paint', 'Custom Input'],
            description='Paint Type:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Water Based Emulsion', 'Solvent Based Paint', 'Input custom Paint Parameters'],
            value = 'Emulsion Paint')




class FinishChoices(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=['Vinyl Matt Emulsion', 'Diamond Matt Emulsion', 'Silk Emulsion'],
            value='Vinyl Matt Emulsion',
            description='Finish:',
            disabled=False,)
        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT
    def get_finish_options(self, paint_type):
        if paint_type == 'Emulsion Paint':
            self.layout.visibility = 'visible'
            self.options = ['Vinyl Matt Emulsion', 'Diamond Matt Emulsion', 'Silk Emulsion']
        elif paint_type == 'Oil Paint':
            self.layout.visibility = 'visible'
            self.options = ['Eggshell', 'Gloss', 'Satinwood']
        elif paint_type == 'Custom Input':
            self.options = ['Custom Input']
            self.value = 'Custom Input'
            self.layout.visibility = 'hidden'


    def get_paint_class_from_value(self):
        if self.value in self.paint_finish_type_to_paint_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = 'Vinyl Matt Emulsion'
        paint = self.paint_finish_type_to_paint_class_dict[dict_key]
        return paint


class PaintDetailsInputBox(widgets.HBox):
    def __init__(self):
        self.paint_price_input = PaintPriceInput()
        self.paint_unit_input = PaintUnitInput()
        self.paint_coverage_input = PaintCoverageInput()
        self.paint_input_widget_list = [self.paint_price_input, self.paint_unit_input, self.paint_coverage_input]
        super().__init__(self.paint_input_widget_list)
        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT

    def toggle_paint_inputs(self, paint_type):
        if paint_type == 'Custom Input':
            self.paint_price_input.disabled=False
            self.paint_unit_input.disabled = False
            self.paint_coverage_input.disabled = False
        else:
            self.paint_price_input.disabled = True
            self.paint_unit_input.disabled = True
            self.paint_coverage_input.disabled = True

    def toggle_paint_values(self, paint_finish):
        if paint_finish != 'Custom Input':
            paint = self.paint_finish_type_to_paint_class_dict[paint_finish]()
            self.paint_price_input.value = paint.price
            self.paint_unit_input.value = paint.unit
            self.paint_coverage_input.value = paint.coverage



class PaintPriceInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=30,
            min=0,
            max=1000.0,
            step=1.0,
            description='£:',
            disabled=True,
            )

class PaintUnitInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=5,
            min=0,
            max=1000.0,
            step=1.0,
            description='Unit(L):',
            disabled=True,
            )

class PaintCoverageInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=50,
            min=0,
            max=2000.0,
            step=1.0,
            description='Coverage:',
            disabled=True,
            )

class SurfaceForm(widgets.VBox):
    def __init__(self):
        self.area_input = AreaInput()
        self.surface_selector = SurfaceSelector()
        self.paint_type_buttons = PaintTypeButtons()
        self.paint_finish_dropdown = FinishChoices()
        self.paint_inputs_box = PaintDetailsInputBox()
        self.widget_dict = {
            'area_input': self.area_input,
            'surface_selector': self.surface_selector,
            'paint_type_buttons': self.paint_type_buttons,
            'paint_finish_dropdown': self.paint_finish_dropdown,
            'paint_inputs_box': self.paint_inputs_box,
        }

        super().__init__(list(self.widget_dict.values()))

        self.paint_type_buttons.observe(self.toggle_finish_visibility, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_inputs, 'value')

    def toggle_finish_visibility(self, change):
        if change['new'] == 'Custom Input':
            self.paint_finish_dropdown.layout.visibility = 'hidden'
        else:
            self.paint_finish_dropdown.layout.visibility = 'visible'

    def toggle_paint_inputs(self, change):
        self.paint_inputs_box.toggle_paint_inputs(change['new'])


class EstimateButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Estimate Job',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Calculate',
            icon='check')
        self.style.button_color='palegreen'

    # def get_estimate(self, job):
    #     estimate = job.get_total_price()
    #     return estimate

class BudgetInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=10,
            min=0,
            max=500000.0,
            step=1.0,
            description='Budget £:',
            disabled=False,)






class RemoteQuoteForm(widgets.VBox):
    def __init__(self, form_widgets_dict):
        self.form_widgets_dict = form_widgets_dict
        self.form_widgets_dict['dropdown_num_rooms'].observe(tab_structure.on_change_num_rooms)

        self.estimate_button = EstimateButton()
        self.estimate_button.on_click(self.get_estimate)
        self.output = widgets.HTML()

        super().__init__([self.form_widgets_dict['dropdown_num_rooms'], self.form_widgets_dict['tab'], self.estimate_button, self.output])
        self.job = core.Job([])

    def get_job(self):
        room_list = []
        num_rooms = self.form_widgets_dict['dropdown_num_rooms'].value
        for room_index in range(num_rooms):
            room_dict = self.form_widgets_dict['rooms']['widget_dict_list'][room_index]
            room = self.get_room(room_dict)
            room_list.append(room)
        job = core.Job(room_list)
        return job

    def get_room(self, room_dict):
        painting_surface_list = []
        num_surfaces = room_dict['dropdown_num_surfaces'].value
        for surface_index in range(num_surfaces):
            surface_dict = room_dict['surfaces']['widget_dict_list'][surface_index]
            painting_surface = self.get_painting_surface(surface_dict)
            painting_surface_list.append(painting_surface)
        room = core.Room(painting_surface_list)
        return room

    def get_painting_surface(self, surface_dict):
        surface = self.get_surface(surface_dict)
        paint = self.get_paint(surface_dict)
        return core.PaintingSurface(surface, paint)

    def get_surface(self, surface_dict):
        surface_area = surface_dict['surface_box'].area_input.value
        surface = surface_dict['surface_box'].surface_selector.get_surface_class_from_value()
        return surface(surface_area)
        #return core.Wall(8)

    def get_paint(self, surface_dict):
        paint_price = surface_dict['surface_box'].paint_inputs_box.paint_price_input.value
        paint_unit = surface_dict['surface_box'].paint_inputs_box.paint_unit_input.value
        paint_coverage = surface_dict['surface_box'].paint_inputs_box.paint_coverage_input.value
        paint_class = surface_dict['surface_box'].paint_finish_dropdown.get_paint_class_from_value()
        ##TODO move this into paint_type buttton class
        if surface_dict['surface_box'].paint_type_buttons.value == 'Custom Input':
            paint = paint_class(paint_price, paint_unit, paint_coverage)
        else:
            paint = paint_class()

        return paint


# return core.Paint(30, 5, 17)

#return core.PaintingSurface(core.Wall(8), core.Paint(30, 5, 17))



    def get_estimate(self, change):
        job = self.get_job()
        total_price = job.get_total_price()
        self.output.value = f'{total_price:.2f}'


