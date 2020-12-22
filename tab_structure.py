import ipywidgets as widgets
import forms

form_widgets_dict = dict()
form_widgets_dict['tab'] = widgets.Tab()
form_widgets_dict['rooms'] = dict()

num_rooms_max = 5
form_widgets_dict['dropdown_num_rooms'] = widgets.Dropdown(options=range(1, num_rooms_max + 1),
                                                                 description='Num Rooms:')

def get_current_surface_widget_box():
    selected_room_index = form_widgets_dict['tab'].selected_index
    selected_surface_index = form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].selected_index
    selected_surface_widget_box = \
    form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['widget_dict_list'][
        selected_surface_index]['surface_box']
    return selected_surface_widget_box

############################################
def on_click_paint_type_buttons(change):
    if change['type'] == 'change' and change['name'] == 'value':
        selected_surface_widget_box = get_current_surface_widget_box()
        paint_type_button_value = selected_surface_widget_box.paint_type_buttons.value
        selected_surface_widget_box.paint_finish_dropdown.get_finish_options(paint_type_button_value)
#############################################



def on_change_num_surfaces(num_surfaces_change):
    if num_surfaces_change['type'] == 'change' and num_surfaces_change['name'] == 'value':
        selected_room_index = form_widgets_dict['tab'].selected_index
        selected_room = selected_room_index + 1

        # creating form and widget list of dictionaries for each of the surfaces inside selected room index
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list'] = []
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['widget_dict_list'] = []
        for surface_index in range(1, num_surfaces_change['new'] + 1):
            # Create dictionary of widgets which will be contained in the surface form
            widgets_surface_dict = dict()
            widgets_surface_dict['surface_box'] = forms.SurfaceForm()
            #widgets_surface_dict['slider'] = forms.AreaInput()
            #widgets_surface_dict['text'] = forms.SurfaceSelector()
            #widgets_surface_dict['paint_type_buttons'] = forms.PaintTypeButtons()
            #widgets_surface_dict['finish_dropdown'] = forms.FinishChoices()

            widgets_surface_dict['surface_box'].paint_type_buttons.observe(on_click_paint_type_buttons)

            # Create the surface form widget
            widgets_surface_form = widgets.Box(list(widgets_surface_dict.values()))

            # Put the surface widgets and surface form inside of the global level dictionary for the whole form
            # to be able to reference them in callbacks
            (form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['widget_dict_list']
             .append(widgets_surface_dict))
            (form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list']
             .append(widgets_surface_form))

        # assignment of forms created for each surface to surface tab widgets
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].children = \
            form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list']

        # setting titles of surface tabs
        for i in range(len(form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].children)):
            form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].set_title(title=
                                                                                                 'Surface' + str(i + 1),
                                                                                                 index=i)
            ############################################################################


def on_change_num_rooms(num_rooms_change):
    # fuction responding to number of rooms dropdown to create rooms.
    if num_rooms_change['type'] == 'change' and num_rooms_change['name'] == 'value':

        # creation of form and list of widget dictionaries for each room
        form_widgets_dict['rooms'] = dict()
        form_widgets_dict['rooms']['form_list'] = []
        form_widgets_dict['rooms']['widget_dict_list'] = []
        for room_index in range(1, num_rooms_change['new'] + 1):
            # creation of surface form dictionary, creation of tab widgets for surfaces,
            # creation of dictionary for widgets inside surfaces tab
            room_widgets_surface_form_dict = dict()
            room_widgets_surface_form_dict['tab'] = widgets.Tab()
            room_widgets_surface_form_dict['surfaces'] = dict()

            # creation of dropdown to select number of surfaces
            num_surfaces_max = 5
            room_widgets_surface_form_dict['dropdown_num_surfaces'] = widgets.Dropdown(
                options=range(1, num_surfaces_max + 1),
                description='Num Surfaces:')
            # calling function on change of dropdown
            room_widgets_surface_form_dict['dropdown_num_surfaces'].observe(on_change_num_surfaces)

            # making the widget for the form inside room tab
            widgets_room_form = widgets.Box([room_widgets_surface_form_dict['dropdown_num_surfaces'],
                                             room_widgets_surface_form_dict['tab']])

            # Put the room widgets and room form inside of the global level dictionary for the whole form
            # to be able to reference them in callbacks
            form_widgets_dict['rooms']['widget_dict_list'].append(room_widgets_surface_form_dict)
            form_widgets_dict['rooms']['form_list'].append(widgets_room_form)

        # assignment of forms created for each room to room tab widgets
        form_widgets_dict['tab'].children = form_widgets_dict['rooms']['form_list']

        # Setting titles for the room tabs
        for i in range(len(form_widgets_dict['tab'].children)):
            form_widgets_dict['tab'].set_title(title='Room' + str(i + 1), index=i)

###############################################################################################################




