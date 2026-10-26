# -*- coding: utf-8 -*-
"""
Unit-Tests fuer arbeitgeberkosten_dach (DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026)
"""

import pytest
from arbeitgeberkosten_dach import (
    EmployerCostInput,
    calculate_employer_cost,
    get_country_defaults,
)


def test_default_de_calculation():
    """Prueft die Standardberechnung fuer Deutschland (5.500 EUR x 12 + 3.000 EUR Bonus = 69.000 EUR)."""
    inp = EmployerCostInput()
    res = calculate_employer_cost(inp)
    assert res.country == "DE"
    assert res.currency == "EUR"
    assert res.annual_gross == pytest.approx(69_000.0)
    assert res.pure_personnel_cost > 80_000.0
    assert res.total_employer_cost_annual == pytest.approx(res.pure_personnel_cost + 6_800.0)


def test_de_bbg_cap_applied_for_high_earners():
    """Prueft, dass bei Spitzenverdienern in DE die Beitragsbemessungsgrenze (BBG 2026) die AG-Sozialabgaben deckelt."""
    res_100k = calculate_employer_cost(EmployerCostInput(monthly_gross=8_500.0, annual_bonus=0.0))
    res_200k = calculate_employer_cost(EmployerCostInput(monthly_gross=17_000.0, annual_bonus=0.0))
    # Above 96.600 EUR RV/AV BBG, AG social security contributions must stay capped
    assert res_200k.ag_social_cost == pytest.approx(res_100k.ag_social_cost)


def test_austria_14_months_and_statutory_levies():
    """Prueft das oesterreichische Modell mit 14 Monatsgehaeltern und rund 29,62 % Lohnnebenkosten."""
    std = get_country_defaults("AT")
    inp = EmployerCostInput(
        country="AT",
        monthly_gross=4_000.0,
        months_paid=std["months_paid"],
        annual_bonus=0.0,
        ag_social_pct=std["ag_social_pct"],
        ag_levy_pct=std["ag_levy_pct"],
    )
    res = calculate_employer_cost(inp)
    assert res.country == "AT"
    assert res.annual_gross == pytest.approx(56_000.0)
    assert res.statutory_markup_pct == pytest.approx(29.62, rel=1e-2)


def test_switzerland_chf_13_months():
    """Prueft das Schweizer Modell in CHF mit 13 Monatsloehnen."""
    std = get_country_defaults("CH")
    inp = EmployerCostInput(
        country="CH",
        monthly_gross=8_000.0,
        months_paid=std["months_paid"],
        annual_bonus=0.0,
        ag_social_pct=std["ag_social_pct"],
        ag_levy_pct=std["ag_levy_pct"],
    )
    res = calculate_employer_cost(inp)
    assert res.country == "CH"
    assert res.currency == "CHF"
    assert res.annual_gross == pytest.approx(104_000.0)
    assert res.statutory_markup_pct == pytest.approx(16.10, rel=1e-2)


def test_productive_hours_and_internal_hourly_cost():
    """Prueft die Berechnung der Anwesenheitstage und Produktivstunden."""
    inp = EmployerCostInput(
        vacation_days=30,
        holiday_days=10,
        sick_training_days=16,
        hours_per_day=8.0,
        productivity_pct=80.0,
    )
    res = calculate_employer_cost(inp)
    # 365 - 104 - 30 - 10 - 16 = 205 Tage
    assert res.net_work_days == 205
    assert res.presence_hours == pytest.approx(1_640.0)
    assert res.productive_hours == pytest.approx(1_312.0)
    assert res.true_internal_hourly_cost == pytest.approx(res.total_employer_cost_annual / 1_312.0, rel=1e-3)


def test_make_or_buy_break_even_hours():
    """Prueft den Break-Even-Stundenvergleich gegenueber einem externen Freelancer."""
    inp = EmployerCostInput(freelancer_hourly_rate=100.0)
    res = calculate_employer_cost(inp)
    assert res.make_or_buy_break_even_hours == pytest.approx(res.total_employer_cost_annual / 100.0, rel=1e-3)


def test_zero_workplace_overhead():
    """Prueft, dass ohne Arbeitsplatz-Overhead die Gesamtkosten exakt den reinen Personalkosten entsprechen."""
    inp = EmployerCostInput(workplace_overhead_annual=0.0)
    res = calculate_employer_cost(inp)
    assert res.total_employer_cost_annual == pytest.approx(res.pure_personnel_cost)


def test_lower_productivity_increases_hourly_cost():
    """Prueft, dass geringere Produktivitaet den wahren internen Stundensatz erhoeht."""
    res_80 = calculate_employer_cost(EmployerCostInput(productivity_pct=80.0))
    res_60 = calculate_employer_cost(EmployerCostInput(productivity_pct=60.0))
    assert res_60.true_internal_hourly_cost > res_80.true_internal_hourly_cost


def test_invalid_country_raises():
    """Prueft Fehlerbehandlung bei ungueltigem Land."""
    with pytest.raises(ValueError, match="Unsupported country"):
        get_country_defaults("NL")


def test_invalid_inputs_raise():
    """Prueft Fehlerbehandlung bei ungueltigen numerischen Parametern."""
    with pytest.raises(ValueError):
        calculate_employer_cost(EmployerCostInput(monthly_gross=-100.0))
    with pytest.raises(ValueError):
        calculate_employer_cost(EmployerCostInput(productivity_pct=5.0))
    with pytest.raises(ValueError):
        calculate_employer_cost(EmployerCostInput(freelancer_hourly_rate=0.0))
