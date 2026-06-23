# Collection Query

[![PyPI version](https://img.shields.io/pypi/v/collection-query.svg)](https://pypi.org/project/collection-query/)
[![Python versions](https://img.shields.io/pypi/pyversions/collection-query.svg)](https://pypi.org/project/collection-query/)
[![License: MIT](https://img.shields.io/pypi/l/collection-query.svg)](https://github.com/vanya1301/collection_query/blob/develop/LICENSE)

A Python library that provides Django-style query syntax for filtering and navigating through large JSON payloads serialized into Python collection objects (lists, dictionaries, etc.).

📦 **Available on PyPI:** https://pypi.org/project/collection-query/

## Problem Solved

When working with large JSON payloads or complex nested data structures in Python, extracting specific data often requires writing verbose loops, list comprehensions, or deeply nested dictionary access patterns. This becomes unwieldy and error-prone as the data complexity grows.

**Traditional approach:**
```python
# Find all users with first_name "Blane" or "Samara" with ID < 5
results = []
for item in data:
    if item.get("first_name") in ["Blane", "Samara"] and item.get("id", 0) < 5:
        results.append(item)
```

**With Collection Query:**
```python
from collection_query import ListQuery

results = ListQuery(data).filter(
    first_name__in=["Blane", "Samara"], 
    id__lt=5
)
```

## Features

- **Django-style query syntax**: Use familiar field lookups like `field__in`, `field__gt`, `field__contains`
- **Method chaining**: Chain multiple filter/exclude operations for complex queries
- **Nested field access**: Navigate nested dictionaries using double underscore notation
- **Extensible**: Easy to add custom field lookup operations
- **Zero dependencies**: Pure Python, no external runtime dependencies

## Available Field Lookups

| Lookup | Description | Example |
|--------|-------------|---------|
| `in` | Value is in a list | `first_name__in=["Blane", "Samara"]` |
| `not` | Value is not equal to | `car_make__not="Land Rover"` |
| `in_range` | Value is in a range | `id__in_range=range(1, 5)` |
| `lt` | Less than | `id__lt=5` |
| `lte` | Less than or equal to | `id__lte=5` |
| `gt` | Greater than | `id__gt=3` |
| `gte` | Greater than or equal to | `id__gte=3` |
| `startswith` | String starts with | `email__startswith="sblackley"` |
| `endswith` | String ends with | `email__endswith="@imgur.com"` |
| `contains` | String contains substring | `ip_address__contains=".183."` |

## Installation

### Requirements

- Python 3.8 or higher

### Install from PyPI

The package is published on PyPI: **https://pypi.org/project/collection-query/**

```bash
pip install collection-query
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add collection-query
```

Then import and use it:

```python
from collection_query import ListQuery
```

### For Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. Clone the repository:
```bash
git clone https://github.com/vanya1301/collection_query.git
cd collection_query
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Run tests to verify installation:
```bash
python -m unittest discover -v
```

**Tested Python versions:** 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

## Usage Examples

### Basic Filtering

**Traditional approach:**
```python
# Find all users named "Donalt"
results = [item for item in data if item.get("first_name") == "Donalt"]
```

**With Collection Query:**
```python
from collection_query import ListQuery

results = ListQuery(data).filter(first_name="Donalt")
```

### Multiple Conditions (AND logic)

**Traditional approach:**
```python
# Find users named "Donalt" who drive a Toyota
results = [
    item for item in data 
    if item.get("first_name") == "Donalt" and item.get("car_make") == "Toyota"
]
```

**With Collection Query:**
```python
results = ListQuery(data).filter(
    first_name="Donalt", 
    car_make="Toyota"
)
```

### Using Field Lookups

**Traditional approach:**
```python
# Find users with ID less than 5
results = [item for item in data if item.get("id", 0) < 5]

# Find users with ID in specific range
results = [item for item in data if 1 <= item.get("id", 0) < 5]

# Find users whose email contains specific text
results = [
    item for item in data 
    if ".183." in item.get("ip_address", "")
]
```

**With Collection Query:**
```python
results = ListQuery(data).filter(id__lt=5)
results = ListQuery(data).filter(id__in_range=range(1, 5))
results = ListQuery(data).filter(ip_address__contains=".183.")
```

### Method Chaining

**Traditional approach:**
```python
# Find users with ID >= 3, exclude those named "Donalt", then exclude Toyota drivers
temp1 = [item for item in data if item.get("id", 0) >= 3]
temp2 = [item for item in temp1 if item.get("first_name") != "Donalt"]
results = [item for item in temp2 if item.get("car_make") != "Toyota"]
```

**With Collection Query:**
```python
results = (ListQuery(data)
    .filter(id__gte=3)
    .exclude(first_name="Donalt")
    .exclude(car_make="Toyota")
)
```

### Nested Field Access

**Traditional approach:**
```python
# Find items where nested car.country is "Japan"
results = [
    item for item in nested_dict_data 
    if item.get("car", {}).get("country") == "Japan"
]

# Find items where car.country is in ["Japan", "Germany"]
results = [
    item for item in nested_dict_data 
    if item.get("car", {}).get("country") in ["Japan", "Germany"]
]
```

**With Collection Query:**
```python
results = ListQuery(nested_dict_data).filter(car__country="Japan")
results = ListQuery(nested_dict_data).filter(car__country__in=["Japan", "Germany"])
```

### Combining Filter and Exclude

**Traditional approach:**
```python
# Keep items matching condition, but exclude others
filtered = [item for item in data if item.get("id", 0) >= 3]
results = [item for item in filtered if item.get("first_name") != "Donalt"]
```

**With Collection Query:**
```python
results = ListQuery(data).filter(id__gte=3).exclude(first_name="Donalt")
```

### Real-World Example: API Response Processing

```python
from collection_query import ListQuery

# Assume this is a large API response
api_response = {
    "users": [
        {"id": 1, "name": "Alice", "department": {"name": "Engineering", "budget": 100000}},
        {"id": 2, "name": "Bob", "department": {"name": "Sales", "budget": 50000}},
        {"id": 3, "name": "Charlie", "department": {"name": "Engineering", "budget": 120000}},
        # ... hundreds more users
    ]
}

# Find all Engineering users with budget > 100000
engineers = (ListQuery(api_response["users"])
    .filter(department__name="Engineering")
    .filter(department__budget__gt=100000))

for engineer in engineers:
    print(f"{engineer['name']} - Budget: ${engineer['department']['budget']}")
```

## Testing

Run all tests:
```bash
python -m unittest discover -v
```

Run specific test file:
```bash
python -m unittest tests.test_field_lookups -v
```

Run specific test class:
```bash
python -m unittest tests.test_field_lookups.FieldsLookupTestCase -v
```

Run specific test method:
```bash
python -m unittest tests.test_field_lookups.FieldsLookupTestCase.test_field_lookup_in -v
```

## License

MIT License - feel free to use in your projects.
