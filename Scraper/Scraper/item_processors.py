from itemloaders.processors import TakeFirst, Identity, MapCompose, Compose

from .utils import cleanse_str, str_to_int, set_empty_val_to_none


def process_int(*extra_functions):
    """
    Cleanse all values, convert them to integers and remove all the empty ones

    :param extra_functions: if you wish to apply any additional function to list
    """

    return MapCompose(
        cleanse_str,
        str_to_int,
        set_empty_val_to_none,
        *extra_functions
    )


def process_str(*extra_functions):
    """
    Cleanse all values and remove all the empty ones

    :param extra_functions: if you wish to apply any additional function to list
    """

    return MapCompose(
        cleanse_str,
        set_empty_val_to_none,
        *extra_functions
    )


def process_seller_type(values):
    """
    Return ["compamy"] if values is not empty, else ["person"]
    """

    return ["company"] if values else ["person"]


def take_last(values):
    """
    Returns last item
    """

    return values[-1]
