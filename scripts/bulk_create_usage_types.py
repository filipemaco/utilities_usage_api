from usages.models import UsageType

usage_types_data = [
    {'name': 'electricity', 'unit': 'kwh', 'factor': 1.5},
    {'name': 'water', 'unit': 'kg', 'factor': 26.93},
    {'name': 'heating', 'unit': 'kwh', 'factor': 3.892},
    {'name': 'heating', 'unit': 'l', 'factor': 8.57},
    {'name': 'heating', 'unit': 'm3', 'factor': 19.456},
]


def bulk_create_usage_types():
    objs = []
    for usage_type in usage_types_data:
        objs.append(UsageType(
            name=usage_type['name'],
            unit=usage_type['unit'],
            factor=usage_type['factor']
        ))

    UsageType.objects.bulk_create(objs)
