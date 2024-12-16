import json, dataclasses
from itemloaders.processors import TakeFirst, Identity, MapCompose, Compose

from .formatting_utils import cleanse_str, str_to_int, set_empty_val_to_none
from .parsing_utils import encode_url


def process_int(*extra_functions):
    """
    Cleanse all values, convert them to integers and remove all the empty ones

    :param extra_functions: if you wish to apply any additional function to list
    """

    return MapCompose(cleanse_str, str_to_int, set_empty_val_to_none, *extra_functions)


def process_str(*extra_functions):
    """
    Cleanse all values and remove all the empty ones

    :param extra_functions: if you wish to apply any additional function to list
    """

    return MapCompose(cleanse_str, set_empty_val_to_none, *extra_functions)


def process_seller_type(values):
    """
    Return ["company"] if values is not empty, else ["person"]
    """

    return ["company"] if values else ["person"]


def take_last(values):
    """
    Returns last item
    """

    return values[-1]


# Custom json encoder to handle dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            r = dataclasses.asdict(o)
            return r
        return super().default(o)


def dataclass_to_json(dtcls: dataclasses):
    return json.dumps(dtcls, cls=EnhancedJSONEncoder)


def replace_relative_url(values: list[str]):
    return [url.replace("..", "https://avto.net").replace(" ", "%20") for url in values]


def process_list_of_tuples(values: list[tuple[str, str]]):
    output = []
    for val_1, val_2 in values:
        if not val_1 or not val_2:
            continue

        if isinstance(val_1, list):
            val_1 = "".join(val_1)
        if isinstance(val_2, list):
            val_2 = "".join(val_2)

        output.append((cleanse_str(val_1), cleanse_str(val_2)))

    return output