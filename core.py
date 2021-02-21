from numbers import Number
import math
import knapsack

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Global variables ----------------------------------------------------------

# List of conditions available for the Substrate class condition property.
CONDITION_OPTIONS = ['good', 'okay', 'poor']

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Surface class -------------------------------------------------------------

#  Creating a class for the surface object in RemoteQuote which will be the parent class to
#  different types of surface object. The Surface class has fundamental properties such as surface area and substrate.
class Surface:
    def __init__(
            self,
            area=None,
            length=None,
            width=None,
            labour_adjustment=None,
            substrate=None,
            design=None,
            design_options=None,
            description=None,
            name=None,
            num_panes=None,
            room_name=None

    ):
        # Validation for inputs when instantiating a surface object
        if area is None:
            assert length is not None and width is not None, 'Input either "area" or "length" and "width".'
            assert isinstance(length, Number) and length > 0, 'Input "length" needs to be numeric and > 0.'
            assert isinstance(width, Number) and width > 0, 'Input "width" needs to be numeric and > 0.'
            area = length * width
        else:
            assert length is None and width is None, 'Input either "area" or "length" and "width".'
            assert isinstance(area, Number) and area > 0, 'Input "area" needs to be numeric and > 0.'

        if labour_adjustment is None:
            labour_adjustment = 1
        else:
            assert isinstance(labour_adjustment, Number) and labour_adjustment > 0, \
                'Input "labour_adjustment" needs to be numeric and > 0.'

        # Setting a default substrate when no substrate argument is passed in
        if substrate is None:
            substrate = PrePaintedEmulsion()

        self.area = area
        self.length = length
        self.width = width
        self.labour_adjustment = labour_adjustment
        self.substrate = substrate
        self.design = design
        self.design_options = design_options
        self.description = description
        self.name = name
        self.num_panes = num_panes
        self.room_name = room_name


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Surface subclasses --------------------------------------------------------

#Different surface types containing default labour adjustment settings and design options specific to each surface type

class Wall(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the name and description properties for the Wall class.
        description = 'An interior wall'
        name = 'Wall'
        # Default labour adjustment being set. Used when calculating the labour cost for this surface type.
        if labour_adjustment is None:
            labour_adjustment = 0.9
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Ceiling(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the description and name properties  for the Ceiling class
        description = 'An interior ceiling'
        name = 'Ceiling'
        # Setting the default labour adjustment
        if labour_adjustment is None:
            labour_adjustment = 0.95

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Door(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, num_panes=None, **kwargs):
        # Setting the name and description properties for the Door class
        description = 'One side of an interior door'
        name = 'Door'
        # List containing design options for Door.
        design_options = ['Panelled', 'Flat door', 'Cutting in']
        # ensuring that a cutting in door must have at least one pane of glass, else it is not a cutting in door.
        if design == 'Cutting in' and num_panes is None:
            num_panes = 1
        elif num_panes is None:
            num_panes = 0
        # validation of design argument, if it is passed in it needs to be in the programmed options.
        assert design in (design_options + [None]), 'input needs to be "Panelled", "Flat door", "Cutting in" or None'
        assert isinstance(num_panes, int) and num_panes >= 0, 'Input "num_panes" needs to be a non-negative integer'
        # setting the default design to flat door when there is no panes of glass and no design argument provided.
        if num_panes > 0 and design is None:
            design = 'Cutting in'
        if design is None:
            design = 'Flat door'

        assert (num_panes > 0 and design == 'Cutting in') or \
               (num_panes == 0 and design in ['Panelled', 'Flat door', None]), 'Only "Cutting in" doors have panes > 0'
        # algorithm to assign the labour adjustment for cutting in doors which vary
        # in price depending on the number of panes.
        if labour_adjustment is None:
            labour_adjustment = 1.6
            if design == 'Panelled':
                labour_adjustment = 1.65
            elif design == 'Cutting in':
                if num_panes < 7:
                    labour_adjustment = 2.7
                else:
                    labour_adjustment = min(5/12 * num_panes, 5.5)

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name, num_panes=num_panes)


class Doorframe(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):
        # Setting the name and description properties for the Doorframe class.
        description = 'Room side of door frame'
        name = 'Door Frame'
        # List containing design options for Doorframe
        design_options = ['Standard', 'Victorian', 'Elaborate']
        # Setting the default design and validating the design argument to make sure it is in the coded list.
        if design is None:
            design = design_options[0]
        else:
            assert design in design_options,\
                'input needs to be "Standard", "Victorian", "Elaborate" or None'
        # Setting the  default labour adjustment based on design.
        if labour_adjustment is None:
            labour_adjustment = 3.2
            if design == 'Victorian':
                labour_adjustment = 3.6
            elif design == 'Elaborate':
                labour_adjustment = 4.2

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name)


class Skirtingboard(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the name and description properties for the skirting board class
        description = 'Skirting board along the bottom of a wall'
        name = 'Skirting board'
        # Setting the default labour adjustment value for the Skirting Board class.
        if labour_adjustment is None:
            labour_adjustment = 2.5
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Window(Surface):
    def __init__(self, *args, labour_adjustment=None, num_panes=1, **kwargs):
        # Setting the name and description for the Window class.
        description = 'Interior side of a window, frame included'
        name = 'Window'
        # Validating the number of panes argument which must be greater than zero.
        assert isinstance(num_panes, int) and num_panes >= 1, '"num_panes" needs to be an integer and >= 1'
        # Setting the default labour adjustment value for Window which changes based on the number of panes of glass
        if labour_adjustment is None:
            labour_adjustment = (1.325 * num_panes)

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description,
                         name=name, num_panes=num_panes)


class Windowsill(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the name and description for the Windowsill class.
        description = 'The interior horizontal sill beneath a window'
        name = 'Windowsill'
        # Setting the default labour adjustment value for the windowsill class.
        if labour_adjustment is None:
            labour_adjustment = 8.5
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Spindle(Surface):
    def __init__(self, *args, labour_adjustment=None, design=None, **kwargs):
        # Setting the name and description properties for the Spindle class.
        description = 'Vertical bars underneath a handrail'
        name = 'Spindle'
        # List containing design options for Spindle
        design_options = ['Square', 'Shaped', 'Elaborate']
        # Setting default design.
        if design is None:
            design = design_options[0]
        else:
            assert design in design_options, \
                'input needs to be "Square", "Shaped", "Elaborate" or None'
        # Setting the labour adjustment depending on the design property.
        if labour_adjustment is None:
            labour_adjustment = 0.25
            if design == 'Shaped':
                labour_adjustment = 0.5
            elif design == 'Elaborate':
                labour_adjustment = 0.75

        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, design=design,
                         design_options=design_options, description=description, name=name)


class ElaborateCornice(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the name and description properties for the Elaborate Cornice class.
        description = 'Large ornate plaster cornice, ceiling roses or corbels'
        name = 'Decorative plaster'
        # Setting the default labour adjustment.
        if labour_adjustment is None:
            labour_adjustment = 2
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


class Radiator(Surface):
    def __init__(self, *args, labour_adjustment=None, **kwargs):
        # Setting the name and description properties for the Radiator class.
        description = 'Enamelled modern radiator'
        name = 'Radiator'
        # Setting the default labour adjustment value.
        if labour_adjustment is None:
            labour_adjustment = 3.7
        super().__init__(*args, **kwargs, labour_adjustment=labour_adjustment, description=description, name=name)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Substrate class -----------------------------------------------------------

# Creating the Substrate class which represents the substrate material of a surface object.
class Substrate:
    # Adding Substrate properties, number of coats of paint, the condition the substate is in and the coverage
    # adjustment factor which represents the effect that a substrate material has on the coverage ability of paint
    # and a boolean to hold whether the substrate has been primed or not.
    def __init__(
            self,
            num_coats=1,
            condition=None,
            coverage_adjustment=1,
            condition_assumption=None,
            primed=False

    ):
        # Adding the conditions options list as a property of the Substrate class.
        self.condition_options = CONDITION_OPTIONS
        # Validation of condition argument
        assert condition in self.condition_options + [None], \
            'Input "condition" needs to be "poor", "okay", "good" or None'
        # Setting default condition as good
        if condition is None:
            condition = 'good'
        # Validating the number of coats argument, it must be greater than 0 to paint a surface.
        assert isinstance(num_coats, int) and num_coats > 0, 'Input "num_coats" needs to be a non-zero integer'
        # Validating the coverage adjustment is a non zero number
        assert (isinstance(coverage_adjustment, Number) and coverage_adjustment > 0.0) \
               or (coverage_adjustment is None), 'Input needs to be numeric and > 0, or None'
        # Setting default coverage adjustment to 1. In this case it will not affect the paint's coverage performance.
        if coverage_adjustment is None:
            coverage_adjustment = 1
        
        if condition_assumption is None:
            condition_assumption = ConditionAssumptions()

        self.num_coats = num_coats
        self.condition = condition
        self.preparation_factor = self.get_preparation_factor()
        self.coverage_adjustment = coverage_adjustment
        self.condition_assumption = condition_assumption
        self.primed = False

    # Function to set the preparation factor based on the condition
    def get_preparation_factor(self):
        if self.condition == 'poor':
            preparation_factor = 1.05
        elif self.condition == 'okay':
            preparation_factor = 1.025
        else:
            preparation_factor = 1

        return preparation_factor


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ Substrate subclasses-------------------------------------------------------

# These are substrate subclasses which represent the various materials a surface can be

class Plaster(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        # setting the number of coats for a plaster substrate
        if num_coats is None:
            num_coats = 2
        # setting the coverage adjustment for a plaster substrate
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)


class PrePaintedEmulsion(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        # Setting the number of coats for a substrate which has been previously painted with emulsion paint, the
        # number of coats is dependant on condition
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        # Setting coverage adjustment to 1 this will not affect coverage, paint should achieve optimum coverage on
        # a surface already painted with good quality paint
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition,
                         coverage_adjustment=coverage_adjustment)


class PrePaintedWood(Substrate):
    def __init__(self, *args, num_coats=None, condition=None, coverage_adjustment=None, **kwargs):
        # setting the number of coats for pre painted woodwork, the number of coats needed is dependant upon condition
        if num_coats is None and condition == 'poor':
            num_coats = 2
        elif num_coats is None:
            num_coats = 1
        # setting coverage adjustment to 1, this will not affect coverage as max coverage performance should be
        # achieved on pre-painted surfaces
        if coverage_adjustment is None:
            coverage_adjustment = 1
        super().__init__(*args, **kwargs, num_coats=num_coats, condition=condition,
                         coverage_adjustment=coverage_adjustment)



class NewLiningPaper(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, **kwargs):
        # Setting the number of coats for new and not painted lining paper, this should always be 2 coats
        if num_coats is None:
            num_coats = 2
        # Lining paper is porous so the coverage adjustment is set to decrease coverage performance
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)




class Mdf(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, primed=False, **kwargs):
        # Setting the number of coats needed for mdf depends on whether the MDF has been primed or is pre-primed
        if num_coats is None:
            num_coats = 3
        if primed is True:
            num_coats = 2
        # MDF is very porous even after priming so the coverage adjustment is set to decrease expected coverage
        if coverage_adjustment is None:
            coverage_adjustment = 1.2

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment, primed=primed)




class NewWood(Substrate):
    def __init__(self, *args, num_coats=None, coverage_adjustment=None, primed=False, **kwargs):
        # Setting the number of coats needed for new wood, this is dependant on it being primed or not.
        if num_coats is None and primed is False:
            num_coats = 3
        if num_coats is None and primed is True:
            num_coats = 2
        # Setting the coverage adjustment for new wood, it is not as porous as MDF.
        if coverage_adjustment is None:
            coverage_adjustment = 1.05

        super().__init__(*args, **kwargs, num_coats=num_coats, coverage_adjustment=coverage_adjustment)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Paint ---------------------------------------------------------

# Paint objects coded here with the paint parent class first.

class Paint:
    def __init__(self, price, unit, coverage,):
        # Validating the price unit and coverage arguments for the paint class.
        assert isinstance(price, Number) and price >= 0, 'Input "price" needs to be numeric and greater than or equal' \
                                                         ' to zero.'
        assert isinstance(unit, Number) and unit > 0, 'Input "unit" needs to be numeric and greater than 0.'
        assert isinstance(coverage, Number) and coverage > 0, 'Input "coverage" needs to be numeric and greater than 0.'
        self.price = price
        self.unit = unit
        self.coverage = coverage


class EmulsionPaint(Paint):
    # Emulsion paint sub-class
    def __init__(self, price=None, unit=None, coverage=None):
        super().__init__(price, unit, coverage)

class MattEmulsionPaint(EmulsionPaint):
    # Dulux default paint with set price unit and coverage values taken from Dulux website
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 37.87
        if unit is None:
            unit = 5
        if coverage is None:
            coverage = 17

        super().__init__(price, unit, coverage)


class SilkEmulsionPaint(EmulsionPaint):
    # Dulux default paint for use in the GUI, Silk finish, with set price unit and coverage taken from Dulux's website
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 46.27
        if unit is None:
            unit = 5
        if coverage is None:
            coverage = 17

        super().__init__(price, unit, coverage)

class DiamondMattEmulsion(EmulsionPaint):
    # Dulux default paint for the GUI, Diamond matt emulsion, with price unit and coverage values set from website
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 50.03
        if unit is None:
            unit = 5
        if coverage is None:
            coverage = 17
        super().__init__(price, unit, coverage)

class OilPaint(Paint):
    # oil/solvent based paint subclass of paint
    def __init__(self, price=None, unit=None, coverage=None):
        super().__init__(price, unit, coverage)

class OilEggshell(OilPaint):
    # Eggshell finish oil paint as a subclass of oilpaint with price, unit, coverage values set from Dulux website
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 32.07
        if unit is None:
            unit = 2.5
        if coverage is None:
            coverage = 17
        super().__init__(price, unit, coverage)


class OilGloss(OilPaint):
    # Gloss finish class as a child class of oil paint with values price, unit, coverage set to the values on Dulux site
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 19.00
        if unit is None:
            unit = 2.5
        if coverage is None:
            coverage = 17
        super().__init__(price, unit, coverage)

class OilSatin(OilPaint):
    # Satin finish oil paint subclass, with price unit and coverage values defaulted to the values from Dulux website
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 37.20
        if unit is None:
            unit = 2.5
        if coverage is None:
            coverage = 17
        super().__init__(price, unit, coverage)



class Primer(Paint):
    # A primer subclass of paint with the values defaulted to the values of a Dulux undercoat/wood primer.
    def __init__(self, price=None, unit=None, coverage=None):
        if price is None:
            price = 31.15
        if unit is None:
            unit = 2.5
        if coverage is None:
            coverage = 25
        super().__init__(price, unit, coverage)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------- Painting Surface -----------------------------------------------------
class PaintingSurface:
    # Painting surface is a new class which takes a paint and a surface as arguments to calculate the labour and
    # material cost of painting the surface argument with the paint argument
    def __init__(self, surface, paint, labour_price_msq=None):
        # Setting the default labour price per square metre which will be adjusted by the labour adjustment property
        # contained in the surface class passed in as an argument
        if labour_price_msq is None:
            labour_price_msq = 4
        self.surface = surface
        self.paint = paint
        self.labour_price_msq = labour_price_msq
        # Validating the arguments are instantiations of the correct classes
        assert isinstance(surface, Surface), 'Input needs to be a Surface object'
        assert isinstance(paint, Paint), 'Input needs to be a Paint object'
        self.total_paint_coverage = self.get_total_paint_coverage()

    # Function to calculate the coverage of the whole tin of paint because coverage value is given per litre on tins
    def get_total_paint_coverage(self):
        total_paint_coverage = int(self.paint.coverage * self.paint.unit)
        return total_paint_coverage

    # Function to calculate the amount of paint needed, takes into account the number of coats property here as well as
    # the coverage value, coverage adjustment value and the area to be covered
    def get_units_of_paint(self):
        units_of_paint = (
            (self.surface.area / (self.total_paint_coverage / self.surface.substrate.coverage_adjustment))
            * self.surface.substrate.num_coats)
        return units_of_paint

    # Funtion to calculate the price of the amount of paint needed to paint the surface
    def get_paint_price(self):
        paint_price = self.get_units_of_paint() * self.paint.price
        return paint_price

    # Function which calculates the labour price for coating the surface, considers the area, labour price psqm, the
    # labour adjustment value, the number of coats needed and the preparation factor
    def get_labour_price(self):
        labour_price = self.surface.area * self.labour_price_msq * self.surface.labour_adjustment * \
            self.surface.substrate.num_coats * self.surface.substrate.preparation_factor
        return labour_price

    # Get total price function to call the previous functions add the results and return a total
    def get_total_price(self):
        total_price = self.get_labour_price() + self.get_paint_price()
        return total_price

    # A breakdown function which creates a dictionary of the results of each calculation and returns each price,
    # the calculation results are rounded to 2 decimal points avoiding long floats as breakdown dictionary could be
    # returned to the user in the GUI or downloadable quote
    def get_breakdown(self):
        breakdown = dict(
            room_name=self.surface.room_name,
            surface_name=self.surface.name,
            total_price=round(self.get_total_price(), 2),
            labour_price=round(self.get_labour_price(), 2),
            paint_price=round(self.get_paint_price(), 2),
            units_of_paint=round(self.get_units_of_paint(), 2),
            surface_area=self.surface.area,
        )
        return breakdown


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Room --------------------------------------------------------------

# Room class which acts as a room does in a real quote and contains a list of surfaces and their costs to be totalled

class Room:
    def __init__(self, painting_surfaces, name=None):
        # asserting that the list passed in is a list of painting surface objects
        for painting_surface in painting_surfaces:
            assert isinstance(painting_surface, PaintingSurface), 'Input needs to be a list of painting surface objects'
        # setting a name in the case none is passed in, the ability to name the room is provided to user in GUI
        if name is None:
            name = 'my room'

        self.painting_surfaces = painting_surfaces
        self.name = name

        # adding the room name to the surface name so that surfaces can be identified by the room they belong to
        for painting_surface in self.painting_surfaces:
            painting_surface.surface.room_name = self.name

    # function to total the paint price from each surface in the room
    def get_paint_price(self):
        room_paint_price = 0
        for painting_surface in self.painting_surfaces:
            room_paint_price += painting_surface.get_paint_price()
        return room_paint_price

    # Method to total the labour price from each surface in the surface list passed in as an argument
    def get_labour_price(self):
        room_labour_price = 0
        for painting_surface in self.painting_surfaces:
            room_labour_price += painting_surface.get_labour_price()
        return room_labour_price

    # Method to calculate total price which calls the total price function from each painting surface and totals
    def get_total_price(self):
        room_total_price = 0
        for painting_surface in self.painting_surfaces:
            room_total_price += painting_surface.get_total_price()
        return room_total_price

    # Method to calculate the total surface area to paint in a room, this is used for the value list in the optimisation
    def get_total_surface_area(self):
        room_surface_area = 0
        for painting_surface in self.painting_surfaces:
            room_surface_area += painting_surface.surface.area
        return room_surface_area

    # Method to calculate the total surface area of surfaces in poor condition within a room to optimise by condition.
    def get_total_surface_area_by_condition(self, condition_list):
        total_surface_area_by_condition = 0
        for painting_surface in self.painting_surfaces:
            if painting_surface.surface.substrate.condition in condition_list:
                total_surface_area_by_condition += painting_surface.surface.area
        return total_surface_area_by_condition

    # breakdown function which uses the breakdown function of each painting surface and adds all the dictionaries from
    # painting surface breakdowns into a breakdown list of dictionaries
    def get_breakdown(self):
        breakdown_list = []

        for painting_surface in self.painting_surfaces:
            breakdown_dict = painting_surface.get_breakdown()
            breakdown_list.append(breakdown_dict)

        return breakdown_list


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Job ---------------------------------------------------------------
class Job:
    def __init__(self, rooms, name=None):
        # Using an assert statement to validate the room argument is a list of room objects
        for room in rooms:
            assert isinstance(room, Room), 'Input needs to be a list of room objects'
        self.rooms = rooms
        # assigning job name
        if name is None:
            name = 'my job'
        self.name = name

    # Method to total the paint price of each painting surface in each room for the whole job
    def get_paint_price(self):
        total_job_paint_price = 0
        for room in self.rooms:
            total_job_paint_price += room.get_paint_price()
        return total_job_paint_price

    # Method to total the labour price of each painting surface in each room for the whole job
    def get_labour_price(self):
        total_job_labour_price = 0
        for room in self.rooms:
            total_job_labour_price += room.get_labour_price()
        return total_job_labour_price

    # Method to total the total price of each painting surface in each room for the whole job
    def get_total_price(self):
        total_job_price = 0
        for room in self.rooms:
            total_job_price += room.get_total_price()
        return total_job_price

    # Breakdown method which creates a list of the room breakdown lists which create the painting surface dictionaries
    def get_breakdown(self):
        breakdown_list = []
        for room in self.rooms:
            breakdown_list.append(room.get_breakdown())
        return breakdown_list

    # Method to get the painting surface lists for the optimisation from each room which calls the static method below
    def get_painting_surface_list(self):
        rooms = self.rooms
        return self.get_painting_surface_list_from_room_list(rooms)
    # Method to add every surface in the job into one list
    @staticmethod
    def get_painting_surface_list_from_room_list(rooms):
        painting_surface_list = []
        for room in rooms:
            for painting_surface in room.painting_surfaces:
                painting_surface_list.append(painting_surface)

        # sorting list in preparation for knapsack algorithm which needs ascending order of cost
        painting_surface_list.sort(key=lambda x: x.get_total_price())

        return painting_surface_list
    # Method to create area cost lists for optimisation by taking the painting surface list and extracting from each
    # surface the area for one list and the cost for the other list so that the indexing of each list matches
    @staticmethod
    def get_area_cost_lists(painting_surface_list):

        surface_area_list = []
        painting_price_list = []

        # creating value and cost lists for knapsack
        for painting_surface in painting_surface_list:
            surface_area_list.append(painting_surface.surface.area)
            painting_price_list.append(math.ceil(painting_surface.get_total_price()))

        return surface_area_list, painting_price_list

    # Method to optimise the job, takes in a budget as an argument and all the other information is gathered from
    # within the job class using the job class methods.
    def get_optimised_job(self, budget):
        surface_list = self.get_painting_surface_list()
        values, costs = self.get_area_cost_lists(surface_list)
        # next line calls the optimisation algorithm from the knapsack python file and passes in the information
        optimal_index_list = knapsack.optimal_knapsack(budget, values, costs)
        optimal_surface_list = [surface_list[i] for i in optimal_index_list]
        # next line returns an instantiation of the optimised job class to contain results of optimisation
        return OptimisedJob(optimal_surface_list, surface_list, budget)

    # Method preparing to optimise by whole rooms instead of individual surfaces,
    # adds rooms to a list and orders by total price
    def get_sorted_room_list(self):
        sorted_room_list = []
        for room in self.rooms:
            sorted_room_list.append(room)
            sorted_room_list.sort(key=lambda x: x.get_total_price())
        return sorted_room_list

    # Method which takes the sorted room list in as an argument and extracts the total surface area of each room and
    # returns a list of total surface areas for the optimisation
    def get_room_surface_area_list(self, sorted_room_list):
        room_surface_area_list = []
        for room in sorted_room_list:
            room_surface_area_list.append(room.get_total_surface_area())
        return room_surface_area_list

    # Method to create a price list from the sorted room list
    def get_room_price_list(self, sorted_room_list):
        room_price_list = []
        for room in sorted_room_list:
            room_price_list.append(math.ceil(room.get_total_price()))
        return room_price_list

    # Method to optimise a job by whole rooms, takes in a budget, returns an instantiation of an optimised job class,
    # uses the above functions to prepare the area cost lists
    def get_optimised_rooms_job(self, budget):
        sorted_room_list = self.get_sorted_room_list()
        room_surface_area_list = self.get_room_surface_area_list(sorted_room_list)
        room_price_list = self.get_room_price_list(sorted_room_list)
        # next line calls the optimisation algorithm from the knapsack python file and passes in the information
        optimal_room_index_list = knapsack.optimal_knapsack(budget, room_surface_area_list, room_price_list)
        optimal_room_list = [sorted_room_list[i] for i in optimal_room_index_list]
        budgeted_painting_surface_list = self.get_painting_surface_list_from_room_list(optimal_room_list)
        original_painting_surface_list = self.get_painting_surface_list_from_room_list(sorted_room_list)
        # next line returns an instantiation of the optimised job class to contain results of optimisation
        # passes in the original list of painting surfaces and the optimised list
        return OptimisedJob(budgeted_painting_surface_list, original_painting_surface_list, budget)

    # Method to prepare the lists for the optimisation to optimise by area of poor condition surface in a room
    def get_room_surface_area_by_condition_list(self, sorted_room_list, condition_list):
        room_surface_area_by_condition_list = []
        for room in sorted_room_list:
            room_surface_area_by_condition_list.append(room.get_total_surface_area_by_condition(condition_list))
        return room_surface_area_by_condition_list

    # Method to optimise by condition, returns an optimised job object, takes in a budget to optimise to
    def get_optimised_condition_job(self, budget):
        sorted_room_list = self.get_sorted_room_list()
        condition_list = ['poor']
        room_surface_area_by_condition_list = self.get_room_surface_area_by_condition_list(sorted_room_list,
                                                                                           condition_list)
        room_price_list = self.get_room_price_list(sorted_room_list)
        # calling the optimisation algorithm funtion from within the knapsack python file
        optimal_room_index_list = knapsack.optimal_knapsack(budget, room_surface_area_by_condition_list,
                                                            room_price_list)
        optimal_room_list = [sorted_room_list[i] for i in optimal_room_index_list]
        budgeted_painting_surface_list = self.get_painting_surface_list_from_room_list(optimal_room_list)
        original_painting_surface_list = self.get_painting_surface_list_from_room_list(sorted_room_list)
        # returning an optimised job class object
        return OptimisedJob(budgeted_painting_surface_list, original_painting_surface_list, budget)


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Optimised Job -----------------------------------------------------

# This is the optimised job class which is instantiated when a job is optimised using the algorithm in the knapsack
# python file and contains the information from job which was to be optimised as well as the optimised information and
# returns summary dictionaries to view and compare results

class OptimisedJob:
    # takes in the un-optimised list, the optimised list and the budget that the job was optimised to as arguments
    def __init__(self, budgeted_painting_surface_list, original_painting_surface_list, budget):
# Sorting the budgeted painting surface list by room name property so for summary info surfaces are grouped in rooms
        self.budgeted_painting_surface_list = sorted(budgeted_painting_surface_list, key=lambda x: x.surface.room_name)
        self.original_painting_surface_list = original_painting_surface_list
        self.budget = budget

    # method to provide a breakdown of the budgeted painting surface list using the get breakdown method from each
    # painting surface class and adding the breakdowns to a list
    def get_breakdown(self):
        breakdown_list = []
        for painting_surface in self.budgeted_painting_surface_list:
            breakdown_dict = painting_surface.get_breakdown()
            breakdown_list.append(breakdown_dict)
        return breakdown_list

    # Method to summarise the original list and the budgeted list and combine into a final dictionary of useful info
    def get_summary(self):
        summary_dict_original_job = self.get_surface_list_summary_statistics(self.original_painting_surface_list)
        summary_dict_budgeted_job = self.get_surface_list_summary_statistics(self.budgeted_painting_surface_list)

        # final summary dictionary compares the summary values from original and budgeted list to give
        # new comparison values, total surface area in budget, unpainted area, cost of remaining items
        final_summary_dict = dict(
            budget=self.budget,
            total_budgeted_job_price=round(summary_dict_budgeted_job['total_price'], 2),
            total_surface_area_in_budget=round(summary_dict_budgeted_job['total_surface_area'], 2),
            unpainted_surface_area=round(
            summary_dict_original_job['total_surface_area']-summary_dict_budgeted_job['total_surface_area'], 2),
            cost_for_remaining_items=round(
                summary_dict_original_job['total_price']-summary_dict_budgeted_job['total_price'], 2)
        )
        return final_summary_dict

    #Method which is given the original list and budgeted list separately to summarise
    @staticmethod
    def get_surface_list_summary_statistics(surface_list):
        total_price = 0
        total_surface_area = 0
        for painting_surface in surface_list:
            total_price += painting_surface.get_total_price()
            total_surface_area += painting_surface.surface.area
        return dict(
            total_price=total_price,
            total_surface_area=total_surface_area,
        )



# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- Other things ------------------------------------------------------

# class to contain descriptions of the condition statements which is not currently used in the GUI but could be
# incorporated to display these description when a user wishes to understand the definition of the condition assumptions

class ConditionAssumptions():
    def __init__(self):
        poor = '''Poor condition is where lots of preparation is required. Surfaces exhibit cracking, gaps not filled,
        previously poorly painted with drips, fibres or flaking in the surface paint. Stains from oil or water may be 
        present. There may be joinings of the paper which is painted which requite sticking back. If any of the above
        or multiple faults then condition is poor'''
        okay = '''Okay condition is where there are some faults with the surface and a small amount of preparation is 
        required, the surface may be marked and old but it sound, there may be a few fine cracks or small gaps to 
        fill'''
        good = '''Good condition is where there is almost no preparation required, a light sand, limited fine cracks in
         corners but otherwise a good smooth surface which you are happy with'''

        self.poor = poor
        self.okay = okay
        self.good = good

    def get_condition_assumption(self, condition):
        if condition == 'poor':
            return 'poor_example.jpg'
        else:
            return 'poor_example.jpg'

    def get_condition_description(self, condition):
        if condition == 'poor':
            return self.poor
        elif condition == 'okay':
            return self.okay
        elif condition == 'good':
            return self.good


