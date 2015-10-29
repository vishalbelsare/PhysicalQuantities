# -*- coding: utf-8 -*-
import numpy as np
from .Quantity import *
from .Unit import UnitError
from . import isphysicalquantity, q

__all__ = ['floor', 'ceil', 'sqrt', 'linspace', 'tophysicalquantity']


def floor(q):
    """ Return the floor of the input, element-wise.

    :return: The floor of each element
    :rtype: PhysicalQuantity

    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.floor(1.3 mm)
    1 mm
    """
    value = np.floor(q.value)
    return q.__class__(value, q.unit)


def ceil(q):
    """ Return the ceiling of the input, element-wise.

    :param q:
    :type q: numpy array
    :return: The ceiling of each element
    :rtype: PhysicalQuantity

    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.ceil(1.3 mm)
    2.0 mm
    """
    value = np.ceil(q.value)
    return q.__class__(value, q.unit)


def sqrt(q):
    """ Return the square root of the input, element-wise.

    :return: The floor of each element
    :rtype: PhysicalQuantity

    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.sqrt(4 m**2)
    2.0 m
    """
    value = np.sqrt(q.value)
    return q.__class__(value, q.unit**0.5)


def linspace(start, stop, num=50,  endpoint=True, retstep=False):
    """ A units-enabled linspace

    :param start: start value
    :type start: PhysicalQuantity or float
    :param stop:  stop value
    :type stop: PhysicalQuantity or float
    :param num: number of points
    :type num: int
    :param endpoint: include stop point
    :param retstep: if true, return (samples, step)
    :return: return equally spaced samples between start and stop

    >>> import PhysicalQuantities.numpywrapper as nw
    >>> nw.linspace(0 GHz, 100 GHz, 200)
    """
    if not isinstance(start, PhysicalQuantity) and not isinstance(stop, PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start, PhysicalQuantity) and isinstance(stop, PhysicalQuantity):
        if start.base.unit != stop.base.unit:
            raise UnitError("Cannot match units")

    unit = None
    if isinstance(start, PhysicalQuantity):
        start_value = start.value
        unit = start.unit
    else:
        start_value = start

    if isinstance(stop, PhysicalQuantity):
        stop_value = stop.value
        unit = stop.unit
    else:
        stop_value = stop

    array = np.linspace(start_value, stop_value, num,  endpoint, retstep)

    if retstep:
        return PhysicalQuantity(array[0], unit), PhysicalQuantity(array[1], unit)
    else:
        return array * PhysicalQuantity(1, unit)


def tophysicalquantity(arr, unit=None):
    """ Convert numpy array or list containing PhysicalQuantity elements to PhysicalQuantity object containing array or list

    :param arr: input array
    :return: PhysicalQuantity wrapped numpy array

    >>> a = [ 1mm, 2m, 3mm]
    >>> b = toPhysicalQuantity(a)
    >>> b
    [ 1 2000 3] mm
    """
    if isphysicalquantity(arr) and type(arr.value) is np.ndarray:
        return arr
    if isphysicalquantity(arr) and type(arr.value) is list:
        newarr = np.array(arr.value)
        return newarr * q[arr.unit]
    if isphysicalquantity(arr):
        raise TypeError('%s is not a valid list or array' % type(arr))
        
    for i, _a in enumerate(arr):
        if not isphysicalquantity(_a) and unit == None:
            raise UnitError('Element %d is not a physical quantity: %s' % (i,_a))

    if unit is None:
        unit = arr[0].unit
    if isphysicalquantity(arr[0]):
        valuetype = type(arr[0].value)
    else:
        valuetype = type(arr[0])

    newarr = np.zeros_like(arr, dtype=valuetype )
    for i, _a in enumerate(arr):
        if isphysicalquantity(_a):
            try:
                newarr[i] = _a.to(unit).value
            except UnitError:
                raise UnitError('Element %d is not same unit as others' % i)
        else:
                newarr[i] = _a
    print("U:", unit)
    return newarr * q[unit]

def argsort(arr):
    return np.argsort(arr.value)
#def any(arr):
#    return np.any(arr.value)
def insert(array, obj, values):
    return np.insert(array.value, obj, values.value) * q[array.unit]
