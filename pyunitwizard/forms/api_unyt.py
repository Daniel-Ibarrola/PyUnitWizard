from sympy import im
from pyunitwizard._private.exceptions import *
from pyunitwizard._private.quantity_or_unit import ArrayLike
from typing import Any, Dict, Union

try:
    import unyt
    from unyt import unyt_array, unyt_quantity, Unit
except:
    raise LibraryNotFoundError('unyt')

form_name = 'unyt'
parser = True

is_form = {
    unyt_array:    form_name,
    unyt_quantity: form_name,
    Unit:          form_name,
}


def is_quantity(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is a unyt quantity.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit

        Returns
        -------
        bool
            True if it is a unyt.unyt_array or unyt.unyt_quantity.
    """
    return isinstance(quantity_or_unit, (unyt_array, unyt_quantity))

def is_unit(quantity_or_unit: Any) -> bool:
    """ Check whether a quantity or unit is a unyt unit.

        Parameters
        -----------
        quantity_or_unit : Any
            A quanitity or a unit.

        Returns
        -------
        bool
            True if it is a unyt.Unit.
    """
    return isinstance(quantity_or_unit, Unit)

def dimensionality(quantity_or_unit: Union[unyt_array, unyt_quantity, Unit]
                  ) -> Dict[str, int]:
    """ Returns the dimensionality of the quantity or unit.

        Parameters
        -----------
        quantity_or_unit : pint.Quantity or pint.Unit
            A quanitity or a unit

        Returns
        -------
        dimensionality_dict : dict
            Dictionary which keys are fundamental units and values are the exponent of
            each unit in the quantity.

    """
    # We get the dimensionality by transforming first to pint because
    # unyt handles dimensions in a different way. Might change this in
    # the future.
    from .api_pint import dimensionality as dimensionality_pint

    if is_unit(quantity_or_unit):
        temp_quantity = 1 * quantity_or_unit
    else:
        temp_quantity = quantity_or_unit
    temp_quantity = temp_quantity.to_pint()

    return dimensionality_pint(temp_quantity)
    

def compatibility(quantity_or_unit_1: Union[unyt_array, unyt_quantity, Unit], 
                  quantity_or_unit_2: Union[unyt_array, unyt_quantity, Unit]
                  ) -> bool:
    """ Check whether two quantities or units are compatible.

        Parameters
        ----------
        quantity_or_unit_1 : unyt_array or unyt_quantity or Unit
            A quanitity or a unit.

        quantity_or_unit_2 : unyt_array or unyt_quantity or Unit
            A quanitity or a unit.

        Returns
        -------
        bool
            True if they are compatible.
    """
    if is_quantity(quantity_or_unit_1):
        unit_1 = get_unit(quantity_or_unit_1)
    else:
        unit_1 = quantity_or_unit_1
    
    if is_quantity(quantity_or_unit_2):
        unit_2 = get_unit(quantity_or_unit_2)
    else:
        unit_2 = unit_2

    return unit_1.same_dimensions_as(unit_2)

def make_quantity(value: Union[int, float, ArrayLike], 
                  unit: Union[str, Unit]) -> Union[unyt_array, unyt_quantity]:
    """ Returns a unyt quantity.

        Parmeters
        ---------
        value: int, float or ArrayLike
            The value of the quantity.

        unit : Unit or str
            The unit.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The quantity.
    """ 
    if isinstance(value, (int, float)):
        return unyt_quantity(value, unit)
    else:
        return unyt_array(value, unit)

def string_to_quantity(string):

    raise LibraryWithoutParserError("Unyt library has no string parser")

def to_string(quantity_or_unit: Union[unyt_array, 
                                unyt_quantity,
                                Unit]) -> str:
    """ Convert a quantity to string. 

        Parameters
        -----------
        quantity_or_unit : unyt_array or unyt_quantity or Unit
            A quanitity or a unit.

        Returns
        -------
        str
            The quantitity as a string.
    """
    return str(quantity_or_unit)

def convert(quantity: Union[unyt_array, unyt_quantity], 
            unit_name: str) -> Union[unyt_array, unyt_quantity]:
    """ Converts the quantity to a different unit.

        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        unit : str
            The unit to convert to.
        
        Returns
        -------
        unyt_array or unyt_quantity
            The converted quantity.
    """
    return quantity.to(unit_name)

def get_value(quantity: Union[unyt_array, 
                        unyt_quantity]) -> Union[int, float, ArrayLike]:
    """ Returns the value of the quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        Returns
        -------
        int, float or ArrrayLike
            The value.
    """
    return quantity.value

def get_unit(quantity: Union[unyt_array, 
                       unyt_quantity]) -> Unit:
    """ Returns the units of the quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity or a unit.
        
        Returns
        -------
        Unit
            The unit.
    """
    return quantity.units

def change_value(quantity: Union[unyt_quantity, unyt_array],
                 value: Union[int, float, ArrayLike]) -> Union[unyt_array, unyt_quantity]:

    return make_quantity(value, get_unit(quantity))

def to_pint(quantity: Union[unyt_array, 
                       unyt_quantity]):
    """ Transform a quantity from unyt to a pint quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity.
        
        Returns
        -------
        pint.Quantity
            The quantity.
    """
    from .api_pint import ureg
    return quantity.to_pint(unit_registry=ureg)

def to_openmm_unit(quantity: Union[unyt_array, unyt_quantity]):
    """ Transform a quantity from unyt to an openmm.unit quantity.
        
        Parameters
        -----------
        quantity : unyt_array or unyt_quantity
            A quanitity.
        
        Returns
        -------
        openmm.unit.Quantity
            The quantity.
    """
    # Convert to pint quantity first and then to openmm. Temporary solution
    from .api_pint import to_openmm_unit as pint_to_openmm

    return pint_to_openmm(quantity.to_pint())

