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
# Dictionary of HTML paragraphs used in the GUI
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

# Dictionary of tooltips text for the blank info button widgets in the GUI
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

# Information button for the surface section of the GUI with no on click actions, just to provide info
class SurfaceInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Surface Info',
            disabled=False,
            button_style='',
            # selecting the tooltip text from the dictionary
            tooltip=TOOLTIPS_DICT['surface_tip'],
            # adding a light bulb icon onto the button visible to the user in the GUI
            icon='fa-lightbulb-o',
        )
        # setting the button colour to light blue
        self.style.button_color = 'lightblue'

# class inheriting from a widget float text box and being implemented to allow user input of surface area
class AreaInput(widgets.BoundedFloatText):
    def __init__(self):
        super().__init__(
            value=10,
            min=0,
            max=1000.0,
            step=1.0,
            # setting the description property to 'msq' to inform the user of the units I want the measurment in
            description='msq:',
            disabled=False,
        )

# class inheriting from ipywidget dropdown and allowing user to select the surface type surface subclass
class SurfaceSelector(widgets.Dropdown):
    def __init__(self):
        # setting the surface-type to surface class dict as a property to be able to access the appropriate class from
        # the user selection which will be the name of the class but in a string, to allow instantiation from GUI inputs
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT
        # setting the default surface class string to be used by the widget, selecting the 0th key from the dictionary
        self.default = list(SURFACE_TYPE_TO_CLASS_DICT.keys())[0]

        super().__init__(
            # using the class dictionary keys to fill in the options list for the widget
            options=list(self.surface_type_to_class_dict.keys()),
            # setting the default key as the default value for the widget
            value=self.default,
            description='Surface:',
            disabled=False,
        )
    # Function to use the surface class dictionary to convert user string selection into the class the string represents
    def get_surface_class_from_value(self):
        if self.value in self.surface_type_to_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = self.default
        surface = self.surface_type_to_class_dict[dict_key]
        return surface

# class inheriting from ipywidget dropdown to provide user with ability to select the design property of a surface type
class DesignSelector(widgets.Dropdown):
    def __init__(self):
        # using the same string to class dictionary structure as in previous class setting the dict as property
        self.surface_type_to_class_dict = SURFACE_TYPE_TO_CLASS_DICT

        super().__init__(
            # because the design property is not needed and is different for every surface type and is not needed for
            # the default surface type the options list and value property is an empty string by default
            options=[''],
            value='',
            description='Design:',
            disabled=False,
        )

    # function to toggle widget visibility depending on whether design options are needed for the current surface type
    def get_design_options(self, surface_type):
        # selecting the correct set of options
        design_options = self.surface_type_to_class_dict[surface_type](10).design_options
        # if design options are none for the surface type currently in the surface type widget then the widget is hidden
        if design_options is None:
            self.options = ['']
            self.layout.visibility = 'hidden'
            # if surface type has design options then they are set as property of the class and the widget is visible
        else:
            self.layout.visibility = 'visible'
            self.options = design_options

# only windows and cutting in doors need this widget class which inherits the ipywidget boundinttext
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
# function to toggle visibility of num panes widget based on surface type and design
    def display_num_panes(self, surface_type, design_type):
        num_panes = self.surface_type_to_class_dict[surface_type](10, design=design_type).num_panes
        if (num_panes is None) or (num_panes == 0):
            self.layout.visibility = 'hidden'
        else:
            self.layout.visibility = 'visible'
    # funtion to return number of panes of glass. If widget is hidden None is returned
    def get_num_panes_value(self):
        if self.layout.visibility == 'hidden':
            return None
        else:
            return self.value


# ----------------------------------------------- Surface form ---------------------------------------------------------

# Widget class inheriting from an ipywidgets vertical box to contain widgets for area, surface, design and num panes
class SurfaceForm(widgets.VBox):
    def __init__(self):
        # setting some HTML widgets to properties of surface from class to help format the surface section
        self.surface_heading = widgets.HTML(
            '<h2 style="font-family:georgia;background-color:#EDF9F4; color:#4FAD99">Surface Inputs</h2>')
        self.surface_paragraph = widgets.HTML(
            f'<p style="font-family:georgia; background-color:#EDF9F4; color:#4FAD99">'
            f'{HTML_PARAGRAPH_DICT["surface_paragraph_string"]}</p>')
        # setting an instantiation of the widgets to be contained
        # in the surface form as properties of this class for easy access
        self.surface_info = SurfaceInfoButton()
        self.area_input = AreaInput()
        self.surface_selector = SurfaceSelector()
        self.design_selector = DesignSelector()
        self.num_panes_selector = NumPanesSelector()

        # dictionary of widgets for easy accessing
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

        # using the observe method to watch the surface type selection widgets and call a method to change design
        # options and visibilty based on the change of the surface selector widget
        self.surface_selector.observe(self.toggle_design_options, 'value')
        # using the observe widget method to watch the designs for a change and call a function to toggle num panes
        self.design_selector.observe(self.toggle_num_panes_design, 'value')
        # using the observe method to watch the surface selector again but change number of panes selector visibility
        self.surface_selector.observe(self.toggle_num_panes_surface, 'value')

        # call the observe functions to set up design options and number of panes whose default settings
        # depend on surface type
        self.design_selector.get_design_options(self.surface_selector.value)
        self.num_panes_selector.display_num_panes(self.surface_selector.value, self.design_selector.value)
    # functions called for each of the observe methods used
    def toggle_num_panes_design(self, change):
        self.num_panes_selector.display_num_panes(self.surface_selector.value, change['new'])

    def toggle_num_panes_surface(self, change):
        self.num_panes_selector.display_num_panes(change['new'], self.design_selector.value)

    def toggle_design_options(self, change):
        self.design_selector.get_design_options(change['new'])


# ----------------------------------------------------------------------------------------------------------------------
#  ----------------------------------------------- Substrate widgets  --------------------------------------------------
# Widgets for substrate, condition, num coats and coverage adjustment

# info button widget with no on click functionality but providing extra text description for user in the GUI
class SubstrateInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Substrate Info',
            disabled=False,
            button_style='',
            # selecting the correct tooltip text from the tooltip dictionary for the tooltip property
            tooltip=TOOLTIPS_DICT['substrate_tip'],
            # setting a lightbulb font awesome icon to appear on the widget
            icon='fa-lightbulb-o',
        )
        # setting the button colour to light blue
        self.style.button_color = 'lightblue'

# widget class inheriting from ipywidgets toggle buttons to use as substrate selection for the user
class InputSubstrate(widgets.ToggleButtons):
    def __init__(self):
        # using the keys of the string to class dict for substrate to set the options list
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

# condition selection widget class inheriting from ipywidget dropdown class
class InputCondition(widgets.Dropdown):
    def __init__(self):
        super().__init__(
            # setting the options property using condition options dictionary in core file
            options=core.CONDITION_OPTIONS,
            value=core.CONDITION_OPTIONS[0],
            description='Condition:',
            disabled=False,
        )

# input number of coats class inheriting from bound int widget
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

# input coverage adjustment class inheriting from ipywidget bounded float text class
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

# input substrate details class inheriting from ipywidget accordion class and containing substrate details classes
class InputSubstrateDetails(widgets.Accordion):
    def __init__(self):
        # setting the classes/widgets to be contained as properties
        self.input_num_coats = InputNumCoats()
        self.input_coverage_adjustment = InputCoverageAdjustment()
        self.substrate_input_to_substrate_class_dict = SUBSTRATE_INPUT_TO_SUBSTRATE_CLASS_DICT
        # adding them to a dictionary
        self.widget_dict = {
            'input_num_coats': self.input_num_coats,
            'input_coverage_adjustment': self.input_coverage_adjustment,
        }
        # setting the widgets to be contained as children of the accordion widget using the dictionary of widgets
        super().__init__(
            children=[widgets.HBox(list(self.widget_dict.values()))],
            selected_index=None)
    # setting the title of the accordion
        self.set_title(0, "Substrate Details...")
    # function disabling the default values so they cannot be changed unless user chooses to input a custom substrate
    def toggle_substrate_details(self, substrate_type, condition):
        if substrate_type != 'Custom Substrate':
            disabled = True
        else:
            disabled = False
        # defaulting as disabled because as default there will be a substrate selected not custom substrate
        self.input_num_coats.disabled = disabled
        self.input_coverage_adjustment.disabled = disabled
        # using the dictionary to get the class from the string widget option
        substrate = self.substrate_input_to_substrate_class_dict[substrate_type](condition=condition)
        self.input_num_coats.value = substrate.num_coats
        self.input_coverage_adjustment.value = substrate.coverage_adjustment


# --------------------------------------------- Substrate form ---------------------------------------------------------
# Substrate form to combine and contain widgets for substrate type, condition, num coats and coverage adjustment
# used to instantiate Substrate classes in the GUI

# subsrate form class inheriting from ipywidget vertical box to organise and access the widgets contained
class SubstrateForm(widgets.VBox):
    def __init__(self):
        # HTML widget text for a heading and description of the substrate section of the GUI
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

        # dictionary of widgets contained in the substrate form class
        self.widget_list_dict = {
            'substrate_heading': self.substrate_heading,
            'substrate_paragraphself': self.substrate_paragraph,
            'substrate_info': self.substrate_info,
            'input_substrate': self.input_substrate,
            'input_condition': self.input_condition,
            'input_substrate_details': self.input_substrate_details,

            }
    # using observe method to toggle substrate details depending on the substrate and condition the user selects
        self.input_condition.observe(self.toggle_substrate_details_on_condition, 'value')
        self.input_substrate.observe(self.toggle_substrate_details_on_substrate, 'value')

        super().__init__(list(self.widget_list_dict.values()))

        # Run the observe functions to set up substrate details whose default settings depend on surface type
        self.input_substrate_details.toggle_substrate_details(self.input_substrate.value, self.input_condition.value)

# functions called by the observe method to change the values displayed in the substrate details accordion
    def toggle_substrate_details_on_condition(self, change):
        self.input_substrate_details.toggle_substrate_details(self.input_substrate.value, change['new'])

    def toggle_substrate_details_on_substrate(self, change):
        self.input_substrate_details.toggle_substrate_details(change['new'], self.input_condition.value)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------- Paint widgets --------------------------------------------------------

# Widgets for paint type, finish and paint details (price, unit, coverage)

# paint info button class inheriting from ipywidget button class to display info to user via tooltip
class PaintInfoButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Paint Info',
            disabled=False,
            button_style='',
            #selecting the correct tooltip from tooltip dictionary
            tooltip=TOOLTIPS_DICT['paint_tip'],
            icon='fa-lightbulb-o',
        )

        self.style.button_color = 'lightblue'

# paint type buttons class inheriting from ipywidget toggle button class
class PaintTypeButtons(widgets.ToggleButtons):
    def __init__(self):
        # selecting the string keys for the options list from the paint type to finish options dictionary
        options = list(PAINT_TYPE_TO_FINISH_OPTIONS_DICT.keys())
        super().__init__(
            options=options,
            description='Paint Type:',
            disabled=False,
            button_style='',
            tooltips=['Water Based Emulsion', 'Solvent Based Paint', 'Input custom Paint Parameters'],
            value=options[0],
        )

# finish choices class inheriting from ipywidgets dropdown menu class
class FinishChoices(widgets.Dropdown):
    def __init__(self):
        self.paint_finish_type_to_paint_class_dict = PAINT_FINISH_TYPE_TO_PAINT_CLASS_DICT
        self.paint_type_to_finish_options_dict = PAINT_TYPE_TO_FINISH_OPTIONS_DICT
# setting the defaults
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

    # function which is called from an observe method to change the available paint
    # finish options based on the paint type widget value
    def toggle_finish_options(self, paint_type):
        options = self.paint_type_to_finish_options_dict[paint_type]

        if options is None:
            self.layout.visibility = 'hidden'
        else:
            self.layout.visibility = 'visible'
            self.options = self.paint_type_to_finish_options_dict[paint_type]
            self.value = self.paint_type_to_finish_options_dict[paint_type][0]

# retrieving the class using the string option from dictionary of paint classes
    def get_paint_class_from_value(self):
        if self.value in self.paint_finish_type_to_paint_class_dict.keys():
            dict_key = self.value
        else:
            dict_key = self.default
        paint = self.paint_finish_type_to_paint_class_dict[dict_key]
        return paint

# paint details input class inheriting from ipywidgets accordion class
class PaintDetailsInputBox(widgets.Accordion):
    def __init__(self):
        # adding the widgets to be contained within the accordion as properties
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
    # method called from an observe to enable the paint input values if the user wants to input a custom paint
    def toggle_paint_inputs(self, paint_type):
        if paint_type == 'Custom Input':
            disabled = False
        else:
            disabled = True

        self.paint_price_input.disabled = disabled
        self.paint_unit_input.disabled = disabled
        self.paint_coverage_input.disabled = disabled
# method called from an observe to change the values displayed in the paint details widgets to display the
    # corresponding values for the currently selected paint
    def toggle_paint_values(self, paint_finish, paint_type):
        if paint_type != 'Custom Input':
            paint = self.paint_finish_type_to_paint_class_dict[paint_finish]()
            self.paint_price_input.value = paint.price
            self.paint_unit_input.value = paint.unit
            self.paint_coverage_input.value = paint.coverage

# price input class inheriting from ipywidget bound float text box
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

# unit input class inheriting from ipywidget bound float text box
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

# coverage input class inheriting from ipywidget bound float text box
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
# Paint form combining widgets for paint type, paint finish, paint inputs (price, unit, coverage)
# used to instantiate Paint classes within GUI

# paint form class inheriting from an ipywidget vertical box class
class PaintForm(widgets.VBox):
    def __init__(self):
        # html heading and paragraph for the paint section of the GUI
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
# observe methods being used to create visible changes between the paint widgets as paint type or finish is changed
        self.paint_type_buttons.observe(self.toggle_finish_visibility, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_inputs, 'value')
        self.paint_type_buttons.observe(self.toggle_paint_values_on_paint_type, 'value')
        self.paint_finish_dropdown.observe(self.toggle_paint_values_on_paint_finish, 'value')

        # Run the observe functions to set up paint input details and finish whose default settings
        # depend on paint type and paint finish
        self.paint_finish_dropdown.toggle_finish_options(self.paint_type_buttons.value)
        self.paint_inputs_box.toggle_paint_inputs(self.paint_type_buttons.value)
        self.paint_inputs_box.toggle_paint_values(self.paint_finish_dropdown.value, self.paint_type_buttons.value)
# funtions called by the observe methods above
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
# Combines form widgets for surface, substrate and paint inputs to put into the tabular structure
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

# estimate button class inheriting from ipywidget button to trigger the calculation
class EstimateButton(widgets.Button):
    def __init__(self):
        super().__init__(
            description='Estimate Job',
            disabled=False,
            button_style='',
            tooltip='Calculate',
            icon='check',
        )
# setting the estimate job - calculate button colour to palegreen
        self.style.button_color = 'palegreen'

# budget input class inheriting from ipywidget bounded int text box allowing users to input budget for optimisation
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

# optimise dropdown class inheriting from ipywidget dropdown widget class to select different optimisation priorities
class OptimiseDropdown(widgets.Dropdown):
    def __init__(self):
        self.optimisation_type_to_optimiser = OPTIMISATION_TYPE_TO_OPTIMISER
        super().__init__(
            options=list(self.optimisation_type_to_optimiser.keys()),
            value=list(self.optimisation_type_to_optimiser.keys())[0],
            description='Method:',
            disabled=True,
        )

# optimise button class inheriting from ipywidget button class to trigger the optimisation of the job created by the GUI
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

# remote quote form class inheriting from ipywidget vertical box
class RemoteQuoteForm(widgets.VBox):
    def __init__(self, form_widgets_dict):

# adding the tab structure of dictionaries as properies of remote quote form so everything can be accessed in this class
        self.form_widgets_dict = form_widgets_dict
        self.form_widgets_dict['dropdown_num_rooms'].observe(tab_structure.on_change_num_rooms)
        self.form_widgets_dict['dropdown_num_rooms'].observe(self.freeze_room_dropdown)
# adding all of the grouped widget classes as properties of this class
        self.calculate_box = CalculateBox()
        self.calculate_box.estimate_button.on_click(self.get_estimate)
        self.calculate_box.optimise_button.on_click(self.get_optimised_job)

        super().__init__([self.form_widgets_dict['dropdown_num_rooms'], self.form_widgets_dict['tab'],
                          self.calculate_box])
        self.job = core.Job([])

# function to freeze the room dropdown once a number of rooms is selected this is to stop accidental resetting of form
    def freeze_room_dropdown(self, change):
        self.form_widgets_dict['dropdown_num_rooms'].disabled = True

# function to create the downloadable breakdown text file using an f string and to create the button for the user
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

# function called when the optimise job button is clicked which looks at the value in the optimise dropdown to find
    # what type of optimisation the user wants then selects the correct function from the dictionary of optimisation
    # functions and passes in the budget input widget value along with the instantiation of the job class created by
    # the estimate button on click. This funtion also then sets up the download button and download document,
    # calling the summary funtions of the optimised job class from within an f string so that the results can be
    # downloaded in a text file.
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

# on click function of the estimate button to provide price output in the GUI, calls the funtion get job to instantiate
    # a job with the values from all of the widgets created in the GUI
    # This funtion needs to except the error that is caused by the user trying to estimate a job which has rooms where
    # the user has not selected the number of surfaces in the dropdown
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
# function to instantiate job with the values held in the widgets in the GUI
# a chain of functions is set in motion to get the rooms, get the painting surfaces, get the surfaces and get the paint
    def get_job(self):
        room_list = []
        num_rooms = self.form_widgets_dict['dropdown_num_rooms'].value
        for room_index in range(num_rooms):
            room_dict = self.form_widgets_dict['rooms']['widget_dict_list'][room_index]
            room = self.get_room(room_dict)
            room_list.append(room)
        job = core.Job(room_list)
        return job

# function to instantiate rooms from the values held in the GUI
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

# Function to instantiate painting surfaces using the values held in the widgets of the GUI
    def get_painting_surface(self, surface_dict):
        surface_name = surface_dict['surface_title'].value
        surface_form = surface_dict['surface_box'].surface_form
        substrate_form = surface_dict['surface_box'].substrate_form
        paint_form = surface_dict['surface_box'].paint_form

        surface = self.get_surface(surface_form, substrate_form)
        paint = self.get_paint(paint_form)
        surface.name = surface.name + surface_name
        return core.PaintingSurface(surface, paint)

# Function to instantiate surfaces using the values held in the widgets in the GUI
    def get_surface(self, surface_form, substrate_form):
        surface_area = surface_form.area_input.value
        surface = surface_form.surface_selector.get_surface_class_from_value()
        design = surface_form.design_selector.get_design_options(surface_form.surface_selector.value)
        num_panes = surface_form.num_panes_selector.get_num_panes_value()
        substrate = self.get_substrate(substrate_form)
        return surface(surface_area, design=design, num_panes=num_panes, substrate=substrate)

# Function to instantiate substrate using the values held in the substrate widgets and return a substrate class
    # to be used as a property of the corresponding surface class created on the same form
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

# method to get the values from the paint widgets and instantiate each paint needed
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
# refresh button class added to allow users to start the form again inherits from ipywidget button
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

#instructionsbutton class inherits from widgets.html, creates a button for the user and a text file they can download
class InstructionsButton(widgets.HTML):
    def __init__(self):
        res = f'''
            Your RemoteQuote Instructions

RemoteQuote is designed to provide price estimations of Painting & Decorating work to be undertaken by a professional.
Estimates by a professional may vary and RemoteQuote should be used mainly as a guide and budgeting tool. When tested
RemoteQuote has been consistently within 25% accuracy levels and usually within 10% accuracy.

If RemoteQuote is left inactive in a browser for 15 minutes, the server hosting it will go down. You will need to 
re-load RemoteQuote and start again. Unfortunately your quote will be lost. If you need to stop part way through you 
could estimate what you have so far and download the quote to save it. This information could then be re-entered.

Tools have been incorporated to aid budgeting and these can be used to prioritise or 'optimise' your quote.
There are three ways to optimise your quote if it exceeds a given budget. Using this feature will organise the work to 
be undertaken within your budget for the priority you choose. Priorities include, painting the maximum surface area,
painting the maximum surface area but only completing whole rooms and no partial rooms, and finally, optimising based7
on the condition of surfaces, so that surface in the poorest condition are prioritised. These optimised quotes can be 
downloaded. You can choose each option in the interface and download all three to compare.

Prices for the paint finishes in this interface are taken from www.duluxdecoratingcentre.co.uk and include VAT.
To use another paint, choose custom paint and input the required paint details price per unit, unit size, coverage.
For smaller surfaces, input a smaller unit size. 

If you already have the paint for your project, choose custom paint and input the price as 0.

Descriptive words for the condition of a surface substrate are defined as such:

'Poor' = Poor condition is where lots of preparation is required. Surfaces exhibit cracking, gaps not filled,
        previously poorly painted with drips, bits or flaking in the surface paint. Stains from oil or water may be 
        present. There may be joinings of the paper which is painted which requite sticking back. If any of the above
        or multiple faults then condition is poor
'Okay' = Okay condition is where there are some faults with the surface and a small amount of preparation is 
        required, the surface may be marked and previously not painted very well but it is sound.
        There may be some cracking and small areas of repair.
'Good' = Good condition is where there is almost no preparation required, a light sand, limited fine cracks in
         corners and scuffs but otherwise a good smooth surface which you are happy with.

To estimate spindles do not attempt to calculate a surface area. Count the number of spindles and put this figure into
RemoteQuote as the metres squared value. Count posts as 2.

For all other areas, attempt to measure an accurate square meterage. ALways enter surface area values in square metres.

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

    #funtion called when the refresh button is clicked which restarts the form.
    def reset_form(self, change):
        tab_structure.form_widgets_dict = tab_structure.initialise_form_widgets()
        self.form = RemoteQuoteForm(tab_structure.form_widgets_dict)
        super().__init__([self.heading, self.paragraph,  widgets.HBox([self.refresh_button, self.instructions]),
                          self.form])
