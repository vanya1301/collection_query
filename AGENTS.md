# Collection Query - Agent Guidelines

## Build, Lint, and Test Commands

This is a Python 3.8+ project using uv for dependency management.

### Testing
- **Run all tests**: `python -m unittest discover -v` or `python -m unittest tests -v`
- **Run single test file**: `python -m unittest tests.test_file_name -v`
- **Run single test class**: `python -m unittest tests.test_file_name.TestClassName -v`
- **Run single test method**: `python -m unittest tests.test_file_name.TestClassName.test_method_name -v`

Example: `python -m unittest tests.test_field_lookups.FieldsLookupTestCase.test_field_lookup_in -v`

### No Linting/Formatting Tools Configured
This project does not currently use automated linting (ruff, black, mypy, pylint, flake8, etc.).

## Code Style Guidelines

### Imports
- Always start with `from __future__ import annotations` in all Python modules
- Use absolute imports from project modules (e.g., `from collection_query.field_lookups import FieldLookups`)
- Group imports: standard library → third-party → local (though this project only has local imports)
- No unused imports

### Type Hints
- Use type hints for method parameters and return values
- Examples: `def _in(item, value: list) -> bool:`, `def filter(self, **kwargs) -> ListQuery:`

### Naming Conventions
- **Classes**: CamelCase (e.g., `ListQuery`, `FieldLookups`)
- **Functions/Methods**: snake_case (e.g., `filter`, `exclude`, `_evaluate_condition`)
- **Private methods**: prefix with underscore (e.g., `_evaluate_condition`, `_delete_condition_matching_items`)
- **Variables**: snake_case
- **Constants**: UPPER_CASE (though not extensively used in this codebase)
- **Test classes**: `<Name>TestCase` (e.g., `FieldsLookupTestCase`, `EqualsConditionTestCase`)
- **Test files**: `test_<feature>.py` (e.g., `test_field_lookups.py`)
- **Test methods**: `test_<scenario>` (e.g., `test_field_lookup_in`)

### Formatting
- Use walrus operator (`:=`) when appropriate for assignments within expressions
- Example: `if func := getattr(FieldLookups, f"_{i}", None):`
- Walrus operator requires Python 3.8+
- Keep lines reasonably long but readable (no strict limit observed)
- Use spaces, not tabs

### Classes and Methods
- Use `@staticmethod` for utility methods that don't need class/instance access
- All `FieldLookups` methods are static methods
- Chainable methods return `self` to support method chaining
- Use `hasattr()` with `callable()` for duck-typing checks

### Error Handling
- No explicit error handling in current codebase
- Relies on Python's built-in exceptions
- Consider using assertions in tests (e.g., `self.assertEqual`, `self.assertTrue`)

### Testing Patterns
- Use `unittest.TestCase` as base class
- Use `setUp()` for test initialization
- Test methods should be descriptive about what they test
- Verify results with both length checks and content iteration
- Test both positive and negative cases
- Include `if __name__ == '__main__': unittest.main()` guard in test files

### Code Organization
- Main source: `src/collection_query/list_query.py`, `src/collection_query/field_lookups.py` (src layout, importable as `collection_query`)
- Tests in `tests/` directory, test data in `tests/test_data/data.py`
- Use wildcard imports from test data: `from tests.test_data.data import *`

### Query Syntax (Domain-Specific)
- Uses Django-style query syntax for filtering
- Field lookups use double underscore notation: `field__lookup=value`
- Supported lookups: `in`, `not`, `in_range`, `lt`, `lte`, `gt`, `gte`, `startswith`, `endswith`, `contains`
- Nested field access: `car__country="Japan"`
- Filter/exclude accept multiple kwargs for AND conditions

### Python Version
- Target: Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- Minimum: 3.8 (walrus operator `:=` requirement)
- Tested on: 3.10.15, 3.12.2, 3.12.3, 3.12.6
- Use modern Python features appropriate for 3.8+

## Project Overview

This is a collection query library that provides Django-style query syntax for filtering Python list collections containing dictionaries.

### Core Components
- **ListQuery**: Extends Python's `list` class, adds `filter()` and `exclude()` methods
- **FieldLookups**: Static utility methods implementing field lookup operations (in, not, in_range, comparisons, string matching)

### Data Structures
- Operates on lists of dictionaries
- Supports nested dictionaries (e.g., `{"car": {"name": "Toyota", "country": "Japan"}}`)
- Example data structure:
  ```python
  data = [
      {"id": 1, "first_name": "Blane", "car_make": "Chevrolet"},
      {"id": 2, "first_name": "Sonnnie", "car_make": "Dodge"}
  ]
  ```

### Usage Patterns
```python
from collection_query import ListQuery

# Create a ListQuery from a list of dicts
lq = ListQuery(data)

# Filter with field equality
lq.filter(first_name="Blane")

# Filter with field lookups
lq.filter(first_name__in=["Blane", "Samara"])
lq.filter(id__lt=5)
lq.filter(email__contains="@example.com")

# Filter nested fields
lq.filter(car__country="Japan")

# Exclude items
lq.exclude(car_make="Land Rover")

# Chain operations
lq.filter(id__gte=3).exclude(first_name="Donalt")
```

### Filter vs Exclude
- **filter()**: Keeps only items matching all conditions (AND logic)
- **exclude()**: Removes items matching all conditions (keeps non-matching items)
- Multiple kwargs in one call are AND-ed together; chaining applies operations sequentially

## Development Guidelines

### When Adding New Field Lookups
1. Add a new static method to `FieldLookups` class with prefix `_`
2. Method signature: `def _lookup_name(item, value) -> bool:`
3. Name becomes accessible as `field__lookup_name=value` in queries
4. Add tests in `tests/test_field_lookups.py` following existing patterns

### When Adding Test Cases
1. Create new test file: `tests/test_<feature>.py`
2. Import test data: `from tests.test_data.data import *`
3. Create test class inheriting from `unittest.TestCase`
4. Name test class: `<Feature>TestCase`, test methods: `test_<scenario>`
5. Include test guard: `if __name__ == '__main__': unittest.main()`
6. Consider adding test data to `tests/test_data/data.py` if needed

### File Modifications
- When modifying core functionality (ListQuery, FieldLookups), update related tests
- Use existing test data patterns when creating new tests
- Maintain consistency with existing code style and patterns
