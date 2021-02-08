import ipywidgets as widgets
import core
import tab_structure
import base64


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------- Dictionaries to map the user inputs to classes ---------------------------------
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
    'Vinyl Matt Emulsion': core.MattEmulsionPaint,
    'Diamond Matt Emulsion': core.DiamondMattEmulsion,
    'Silk Emulsion': core.SilkEmulsionPaint,
    'Eggshell': core.OilEggshell,
    'Gloss': core.OilGloss,
    'Satinwood': core.OilSatin,
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

# --------------------------------------------------- Other Dictionaries -----------------------------------------------
PAINT_TYPE_TO_FINISH_OPTIONS_DICT = {
    'Emulsion Paint': ['Vinyl Matt Emulsion', 'Diamond Matt Emulsion', 'Silk Emulsion'],
    'Oil Paint': ['Eggshell', 'Gloss', 'Satinwood'],
    'Custom Input': None,
}

OPTIMISATION_TYPE_TO_OPTIMISER = {
    'Max surface area': core.Job.get_optimised_job,
    'Max rooms by surface area': core.Job.get_optimised_rooms_job,
    'Max rooms by condition and surface area': core.Job.get_optimised_condition_job,
}

HTML_PARAGRAPH_DICT = {
    'heading_paragraph':'''Create your own quotation for Painting & Decorating and optimise the quote for your budget.
                            <br>                     
                            Select the number of rooms you want to estimate. Once selected, the number of rooms is set. 
                            Click refresh to start again.<br> 
                            Once you have created your rooms, select the correct number of
                             surfaces in each room before you select any options.<br> Click "download info" below for
                              a full set of instructions.<br>
                              If not used for 15 minutes you will need to re-load RemoteQuote again.''',
    'surface_paragraph_string': '''In this section select the details of your surface.
                                    Each surface added can be multiple surfaces of the same type within a room 
                                    i.e all the walls can be entered as one wall if they are to be painted the same
                                    colour and are in the same condition''',
    'substrate_paragraph': '''Enter the details of the surface material and the condition. All surfaces in poor
                            condition require 2 coats''',
    'paint_paragraph': '''Choose a pre-set paint from Dulux or choose custom input and enter details of another 
                        paint''',


}


TOOLTIPS_DICT ={
    'surface_tip': 'To measure the surface area of multiple surfaces which are the same type, for example walls or'
                   ' skirting board, measure the height once and multiply by the distance around the room.',
    'substrate_tip': 'The surface material to be painted over will affect the coverage performance of paint and the'
                     ' number of coats necessary for a satisfactory finish. Choose custom substrate to change the'
                     ' number of coats and enter a coverage adjustment. Good condition is when there is almost no'
                     ' preparation necessary, okay condition is when there is some reasonable level of preparation,'
                     ' some small cracks, and/or some imperfections. Poor is when there is any of: flaking paint, large'
                     ' cracks, stains or damage. You can choose poor condition when new plastering has been done badly'
                     ' or when selecting new wood and the joinery is of a poor standard with large gaps to fill and '
                     'repair. ',
    'paint_tip':'All defaults are based on full price dulux paints in brilliant white. Prices for mixed colours are'
                ' slightly more expensive. Choose custom inputs to enter details of a paint you wish to use, or a '
                'similar paint but in a different unit size',

}

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------- Surface widgets  -------------------------------------------------
# Widgets to take inputs area, surface, design and num_panes from user
class SurfaceInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Surface Info',
            disabled=False,
            button_style='',
            tooltip=TOOLTIPS_DICT['surface_tip'],
            icon='fa-lightbulb-o',
        )

        self.style.button_color = 'lightblue'


class AreaInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=10,
            min=0,
            max=1000.0,
            step=1.0,
            description='msq:',
            disabled=False,
        )


class SurfaceSelector(widgets.Dropdown):
    def __init__(self):
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT
        self.default = list(SURFACE_TYPE_TO_CLASS_DICT.keys())[0]

        super().__init__(
            options=list(self.surface_type_to_class_dict.keys()),
            value=self.default,
            description='Surface:',
            disabled=False,
        )

    def get_surface_class_from_value(self):
        if self.value in self.surface_type_to_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = self.default
        surface = self.surface_type_to_class_dict[dict_key]
        return surface


class DesignSelector(widgets.Dropdown):
    def __init__(self):
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT

        super().__init__(
            options=[''],
            value='',
            description='Design:',
            disabled=False,
        )

    def get_design_options(self, surface_type):
        design_options = self.surface_type_to_class_dict[surface_type](10).design_options
        if design_options is None:
            self.options = ['']
            self.layout.visibility = 'hidden'
        else:
            self.layout.visibility = 'visible'
            self.options = design_options


class NumPanesSelector(widgets.BoundedIntText):
    def __init__(self):
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT

        super().__init__(
            value=1,
            min=1,
            max=100,
            step=1,
            description='# Panes:',
            disabled=False,
        )

    def display_num_panes(self, surface_type, design_type):
        num_panes = self.surface_type_to_class_dict[surface_type](10, design=design_type).num_panes
        if (num_panes is None) or (num_panes == 0):
            self.layout.visibility = 'hidden'
        else:
            self.layout.visibility = 'visible'

    def get_num_panes_value(self):
        if self.layout.visibility == 'hidden':
            return None
        else:
            return self.value


# ----------------------------------------------- Surface form ---------------------------------------------------------
# Widget to combine widgets for area, surface, design and num panes
class SurfaceForm(widgets.VBox):
    def __init__(self):
        #self.html_paragraph_dict = HTML_PARAGRAPH_DICT
        self.surface_heading = widgets.HTML(
            '<h2 style="font-family:georgia;background-color:#EDF9F4; color:#4FAD99">Surface Inputs</h2>')
        self.surface_paragraph = widgets.HTML(
            f'<p style="font-family:georgia; background-color:#EDF9F4; color:#4FAD99">'
            f'{HTML_PARAGRAPH_DICT["surface_paragraph_string"]}</p>')
        self.surface_info = SurfaceInfoButton()
        self.area_input = AreaInput()
        self.surface_selector = SurfaceSelector()
        self.design_selector = DesignSelector()
        self.num_panes_selector = NumPanesSelector()


        self.widget_dict = {
            'surface_heading': self.surface_heading,
            'surface_paragraph': self.surface_paragraph,
            'surface_info': self.surface_info,
            'area_input': self.area_input,
            'surface_selector': self.surface_selector,
            'design_selector': self.design_selector,
            'num_panes_selector': self.num_panes_selector,

        }

        super().__init__(list(self.widget_dict.values()))

        self.surface_selector.observe(self.toggle_design_options, 'value')
        self.design_selector.observe(self.toggle_num_panes_design, 'value')
        self.surface_selector.observe(self.toggle_num_panes_surface, 'value')

        # Run the observe functions to set up design options and number of panes whose default settings
        # depend on surface type
        self.design_selector.get_design_options(self.surface_selector.value)
        self.num_panes_selector.display_num_panes(self.surface_selector.value, self.design_selector.value)

    def toggle_num_panes_design(self, change):
        self.num_panes_selector.display_num_panes(self.surface_selector.value, change['new'])

    def toggle_num_panes_surface(self, change):
        self.num_panes_selector.display_num_panes(change['new'], self.design_selector.value)

    def toggle_design_options(self, change):
        self.design_selector.get_design_options(change['new'])


# ----------------------------------------------------------------------------------------------------------------------
#  ----------------------------------------------- Substrate widgets  --------------------------------------------------
# Widgets for substrate, condition, num coats and coverage adjustment
class SubstrateInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Substrate Info',
            disabled=False,
            button_style='',
            tooltip=TOOLTIPS_DICT['substrate_tip'],
            icon='fa-lightbulb-o',
        )

        self.style.button_color = 'lightblue'


class InputSubstrate(widgets.ToggleButtons):
    def __init__(self):
        options_list = list(SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT.keys())

        super().__init__(
            options=options_list,
            description='Substrate:',
            disabled=False,
            button_style='',
            tooltips=['any substrate which is already coated in emulsion', 'Newly plastered surface',
                      'Lining paper with no coating', 'Wood which has already been painted with an oil paint',
                      'Bare wood with no coating', 'medium density fibre board, primed or un-primed'],
            value=options_list[0],
        )


class InputCondition(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            options=core.CONDITION_OPTIONS,
            value=core.CONDITION_OPTIONS[0],
            description='Condition:',
            disabled=False,
        )


class InputNumCoats(widgets.BoundedIntText):
    def __init__(self):
        super().__init__(
            value=1,
            min=1,
            max=3,
            step=1,
            description='# Coats',
            disabled=True,
        )


class InputCoverageAdjustment(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=1.0,
            min=1.0,
            max=10.0,
            step=0.1,
            description='Coveradjust',
            disabled=True,
        )


class InputSubstrateDetails(widgets.Accordion):
    def __init__(self):
        self.input_num_coats = InputNumCoats()
        self.input_coverage_adjustment = InputCoverageAdjustment()
        self.substrate_input_to_substrate_class_dict = SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT
        self.widget_dict = {
            'input_num_coats': self.input_num_coats,
            'input_coverage_adjustment': self.input_coverage_adjustment,
        }

        super().__init__(
            children=[widgets.HBox(list(self.widget_dict.values()))],
            selected_index=None)

        self.set_title(0, "Substrate Details...")

    def toggle_substrate_details(self, substrate_type, condition):
        if substrate_type != 'Custom Substrate':
            disabled = True
        else:
            disabled = False

        self.input_num_coats.disabled = disabled
        self.input_coverage_adjustment.disabled = disabled

        substrate = self.substrate_input_to_substrate_class_dict[substrate_type](condition=condition)
        self.input_num_coats.value = substrate.num_coats
        self.input_coverage_adjustment.value = substrate.coverage_adjustment


# --------------------------------------------- Substrate form ---------------------------------------------------------
# Substrate form to combine widgets for substrate type, condition, num coats and coverage adjustment
# to create Substrate class
class SubstrateForm(widgets.VBox):
    def __init__(self):
        self.substrate_heading = widgets.HTML(
            '<h2 style="font-family:georgia;background-color:#EDF9F4; color:#4FAD99">Substrate Inputs</h2>')
        self.substrate_paragraph = widgets.HTML(
            f'<p style="font-family:georgia; background-color:#EDF9F4; color:#4FAD99">'
            f'{HTML_PARAGRAPH_DICT["substrate_paragraph"]}</p>')
        self.substrate_info = SubstrateInfoButton()
        self.input_substrate = InputSubstrate()
        self.input_condition = InputCondition()
        self.input_substrate_details = InputSubstrateDetails()
        self.substrate_input_to_substrate_class_dict = SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT
        self.widget_list_dict = {
            'substrate_heading': self.substrate_heading,
            'substrate_paragraphself': self.substrate_paragraph,
            'substrate_info': self.substrate_info,
            'input_substrate': self.input_substrate,
            'input_condition': self.input_condition,
            'input_substrate_details': self.input_substrate_details,

            }

        self.input_condition.observe(self.toggle_substrate_details_on_condition, 'value')
        self.input_substrate.observe(self.toggle_substrate_details_on_substrate, 'value')

        super().__init__(list(self.widget_list_dict.values()))

        # Run the observe functions to set up substrate details whose default settings depend on surface type
        self.input_substrate_details.toggle_substrate_details(self.input_substrate.value, self.input_condition.value)

    def toggle_substrate_details_on_condition(self, change):
        self.input_substrate_details.toggle_substrate_details(self.input_substrate.value, change['new'])

    def toggle_substrate_details_on_substrate(self, change):
        self.input_substrate_details.toggle_substrate_details(change['new'], self.input_condition.value)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------- Paint widgets --------------------------------------------------------
# Widgets for paint type, finish and paint details (price, unit, coverage)
class PaintInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Paint Info',
            disabled=False,
            button_style='',
            tooltip=TOOLTIPS_DICT['paint_tip'],
            icon='fa-lightbulb-o',
        )

        self.style.button_color = 'lightblue'


class PaintTypeButtons(widgets.ToggleButtons):
    def __init__(self):
        options = list(PAINT_TYPE_TO_FINISH_OPTIONS_DICT.keys())
        super().__init__(
            options=options,
            description='Paint Type:',
            disabled=False,
            button_style='',
            tooltips=['Water Based Emulsion', 'Solvent Based Paint', 'Input custom Paint Parameters'],
            value=options[0],
        )


class FinishChoices(widgets.Dropdown):
    def __init__(self):
        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT
        self.paint_type_to_finish_options_dict = PAINT_TYPE_TO_FINISH_OPTIONS_DICT

        default_paint_type = PaintTypeButtons().value
        default_options = self.paint_type_to_finish_options_dict[default_paint_type]
        default_finish = default_options[0]

        self.default = default_finish
        super().__init__(
            options=default_options,
            value=default_finish,
            description='Finish:',
            disabled=False,
        )

    def toggle_finish_options(self, paint_type):
        options = self.paint_type_to_finish_options_dict[paint_type]

        if options is None:
            self.layout.visibility = 'hidden'
        else:
            self.layout.visibility = 'visible'
            self.options = self.paint_type_to_finish_options_dict[paint_type]
            self.value = self.paint_type_to_finish_options_dict[paint_type][0]

    def get_paint_class_from_value(self):
        if self.value in self.paint_finish_type_to_paint_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = self.default
        paint = self.paint_finish_type_to_paint_class_dict[dict_key]
        return paint


class PaintDetailsInputBox(widgets.Accordion):
    def __init__(self):
        self.paint_price_input = PaintPriceInput()
        self.paint_unit_input = PaintUnitInput()
        self.paint_coverage_input = PaintCoverageInput()
        self.paint_input_widget_list = [self.paint_price_input, self.paint_unit_input, self.paint_coverage_input]

        super().__init__(
            children=[widgets.HBox(self.paint_input_widget_list)],
            selected_index=None
        )

        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT
        self.set_title(0, 'Paint Details...')

    def toggle_paint_inputs(self, paint_type):
        if paint_type == 'Custom Input':
            disabled = False
        else:
            disabled = True

        self.paint_price_input.disabled = disabled
        self.paint_unit_input.disabled = disabled
        self.paint_coverage_input.disabled = disabled

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


# ----------------------------------------------- Paint form -----------------------------------------------------------
# Paint form combining widgets for paint type, paint finish, paint inputs (price, unit, coverage) to make Paint class
class PaintForm(widgets.VBox):
    def __init__(self):
        self.paint_heading = widgets.HTML('<h2 style="font-family:georgia;background-color:#EDF9F4;'
                                          ' color:#4FAD99">Paint Inputs</h2>')
        self.paint_paragraph = widgets.HTML('<p style="font-family:georgia; background-color:#EDF9F4;'
                                            f' color:#4FAD99">{HTML_PARAGRAPH_DICT["paint_paragraph"]}</p>')
        self.paint_info = PaintInfoButton()
        self.paint_type_buttons = PaintTypeButtons()
        self.paint_finish_dropdown = FinishChoices()
        self.paint_inputs_box = PaintDetailsInputBox()
        self.widget_dict = {
            'paint_heading': self.paint_heading,
            'paint_paragraph': self.paint_paragraph,
            'paint_info':self.paint_info,
            'paint_type_buttons': self.paint_type_buttons,
            'paint_finish_dropdown': self.paint_finish_dropdown,
            'paint_inputs_box': self.paint_inputs_box,
        }

        super().__init__(list(self.widget_dict.values()))

        self.paint_type_buttons.observe(self.toggle_finish_visibility, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_inputs, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_values_on_paint_type, 'value')
        self.paint_finish_dropdown.observe(self.toggle_paint_values_on_paint_finish, 'value')

        # Run the observe functions to set up paint input details and finish whose default settings
        # depend on paint type and paint finish
        self.paint_finish_dropdown.toggle_finish_options(self.paint_type_buttons.value)
        self.paint_inputs_box.toggle_paint_inputs(self.paint_type_buttons.value)
        self.paint_inputs_box.toggle_paint_values(self.paint_finish_dropdown.value, self.paint_type_buttons.value)

    def toggle_finish_visibility(self, change):
        self.paint_finish_dropdown.toggle_finish_options(change['new'])

    def toggle_paint_inputs(self, change):
        self.paint_inputs_box.toggle_paint_inputs(change['new'])

    def toggle_paint_values_on_paint_type(self, change):
        self.paint_inputs_box.toggle_paint_values(self.paint_finish_dropdown.value, change['new'])

    def toggle_paint_values_on_paint_finish(self, change):
        self.paint_inputs_box.toggle_paint_values(change['new'], self.paint_type_buttons.value)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Surface box -----------------------------------------------------------
# Combines widgets for surface, substrate and paint inputs to put into the tabular structure
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


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------- Calculation widgets------------------------------------------------------
# Widgets for calculation box (estimate, optimise, budget input, download)
class EstimateButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Estimate Job',
            disabled=False,
            button_style='',
            tooltip='Calculate',
            icon='check',
        )

        self.style.button_color = 'palegreen'


class BudgetInput(widgets.BoundedIntText):
    def __init__(self):
        super().__init__(
            value=250,
            min=0,
            max=500000,
            step=1,
            description='Budget £:',
            disabled=False,
        )


class OptimiseDropdown(widgets.Dropdown):
    def __init__(self):
        self.optimisation_type_to_optimiser = OPTIMISATION_TYPE_TO_OPTIMISER
        super().__init__(
            options=list(self.optimisation_type_to_optimiser.keys()),
            value=list(self.optimisation_type_to_optimiser.keys())[0],
            description='Method:',
            disabled=True,
        )


class OptimiseButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Optimise Job',
            disabled=True,
            button_style='',
            tooltip='Calculate Budget Optimisation',
            icon='fa-calculator',
        )

        self.style.button_color = 'pink'

# -------------------------------------------- Calculation box ---------------------------------------------------------
# Calculate box combining widgets for estimate, budget input, optimise, download
class CalculateBox(widgets.VBox):
    def __init__(self):
        self.estimate_button = EstimateButton()
        self.output = widgets.HTML()
        self.budget_input = BudgetInput()
        self.optimise_dropdown = OptimiseDropdown()
        self.optimise_button = OptimiseButton()
        self.optimised_output = widgets.HTML()
        self.optimised_download_output = widgets.HTML()
        self.download_output = widgets.HTML()
        self.widget_dict = {
            'estimate_button': self.estimate_button,
            'output': self.output,
            'budget_input': self.budget_input,
            'optimise_dropdown': self.optimise_dropdown,
            'optimise_button': self.optimise_button,
            'optimised_output': self.optimised_output,
            'download_optimised_output': self.optimised_download_output,
            'download_output': self.download_output,
        }

        super().__init__(list(self.widget_dict.values()))


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ Remote Quote Form ---------------------------------------------------
# Remote quote form combining the widget containing the tabular structure of rooms and surfaces together with the
# calculation box and outputs
class RemoteQuoteForm(widgets.VBox):
    def __init__(self, form_widgets_dict):

        self.form_widgets_dict = form_widgets_dict
        self.form_widgets_dict['dropdown_num_rooms'].observe(tab_structure.on_change_num_rooms)
        self.form_widgets_dict['dropdown_num_rooms'].observe(self.freeze_room_dropdown)

        self.calculate_box = CalculateBox()
        self.calculate_box.estimate_button.on_click(self.get_estimate)
        self.calculate_box.optimise_button.on_click(self.get_optimised_job)

        super().__init__([self.form_widgets_dict['dropdown_num_rooms'], self.form_widgets_dict['tab'],
                          self.calculate_box])
        self.job = core.Job([])

    def freeze_room_dropdown(self, change):
        self.form_widgets_dict['dropdown_num_rooms'].disabled = True

    def get_download(self):
        res = f'''
            Your RemoteQuote

    Breakdown:
    {self.job.get_breakdown()}

        '''
        # FILE
        filename = 'quote.txt'
        b64 = base64.b64encode(res.encode())
        payload = b64.decode()

        # BUTTONS
        html_buttons = '''<html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <a download="{filename}" href="data:text/csv;base64,{payload}" download>
                <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-info">
                    <i class="fa fa-download"> Download Quote
                </button>
            </a>
        </body>
        </html>
        '''

        html_button = html_buttons.format(payload=payload, filename=filename)
        self.calculate_box.download_output.value = html_button

    def get_optimised_job(self, change):
        optimise_function = self.calculate_box.optimise_dropdown.optimisation_type_to_optimiser[
            self.calculate_box.optimise_dropdown.value]
        optimised_job = optimise_function(self.job, self.calculate_box.budget_input.value)
        self.calculate_box.optimised_output.value = f'{optimised_job.get_summary()}'
        res = f'''
                    Your RemoteQuote Optimised Job


        A Summary of Your Optimised Quote:
        {optimised_job.get_summary()} 

        A Detailed Breakdown of Your Optimised Quote:
        {optimised_job.get_breakdown()}
                '''
        # FILE
        filename = 'quote.txt'
        b64 = base64.b64encode(res.encode())
        payload = b64.decode()

        # BUTTONS
        html_buttons = '''<html>
                        <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        </head>
                        <body>
                            <a download="{filename}" href="data:text/csv;base64,{payload}" download>
                                <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-info">
                                    <i class="fa fa-download"> Optimised Job
                                </button>
                            </a>
                        </body>
                        </html>
                        '''

        html_button = html_buttons.format(payload=payload, filename=filename)
        self.calculate_box.optimised_download_output.value = html_button

    def get_estimate(self, change):
        try:
            self.job = self.get_job()
            total_price = self.job.get_total_price()
            self.calculate_box.output.value = f'{total_price:.2f}'

            self.get_download()
            self.calculate_box.optimise_button.disabled = False
            self.calculate_box.optimise_dropdown.disabled = False

        except KeyError as e:
            if e.args[0] == 'widget_dict_list':
                self.calculate_box.output.value = 'Rooms with unselected surfaces. Please select.'
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
        room_name = room_dict['room_title'].value
        num_surfaces = room_dict['dropdown_num_surfaces'].value
        for surface_index in range(num_surfaces):
            surface_dict = room_dict['surfaces']['widget_dict_list'][surface_index]
            painting_surface = self.get_painting_surface(surface_dict)
            painting_surface_list.append(painting_surface)

        room = core.Room(painting_surface_list, name=room_name)
        return room

    def get_painting_surface(self, surface_dict):
        surface_name = surface_dict['surface_title'].value
        surface_form = surface_dict['surface_box'].surface_form
        substrate_form = surface_dict['surface_box'].substrate_form
        paint_form = surface_dict['surface_box'].paint_form

        surface = self.get_surface(surface_form, substrate_form)
        paint = self.get_paint(paint_form)
        surface.name = surface.name + surface_name
        return core.PaintingSurface(surface, paint)

    def get_surface(self, surface_form, substrate_form):
        surface_area = surface_form.area_input.value
        surface = surface_form.surface_selector.get_surface_class_from_value()
        design = surface_form.design_selector.get_design_options(surface_form.surface_selector.value)
        num_panes = surface_form.num_panes_selector.get_num_panes_value()
        substrate = self.get_substrate(substrate_form)
        return surface(surface_area, design=design, num_panes=num_panes, substrate=substrate)

    @staticmethod
    def get_substrate(substrate_form):
        substrate_type = substrate_form.input_substrate.value
        if substrate_type == 'Custom Substrate':
            num_coats = substrate_form.input_substrate_details.input_num_coats.value
            coverage_adjustment = substrate_form.input_substrate_details.input_coverage_adjustment.value
            substrate = core.Substrate(num_coats=num_coats, coverage_adjustment=coverage_adjustment)
        else:
            substrate = substrate_form.substrate_input_to_substrate_class_dict[substrate_type](
                condition=substrate_form.input_condition.value)
        return substrate

    @staticmethod
    def get_paint(paint_form):
        paint_price = paint_form.paint_inputs_box.paint_price_input.value
        paint_unit = paint_form.paint_inputs_box.paint_unit_input.value
        paint_coverage = paint_form.paint_inputs_box.paint_coverage_input.value
        paint_class = paint_form.paint_finish_dropdown.get_paint_class_from_value()
        if paint_form.paint_type_buttons.value == 'Custom Input':
            paint = paint_class(paint_price, paint_unit, paint_coverage)
        else:
            paint = paint_class()
        return paint

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Other widgets required for Final GUI ------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- GUI HTML Heading & Paragraph ------------------------------------------
class GUIHeading(widgets.HTML):
    def __init__(self):
        heading = '<h1 style="color:#4FAD99; background-color:#EDF9F4; font-family:georgia;">RemoteQuote</h1>'
        super().__init__(heading)


class GUIInstructionParagraph(widgets.HTML):
    def __init__(self):
        paragraph = f'<p style="font-family:georgia; background-color:#EDF9F4; color:#4FAD99">' \
                    f'{HTML_PARAGRAPH_DICT["heading_paragraph"]}</p>'
        super().__init__(paragraph)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Refresh button --------------------------------------------------------
class RefreshButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Refresh Button',
            disabled=False,
            button_style='',
            tooltip='Refresh the rooms and surfaces (this will delete your current form)',
            icon='fa-refresh',
        )

        self.style.button_color = '#FF880063'


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Instructions button ---------------------------------------------------
class InstructionsButton(widgets.HTML):
    def __init__(self):
        res = f'''
            Your RemoteQuote Instructions
If RemoteQuote is left inactive in a browser for 15 minutes the server hosting it will go down. You will need to re-load
RemoteQuote and start again. Unfortunately your quote will be lost. If you need to stop part way throguh you could
estimate what you have so far and download the quote to save it. This information could then be re-entered.
RemoteQuote is designed to provide price estimations of Painting & Decorating work to be undertaken by a professional.
Estimates by a professional may vary and RemoteQuote should be used mainly as a guide and budgeting tool.
Tools have been incorporated to aid budgeting and these can be used to prioritise and order your quote.
Prices for the paint finishes in this interface are taken from www.duluxdecoratingcentre.co.uk and include VAT.
To use another paint, choose custom paint and input the required paint details price per unit, unit size, coverage.
For smaller surfaces, input a smaller unit size. If you already have the paint, or have bought it for another surface
input the price as 0. Paint needed is rounded up to whole unit sizes.
Descriptive words for the condition of a surface substrate are defined as such:

poor = Poor condition is where lots of preparation is required. Surfaces exhibit cracking, gaps not filled,
        previously poorly painted with drips, bits or flaking in the surface paint. Stains from oil or water may be 
        present. There may be joinings of the paper which is painted which requite sticking back. If any of the above
        or multiple faults then condition is poor
okay = Okay condition is where there are some faults with the surface and a small amount of preparation is 
        required, the surface may be marked and old but it sound, there may be a few fine cracks or small gaps to 
        fill
good = Good condition is where there is almost no preparation required, a light sand, limited fine cracks in
         corners but otherwise a good smooth surface which you are happy with

        '''
        # FILE
        filename = 'quote.txt'
        b64 = base64.b64encode(res.encode())
        payload = b64.decode()

        html_buttons = '''<html>
                <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
                <body>
                    <a download="{filename}" href="data:text/csv;base64,{payload}" download>
                        <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-info">
                            <i class="fa fa-download"></i> Download Info
                        </button>
                    </a>
                </body>
                </html>
                '''

        html_button = html_buttons.format(payload=payload, filename=filename)
        super().__init__(html_button)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- Final GUI -------------------------------------------------------------
class GuiInterface(widgets.VBox):
    def __init__(self):
        self.heading = GUIHeading()
        self.paragraph = GUIInstructionParagraph()
        self.refresh_button = RefreshButton()
        self.refresh_button.on_click(self.reset_form)
        self.form = RemoteQuoteForm(tab_structure.form_widgets_dict)
        self.instructions = InstructionsButton()
        super().__init__([self.heading, self.paragraph, widgets.HBox([self.refresh_button, self.instructions]),
                          self.form])

    def reset_form(self, change):
        tab_structure.form_widgets_dict = tab_structure.initialise_form_widgets()
        self.form = RemoteQuoteForm(tab_structure.form_widgets_dict)
        super().__init__([self.heading, self.paragraph,  widgets.HBox([self.refresh_button, self.instructions]),
                          self.form])
