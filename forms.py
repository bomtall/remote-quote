import ipywidgets as widgets
import core
import tab_structure
import paint_link

SURFACE_TYPE_TO_CLASS_DICT = {
            'Ceiling': core.Ceiling,
            'Door': core.Door,
            'Doorframe': core.Doorframe,
            'Skirting Board': core.Skirtingboard,
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

SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT = {
            'Pre-Painted Emulsion': core.PrePaintedEmulsion,
            'Bare Plaster': core.Plaster,
            'New Lining-Paper': core.NewLiningPaper,
            'Pre-Painted Wood': core.PrePaintedWood,
            'Bare Wood': core.NewWood,
            'Mdf': core.Mdf,
            'Custom Substrate': core.Substrate,
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
        options_list = list(SURFACE_TYPE_TO_CLASS_DICT.keys())
        self.default = options_list[0]

        super().__init__(
            options=options_list,
            value=self.default,
            description='Surface:',
            disabled=False)

        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT

    def get_surface_class_from_value(self):
        if self.value in self.surface_type_to_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = self.default
        surface = self.surface_type_to_class_dict[dict_key]
        return surface

class DesignSelector(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=[''],
            value='',
            description='Design:',
            disabled=False,)

    def get_design_options(self, surface_type):
        if surface_type == 'Door':
            self.layout.visibility = 'visible'
            self.options = ['Flat door', 'Panelled', 'Cutting in']
        elif surface_type == 'Doorframe':
            self.layout.visibility = 'visible'
            self.options = ['Standard', 'Victorian', 'Elaborate']
        elif surface_type == 'Spindle':
            self.layout.visibility = 'visible'
            self.options = ['Square', 'Shaped', 'Elaborate']
        else:
            self.options = ['']
            self.layout.visibility = 'hidden'


class NumPanesSelector(widgets.BoundedIntText):
    def __init__(self):
        super().__init__(
            value=1,
            min=1,
            max=100,
            step=1,
            description='# Panes:',
            disabled=False,)

    def display_num_panes(self, surface_type, design_type):
        if surface_type == 'Window':
            self.layout.visibility = 'visible'
        elif surface_type == 'Door' and design_type == 'Cutting in':
            self.layout.visibility = 'visible'
        else:
            self.layout.visibility = 'hidden'

    def get_num_panes_value(self):
        if self.layout.visibility == 'hidden':
            return None
        else:
            return self.value










class SurfaceForm(widgets.VBox):
    def __init__(self):
        self.area_input = AreaInput()
        self.surface_selector = SurfaceSelector()
        self.design_selector = DesignSelector()
        self.num_panes_selector = NumPanesSelector()

        self.widget_dict = {
            'area_input': self.area_input,
            'surface_selector': self.surface_selector,
            'design_selector': self.design_selector,
            'num_panes_selector': self.num_panes_selector

        }

        super().__init__(list(self.widget_dict.values()))

        self.surface_selector.observe(self.toggle_design_options, 'value')
        self.design_selector.observe(self.toggle_num_panes_design, 'value')
        self.surface_selector.observe(self.toggle_num_panes_surface , 'value')

        #setting extra option to hidden because not necessary for default surface(Wall)
        self.design_selector.layout.visibility = 'hidden'
        self.num_panes_selector.layout.visibility = 'hidden'

    def toggle_num_panes_design(self, change):
        self.num_panes_selector.display_num_panes(self.surface_selector.value, change['new'])


    def toggle_num_panes_surface(self, change):
        self.num_panes_selector.display_num_panes(change['new'], self.design_selector.value)

    def toggle_design_options(self, change):
        self.design_selector.get_design_options(change['new'])


class InputSubstrate(widgets.ToggleButtons):
    def __init__(self):
        options_list = list(SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT.keys())
        super().__init__(
            options=options_list,
            description='Substrate:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['any substrate which is already coated in emulsion', 'Newly plastered surface',
                      'Lining paper with no coating', 'Wood which has already been painted with an oil paint',
                      'Bare wood with no coating', 'medium density fibre board, primed or un-primed'],
            value = options_list[0],
        )

class InputCondition(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=['poor', 'okay', 'good'],
            value='good',
            description='Condition:',
            disabled=False,)



class InputNumCoats(widgets.BoundedIntText):
    def __init__(self):
        super().__init__(
            value=1,
            min=1,
            max=3,
            step=1,
            description='# Coats',
            disabled=True,)

class InputCoverageAdjustment(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=1.0,
            min=1.0,
            max=10.0,
            step=0.1,
            description='Coveradjust',
            disabled=True,)

class InputSubstrateDetails(widgets.Accordion):
    def __init__(self):
        self.input_num_coats = InputNumCoats()
        self.input_coverage_adjustment = InputCoverageAdjustment()
        self.substrate_input_to_substrate_class_dict = SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT
        self.widget_dict = {
            'input_num_coats': self.input_num_coats,
            'input_coverage_adjustment': self.input_coverage_adjustment,
        }
        super().__init__(children=[widgets.HBox(list(self.widget_dict.values()))], selected_index=None)
        self.set_title(0, "Substrate Details...")

    def toggle_substrate_details(self, substrate_type, condition):
        if substrate_type != 'Custom Substrate':
            self.input_num_coats.disabled=True
            self.input_coverage_adjustment.disabled=True
        else:
            self.input_num_coats.disabled=False
            self.input_coverage_adjustment.disabled=False

        substrate = self.substrate_input_to_substrate_class_dict[substrate_type](condition=condition)
        self.input_num_coats.value = substrate.num_coats
        self.input_coverage_adjustment.value = substrate.coverage_adjustment



class SubstrateForm(widgets.VBox):
    def __init__(self):
        self.input_substrate = InputSubstrate()
        self.input_condition = InputCondition()
        self.input_substrate_details = InputSubstrateDetails()
        self.substrate_input_to_substrate_class_dict = SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT
        self.widget_list_dict = {
            'input_substrate': self.input_substrate,
            'input_condition': self.input_condition,
            'input_substrate_details': self.input_substrate_details,
            }

        self.input_condition.observe(self.toggle_substrate_details_on_condition, 'value')
        self.input_substrate.observe(self.toggle_substrate_details_on_substrate, 'value')

        super().__init__(list(self.widget_list_dict.values()))

    def toggle_substrate_details_on_condition(self, change):
        self.input_substrate_details.toggle_substrate_details(self.input_substrate.value, change['new'])

    def toggle_substrate_details_on_substrate(self, change):
        self.input_substrate_details.toggle_substrate_details(change['new'], self.input_condition.value)



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
            self.value = 'Vinyl Matt Emulsion'
        elif paint_type == 'Oil Paint':
            self.layout.visibility = 'visible'
            self.options = ['Eggshell', 'Gloss', 'Satinwood']
            self.value = 'Eggshell'
        elif paint_type == 'Custom Input':
            self.layout.visibility = 'hidden'


    def get_paint_class_from_value(self):
        if self.value in self.paint_finish_type_to_paint_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = 'Vinyl Matt Emulsion'
        paint = self.paint_finish_type_to_paint_class_dict[dict_key]
        return paint


class PaintDetailsInputBox(widgets.Accordion):
    def __init__(self):
        self.paint_price_input = PaintPriceInput()
        self.paint_unit_input = PaintUnitInput()
        self.paint_coverage_input = PaintCoverageInput()
        self.paint_input_widget_list = [self.paint_price_input, self.paint_unit_input, self.paint_coverage_input]
        super().__init__(children=[widgets.HBox(self.paint_input_widget_list)], selected_index=None)
        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT
        self.set_title(0, 'Paint Details...')

    def toggle_paint_inputs(self, paint_type):
        if paint_type == 'Custom Input':
            self.paint_price_input.disabled=False
            self.paint_unit_input.disabled = False
            self.paint_coverage_input.disabled = False
        else:
            self.paint_price_input.disabled = True
            self.paint_unit_input.disabled = True
            self.paint_coverage_input.disabled = True

    def toggle_paint_values(self, paint_finish, paint_type):

        if paint_type != 'Custom Input':
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

class PaintForm(widgets.VBox):
    def __init__(self):

        self.paint_type_buttons = PaintTypeButtons()
        self.paint_finish_dropdown = FinishChoices()
        self.paint_inputs_box = PaintDetailsInputBox()
        self.widget_dict = {

            'paint_type_buttons': self.paint_type_buttons,
            'paint_finish_dropdown': self.paint_finish_dropdown,
            'paint_inputs_box': self.paint_inputs_box,
        }


        super().__init__(list(self.widget_dict.values()))


        self.paint_type_buttons.observe(self.toggle_finish_visibility, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_inputs, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_values_on_paint_type, 'value')
        self.paint_finish_dropdown.observe(self.toggle_paint_values_on_paint_finish, 'value')

    def toggle_finish_visibility(self, change):
        if change['new'] == 'Custom Input':
            self.paint_finish_dropdown.layout.visibility = 'hidden'
        else:
            self.paint_finish_dropdown.layout.visibility = 'visible'

    def toggle_paint_inputs(self, change):
        self.paint_inputs_box.toggle_paint_inputs(change['new'])

    def toggle_paint_values_on_paint_type(self, change):
        self.paint_inputs_box.toggle_paint_values(self.paint_finish_dropdown.value, change['new'])
    def toggle_paint_values_on_paint_finish(self, change):
        self.paint_inputs_box.toggle_paint_values(change['new'], self.paint_type_buttons.value)


class CalculateBox(widgets.HBox):
    def __init__(self):
        self.estimate_button = EstimateButton()
        self.budget_input = BudgetInput()
        self.optimise_button = OptimiseButton()
        self.download_button = DownloadButton()
        self.widget_dict = {
            'estimate_button': self.estimate_button,
            'budget_input': self.budget_input,
            'optimise_button': self.optimise_button,
            'download_button':  self.download_button,
        }
        super().__init__(list(self.widget_dict.values()))

class EstimateButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Estimate Job',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Calculate',
            icon='check')
        self.style.button_color='palegreen'

class DownloadButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Download Quote',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Download a text file with your job breakdown',
            icon='check')
        self.style.button_color='lightblue'

class BudgetInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=10,
            min=0,
            max=500000.0,
            step=1.0,
            description='Budget £:',
            disabled=False,)

class OptimiseButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Optimise Job',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Calculate Budget Optimisation',
            icon='check')
        self.style.button_color='pink'

class SurfaceBox(widgets.VBox):
    def __init__(self):
        self.surface_form = SurfaceForm()
        self.substrate_form = SubstrateForm()
        self.paint_form = PaintForm()
        self.widget_dict = {
            'surface_form': self.surface_form,
            'substrate_form': self.substrate_form,
            'paint_form': self.paint_form,
        }

        super().__init__(list(self.widget_dict.values()))



class RemoteQuoteForm(widgets.VBox):
    def __init__(self, form_widgets_dict):
        self.form_widgets_dict = form_widgets_dict
        self.form_widgets_dict['dropdown_num_rooms'].observe(tab_structure.on_change_num_rooms)
        self.calculate_box = CalculateBox()
        self.calculate_box.estimate_button.on_click(self.get_estimate)
        self.output = widgets.HTML()

        super().__init__([self.form_widgets_dict['dropdown_num_rooms'], self.form_widgets_dict['tab'], self.calculate_box, self.output])
        self.job = core.Job([])

    def get_estimate(self, change):
        try:
            job = self.get_job()
            total_price = job.get_total_price()
            self.output.value = f'{total_price:.2f}'
        except KeyError as e:
            if e.args[0] == 'widget_dict_list':
                self.output.value = 'Rooms with unselected surfaces. Please select.'
            else:
                raise

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
        surface_form = surface_dict['surface_box'].surface_form
        substrate_form = surface_dict['surface_box'].substrate_form
        paint_form = surface_dict['surface_box'].paint_form

        surface = self.get_surface(surface_form, substrate_form)
        paint = self.get_paint(paint_form)
        return core.PaintingSurface(surface, paint)

    def get_surface(self, surface_form, substrate_form):
        surface_area = surface_form.area_input.value
        surface = surface_form.surface_selector.get_surface_class_from_value()
        design = surface_form.design_selector.get_design_options(surface_form.surface_selector.value)
        num_panes = surface_form.num_panes_selector.get_num_panes_value()
        substrate = self.get_substrate(substrate_form)
        return surface(surface_area, design=design, num_panes=num_panes, substrate=substrate)
        #return core.Wall(8)

    def get_substrate(self, substrate_form):
        substrate_type = substrate_form.input_substrate.value
        if substrate_type == 'Custom Substrate':
            num_coats = substrate_form.input_substrate_details.input_num_coats.value
            coverage_adjustment = substrate_form.input_substrate_details.input_coverage_adjustment.value
            substrate = core.Substrate(num_coats=num_coats, coverage_adjustment=coverage_adjustment)
        else:
            substrate = substrate_form.substrate_input_to_substrate_class_dict[substrate_type]()
        return substrate

    def get_paint(self, paint_form):
        paint_price = paint_form.paint_inputs_box.paint_price_input.value
        paint_unit = paint_form.paint_inputs_box.paint_unit_input.value
        paint_coverage = paint_form.paint_inputs_box.paint_coverage_input.value
        paint_class = paint_form.paint_finish_dropdown.get_paint_class_from_value()
        ##TODO move this into paint_type buttton class
        if paint_form.paint_type_buttons.value == 'Custom Input':
            paint = paint_class(paint_price, paint_unit, paint_coverage)
        else:
            paint = paint_class()
        return paint








