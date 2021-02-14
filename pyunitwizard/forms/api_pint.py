import pint as pint

## Create a unit UnitRegistry
## See: https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
U_ = ureg.Unit

##

form_name = 'pint'

is_form={
    pint.Quantity:form_name,
    pint.Unit:form_name,
    Q_:form_name,
    U_:form_name,
    }

def is_quantity(quantity_or_unit):

    tmp_type = type(quantity_or_unit)
    output = (tmp_type==pint.Quantity or tmp_type==Q_)

    return output

def is_unit(quantity_or_unit):

    tmp_type = type(quantity_or_unit)
    output = (tmp_type==pint.Unit or tmp_type==U_)

    return output

def make_quantity(value, unit_name):

    return Q_(value, unit_name)

def get_value(quantity):

    return quantity.magnitude

def get_unit(quantity):

    return quantity.units

def string_to_quantity(string):

    tmp_quantity=Q_(string)
    return tmp_quantity

def string_to_unit(string):

    tmp_quantity = string_to_quantity(string)
    return get_unit(tmp_quantity)

def to_string(quantity_or_item):

    return quantity_or_item.__str__()

def convert(quantity, unit_name):

    return quantity.to(unit_name)

def to_simtk_unit(quantity):

    from .api_simtk_unit import make_quantity as make_simtk_unit_quantity

    value = get_value(quantity)
    unit_name = to_string(get_unit(quantity))

    return make_simtk_unit_quantity(value, unit_name)

