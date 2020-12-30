import ipywidgets as widgets
import forms


# ---------------------------------------------- Initialise form widgets dict ------------------------------------------

def initialise_form_widgets():
    form_widgets_dict = dict()
    form_widgets_dict['tab'] = widgets.Tab()
    form_widgets_dict['rooms'] = dict()

    num_rooms_max = 10
    form_widgets_dict['dropdown_num_rooms'] = widgets.Dropdown(
        options=range(0, num_rooms_max + 1),
        description='Num Rooms:',
        value=0,
    )
    return form_widgets_dict


form_widgets_dict = initialise_form_widgets()

# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- Callback function to create surface tabs--------------------------------------
def on_change_num_surfaces(num_surfaces_change):
    if num_surfaces_change['type'] == 'change' and num_surfaces_change['name'] == 'value':
        selected_room_index = form_widgets_dict['tab'].selected_index

        # creating form and widget list of dictionaries inside selected room index
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list'] = []
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['widget_dict_list'] = []
        for surface_index in range(1, num_surfaces_change['new'] + 1):
            # Create dictionary of widgets for the number of surfaces selected in the dropdown
            widgets_surface_dict = dict()
            widgets_surface_dict['surface_title'] = widgets.Text(
                value='Surface' + str(surface_index),
                description='Surface name',
            )

            # put surface box from the forms file into the surface widgets dictionary
            widgets_surface_dict['surface_box'] = forms.SurfaceBox()

            # Create the surface form widget box for surface box and surface name widget
            widgets_surface_form = widgets.VBox(list(widgets_surface_dict.values()))

            # add widget dictionary to widget dict list
            (form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['widget_dict_list']
             .append(widgets_surface_dict))
            # add surface widget box to form list
            (form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list']
             .append(widgets_surface_form))

        # assignment of forms created for each surface to surface tab widgets
        form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].children = \
            form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['surfaces']['form_list']

        # setting titles of surface tabs
        for i in range(len(form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].children)):
            form_widgets_dict['rooms']['widget_dict_list'][selected_room_index]['tab'].set_title(
                title='Surface' + str(i + 1),
                index=i
            )


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- Callback function to create room tabs ----------------------------------------
def on_change_num_rooms(num_rooms_change):
    # function responding to number of rooms dropdown to create rooms.
    if num_rooms_change['type'] == 'change' and num_rooms_change['name'] == 'value':

        # creation of form list and list of widget dictionaries within rooms dictionary
        form_widgets_dict['rooms'] = dict()
        form_widgets_dict['rooms']['form_list'] = []
        form_widgets_dict['rooms']['widget_dict_list'] = []
        for room_index in range(1, num_rooms_change['new'] + 1):
            # Creating room form dictionary, adding tab widget and dictionary of surfaces
            room_form_widgets_dict = dict()
            room_form_widgets_dict['tab'] = widgets.Tab()
            room_form_widgets_dict['surfaces'] = dict()

            # creation of title box for room
            room_form_widgets_dict['room_title'] = widgets.Text(
                value='Room' + str(room_index),
                description='Room name',
            )

            # creation of dropdown to select number of surfaces
            num_surfaces_max = 10
            room_form_widgets_dict['dropdown_num_surfaces'] = widgets.Dropdown(
                options=range(0, num_surfaces_max + 1),
                description='# Surfaces:',
                value=0,
            )

            # calling function on change of surfaces dropdown
            room_form_widgets_dict['dropdown_num_surfaces'].observe(on_change_num_surfaces)

            # making a vertical box widget to display room form widgets
            room_form_widget_box = widgets.VBox([
                room_form_widgets_dict['room_title'],
                room_form_widgets_dict['dropdown_num_surfaces'],
                room_form_widgets_dict['tab']
            ])

            # adding room form widgets dicitonary to list of dictionaries within rooms for access by name
            form_widgets_dict['rooms']['widget_dict_list'].append(room_form_widgets_dict)
            # adding the same instances of widgets which have been places in a Vbox into the form list for display
            form_widgets_dict['rooms']['form_list'].append(room_form_widget_box)

        # assignment of forms created for each room to room tab widgets
        form_widgets_dict['tab'].children = form_widgets_dict['rooms']['form_list']

        # Setting titles for the room tabs
        for i in range(len(form_widgets_dict['tab'].children)):
            form_widgets_dict['tab'].set_title(title='Room' + str(i + 1), index=i)
