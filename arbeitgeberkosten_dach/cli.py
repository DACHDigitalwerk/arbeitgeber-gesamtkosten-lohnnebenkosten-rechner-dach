# -*- coding: utf-8 -*-
"""
CLI fuer den DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026
"""

import argparse
import json
from .calculator import EmployerCostInput, calculate_employer_cost, get_country_defaults


def main():
    parser = argparse.ArgumentParser(
        description="DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026 (DE, AT, CH)"
    )
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"], help="Land (DE, AT, CH)")
    parser.add_argument("--monthly-gross", type=float, default=5_500.0, help="Monatsbruttogehalt")
    parser.add_argument("--months-paid", type=float, default=None, help="Anzahl Monatsgehaelter pro Jahr (z. B. 12, 13, 14)")
    parser.add_argument("--bonus", type=float, default=3_000.0, help="Variabler Jahresbonus")
    parser.add_argument("--overhead", type=float, default=6_800.0, help="Arbeitsplatz-, IT- & Lizenz-Overhead p.a.")
    parser.add_argument("--productivity", type=float, default=80.0, help="Produktivitaetsgrad in Prozent (%%)")
    parser.add_argument("--freelancer-rate", type=float, default=95.0, help="Externer Freelancer-Stundensatz fuer Make-or-Buy")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()
    std = get_country_defaults(args.country)
    months = args.months_paid if args.months_paid is not None else std["months_paid"]

    inp = EmployerCostInput(
        country=args.country,
        monthly_gross=args.monthly_gross,
        months_paid=months,
        annual_bonus=args.bonus,
        ag_social_pct=std["ag_social_pct"],
        ag_levy_pct=std["ag_levy_pct"],
        workplace_overhead_annual=args.overhead,
        productivity_pct=args.productivity,
        freelancer_hourly_rate=args.freelancer_rate,
    )
    res = calculate_employer_cost(inp)

    if args.json:
        print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
    else:
        print("=" * 74)
        print(f"DACH ARBEITGEBER-GESAMTKOSTEN-ANALYSE 2026 ({res.country} / {res.currency})")
        print("=" * 74)
        print(f"Systematik                 : {res.description}")
        print(f"Jahresbruttogehalt         : {res.annual_gross:,.2f} {res.currency}")
        print(f"Reine AG-Personalkosten    : {res.pure_personnel_cost:,.2f} {res.currency} (+{res.statutory_markup_pct:.1f} %)")
        print(f"AG-Gesamtkosten inkl. IT   : {res.total_employer_cost_annual:,.2f} {res.currency} (Faktor {res.total_cost_factor_vs_gross:.2f}x)")
        print(f"Produktivstunden / Jahr    : {res.productive_hours:,.0f} Std. ({res.net_work_days} Arbeitstage)")
        print(f"Wahrer AG-Stundensatz      : {res.true_internal_hourly_cost:,.2f} {res.currency} / Std.")
        print(f"Make-or-Buy Break-Even     : ab {res.make_or_buy_break_even_hours:,.0f} Std./Jahr gewinnt Festanstellung")
        print("=" * 74)


if __name__ == "__main__":
    main()
