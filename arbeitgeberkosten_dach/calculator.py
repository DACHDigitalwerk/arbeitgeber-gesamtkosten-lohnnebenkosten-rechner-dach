# -*- coding: utf-8 -*-
"""
Finanzmathematisches und betriebswirtschaftliches Kernmodul fuer den
DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026 (DE, AT, CH).

Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG):
Rein mathematische Orientierungsrechnung fuer Personalbudgetierung und Make-or-Buy-Kalkulation,
keine Lohnsteuer- oder Sozialversicherungsberatung.
"""

from dataclasses import dataclass
from typing import Dict, Any


COUNTRY_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "DE": {
        "currency": "EUR",
        "months_paid": 12.0,
        "ag_social_pct": 20.65,
        "ag_levy_pct": 2.85,
        "bbg_kv_pv_annual": 66_150.0,
        "bbg_rv_av_annual": 96_600.0,
        "description": "DE: AG-Anteile KV/PV/RV/AV (inkl. BBG 2026) + Umlage U1/U2/U3 + BG-Unfallversicherung",
    },
    "AT": {
        "currency": "EUR",
        "months_paid": 14.0,
        "ag_social_pct": 21.03,
        "ag_levy_pct": 8.59,
        "bbg_kv_pv_annual": 0.0,
        "bbg_rv_av_annual": 0.0,
        "description": "AT: OeGK SV-DG (21,03%) + FLAF DB (3,7%) + DZ (0,36%) + KommSt (3,0%) + BVK (1,53%) auf 14 Gehaelter",
    },
    "CH": {
        "currency": "CHF",
        "months_paid": 13.0,
        "ag_social_pct": 13.40,
        "ag_levy_pct": 2.70,
        "bbg_kv_pv_annual": 0.0,
        "bbg_rv_av_annual": 148_200.0,
        "description": "CH: AHV/IV/EO (5,3%) + ALV (1,1% bis 148.200 CHF) + BVG (~7%) + UVG (~0,7%) + KTG (~0,5%) + FAK (~1,5%)",
    },
}


@dataclass
class EmployerCostInput:
    country: str = "DE"
    monthly_gross: float = 5_500.0
    months_paid: float = 12.0
    annual_bonus: float = 3_000.0
    ag_social_pct: float = 20.65
    ag_levy_pct: float = 2.85
    workplace_overhead_annual: float = 6_800.0
    vacation_days: int = 30
    holiday_days: int = 10
    sick_training_days: int = 16
    hours_per_day: float = 8.0
    productivity_pct: float = 80.0
    freelancer_hourly_rate: float = 95.0


@dataclass
class EmployerCostResult:
    country: str
    currency: str
    description: str
    annual_gross: float
    ag_social_cost: float
    ag_levy_cost: float
    pure_personnel_cost: float
    statutory_markup_pct: float
    workplace_overhead_annual: float
    total_employer_cost_annual: float
    total_employer_cost_monthly: float
    total_cost_factor_vs_gross: float
    net_work_days: int
    presence_hours: float
    productive_hours: float
    true_internal_hourly_cost: float
    freelancer_equivalent_annual_cost: float
    make_or_buy_break_even_hours: float


def get_country_defaults(country: str) -> Dict[str, Any]:
    c = country.upper().strip()
    if c not in COUNTRY_DEFAULTS:
        raise ValueError(f"Unsupported country '{country}'. Choose from DE, AT, CH.")
    return COUNTRY_DEFAULTS[c]


def calculate_employer_cost(inp: EmployerCostInput) -> EmployerCostResult:
    std = get_country_defaults(inp.country)
    c = inp.country.upper().strip()

    if inp.monthly_gross < 0:
        raise ValueError("monthly_gross must be non-negative")
    if inp.months_paid < 1.0:
        raise ValueError("months_paid must be at least 1.0")
    if inp.hours_per_day <= 0:
        raise ValueError("hours_per_day must be positive")
    if not (10.0 <= inp.productivity_pct <= 100.0):
        raise ValueError("productivity_pct must be between 10 and 100")
    if inp.freelancer_hourly_rate <= 0:
        raise ValueError("freelancer_hourly_rate must be positive")

    annual_gross = float(inp.monthly_gross) * float(inp.months_paid) + max(0.0, float(inp.annual_bonus))
    social_ratio = max(0.0, float(inp.ag_social_pct)) / 100.0
    levy_ratio = max(0.0, float(inp.ag_levy_pct)) / 100.0
    overhead = max(0.0, float(inp.workplace_overhead_annual))

    # Statutory BBG cap handling for DE
    if c == "DE" and annual_gross > 66_150.0:
        kv_pv_share = min(annual_gross, 66_150.0) * (social_ratio * 0.482)
        rv_av_share = min(annual_gross, 96_600.0) * (social_ratio * 0.518)
        ag_social_cost = kv_pv_share + rv_av_share
    else:
        ag_social_cost = annual_gross * social_ratio

    ag_levy_cost = annual_gross * levy_ratio
    pure_personnel_cost = annual_gross + ag_social_cost + ag_levy_cost
    statutory_markup_pct = ((pure_personnel_cost - annual_gross) / annual_gross * 100.0) if annual_gross > 0 else 0.0

    total_employer_cost = pure_personnel_cost + overhead
    total_monthly = total_employer_cost / 12.0
    cost_factor = (total_employer_cost / annual_gross) if annual_gross > 0 else 1.0

    net_work_days = max(1, 365 - 104 - int(inp.vacation_days) - int(inp.holiday_days) - int(inp.sick_training_days))
    presence_hours = float(net_work_days) * float(inp.hours_per_day)
    productive_hours = max(1.0, presence_hours * (float(inp.productivity_pct) / 100.0))

    true_hourly = total_employer_cost / productive_hours
    freelancer_annual = productive_hours * float(inp.freelancer_hourly_rate)
    break_even_hours = total_employer_cost / float(inp.freelancer_hourly_rate)

    return EmployerCostResult(
        country=c,
        currency=std["currency"],
        description=std["description"],
        annual_gross=round(annual_gross, 2),
        ag_social_cost=round(ag_social_cost, 2),
        ag_levy_cost=round(ag_levy_cost, 2),
        pure_personnel_cost=round(pure_personnel_cost, 2),
        statutory_markup_pct=round(statutory_markup_pct, 2),
        workplace_overhead_annual=round(overhead, 2),
        total_employer_cost_annual=round(total_employer_cost, 2),
        total_employer_cost_monthly=round(total_monthly, 2),
        total_cost_factor_vs_gross=round(cost_factor, 4),
        net_work_days=net_work_days,
        presence_hours=round(presence_hours, 2),
        productive_hours=round(productive_hours, 2),
        true_internal_hourly_cost=round(true_hourly, 2),
        freelancer_equivalent_annual_cost=round(freelancer_annual, 2),
        make_or_buy_break_even_hours=round(break_even_hours, 2),
    )
