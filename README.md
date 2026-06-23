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
- **Immutable by design**: `filter()`/`exclude()` return a **new** `ListQuery` and never mutate the source collection or the object you passed in
- **Method chaining**: Chain multiple filter/exclude operations for complex queries
- **Nested field access**: Navigate nested dictionaries using double underscore notation
- **Strict lookups**: Unknown/typo'd lookups raise `FieldLookupError` instead of silently returning nothing
- **Presence & case-insensitive lookups**: `isnull`, `exists`, `icontains`, `iexact`, `regex`, and more
- **Extensible**: Register custom lookups via a public API
- **Typed**: Ships `py.typed`; `ListQuery` is generic (`ListQuery[T]`) for editor autocomplete
- **Zero dependencies**: Pure Python, no external runtime dependencies

## Available Field Lookups

| Lookup | Description | Example |
|--------|-------------|---------|
| `in` | Value is in a list | `first_name__in=["Blane", "Samara"]` |
| `not` | Value is not equal to | `car_make__not="Land Rover"` |
| `in_range` | Value is in a range (accepts `range` or `(lo, hi)`, half-open) | `id__in_range=range(1, 5)` / `id__in_range=(1, 5)` |
| `lt` | Less than | `id__lt=5` |
| `lte` | Less than or equal to | `id__lte=5` |
| `gt` | Greater than | `id__gt=3` |
| `gte` | Greater than or equal to | `id__gte=3` |
| `startswith` | String starts with | `email__startswith="sblackley"` |
| `endswith` | String ends with | `email__endswith="@imgur.com"` |
| `contains` | String contains substring | `ip_address__contains=".183."` |
| `icontains` | Case-insensitive contains | `email__icontains="EXAMPLE"` |
| `istartswith` | Case-insensitive starts with | `name__istartswith="a"` |
| `iendswith` | Case-insensitive ends with | `email__iendswith=".COM"` |
| `iexact` | Case-insensitive equality | `name__iexact="bob"` |
| `regex` | Matches regular expression | `name__regex=r"^[A-Z]"` |
| `iregex` | Case-insensitive regex | `name__iregex=r"^d"` |
| `isnull` | Field is `None` or absent | `email__isnull=True` |
| `exists` | Field is present (any value) | `email__exists=True` |

> String lookups treat non-string values (e.g. `None`, numbers) as non-matches rather than erroring.

Get the registered lookups programmatically (handy for building UIs/autocomplete):

```python
ListQuery.available_lookups()
# ['contains', 'endswith', 'exists', 'gt', 'gte', 'icontains', ...]
```

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

## Behavior & Semantics

### Immutability

`filter()` and `exclude()` are **non-mutating** — they return a brand-new
`ListQuery` and never modify the original collection or the list you passed to
the constructor:

```python
source = [{"id": 1}, {"id": 2}, {"id": 3}]
lq = ListQuery(source)

result = lq.filter(id__gte=2)

len(source)  # 3 — untouched
len(lq)      # 3 — untouched
len(result)  # 2 — a new ListQuery
```

### Missing fields vs. unknown lookups

- A **field that is absent** in a record is a legitimate non-match — it is
  simply filtered out, no error:
  ```python
  ListQuery(data).filter(missing_field="x")   # -> [] (no error)
  ListQuery(data).filter(car__country="Japan")  # items without car/country just don't match
  ```
- An **unknown or typo'd lookup** raises `FieldLookupError`, so mistakes surface
  immediately instead of silently returning nothing:
  ```python
  ListQuery(data).filter(id__bogus=1)   # raises FieldLookupError
  ```

### Presence checks

Because absent fields normally don't match, use `exists` / `isnull` to query
presence explicitly:

```python
ListQuery(users).filter(email__exists=True)    # only users that have an email key
ListQuery(users).filter(email__isnull=True)    # email is None OR the key is absent
```

## Custom Lookups

Register your own lookups through the public API. A lookup is any callable
`(field_value, query_value) -> bool`.

```python
from collection_query import FieldLookups, ListQuery

# Direct registration
FieldLookups.register("iseven", lambda item, value: (item % 2 == 0) == value)

# Or as a decorator
@FieldLookups.register("isodd")
def is_odd(item, value):
    return (item % 2 == 1) == value

ListQuery([{"n": 1}, {"n": 2}, {"n": 3}]).filter(n__iseven=True)  # [{"n": 2}]
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
