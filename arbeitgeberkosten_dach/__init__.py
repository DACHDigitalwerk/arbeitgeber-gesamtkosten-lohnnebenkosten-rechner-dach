"""
arbeitgeberkosten_dach — DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026
"""

from .calculator import (
    EmployerCostInput,
    EmployerCostResult,
    calculate_employer_cost,
    get_country_defaults,
)

__all__ = [
    "EmployerCostInput",
    "EmployerCostResult",
    "calculate_employer_cost",
    "get_country_defaults",
]
__version__ = "1.0.0"
