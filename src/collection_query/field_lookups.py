from __future__ import annotations


class FieldLookups:
    @staticmethod
    def _in(item, value: list) -> bool:
        return item in value

    @staticmethod
    def _not(item, value) -> bool:
        return item != value

    @staticmethod
    def _in_range(item, value: range) -> bool:
        return item in value

    @staticmethod
    def _lt(item, value) -> bool:
        return item < value

    @staticmethod
    def _lte(item, value) -> bool:
        return item <= value

    @staticmethod
    def _gt(item, value) -> bool:
        return item > value

    @staticmethod
    def _gte(item, value) -> bool:
        return item >= value

    @staticmethod
    def _startswith(item: str, value: str) -> bool:
        return item.startswith(value)

    @staticmethod
    def _endswith(item: str, value: str) -> bool:
        return item.endswith(value)

    @staticmethod
    def _contains(item: str, value: str) -> bool:
        return value in item
