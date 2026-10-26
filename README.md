# 👥 DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026 (`arbeitgeberkosten_dach`)

[![CI & Pytest](https://github.com/DACHDigitalwerk/arbeitgeber-gesamtkosten-lohnnebenkosten-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/arbeitgeber-gesamtkosten-lohnnebenkosten-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Live Web-App](https://img.shields.io/badge/Live_Web_App-100%25_Client_Side-10b981)](https://dachdigitalwerk.github.io/arbeitgeber-gesamtkosten-rechner/)

Betriebswirtschaftliche Python-Bibliothek und CLI (`dach-arbeitgeberkosten`) zur Berechnung der **wahren Arbeitgeber-Gesamtkosten, gesetzlichen Lohnnebenkosten (inkl. BBG 2026), effektiven Produktivstunden und des internen Arbeitgeber-Stundensatzes im Make-or-Buy-Vergleich (Festanstellung vs. Freelancer)** für **Deutschland (DE), Österreich (AT) und die Schweiz (CH)**.

---

## 🌐 Interaktive Web-Applikation & HR/CFO-Fachratgeber (100 % Client-Side)

Nutzen Sie den kostenlosen Online-Rechner mit **druckfertigem DIN-A4 Personalbudget- & Lohnnebenkosten-Datenblatt** direkt im Browser:

- 🚀 **[DACH Arbeitgeber-Gesamtkosten-, Lohnnebenkosten- & Personalbudget-Rechner 2026](https://dachdigitalwerk.github.io/arbeitgeber-gesamtkosten-rechner/)**
- 📘 **[Lohnnebenkosten Arbeitgeber 2026 berechnen: Der wahre Kostenfaktor in DE, AT & CH](https://dachdigitalwerk.github.io/lohnnebenkosten-arbeitgeber-berechnen-faktor-2026-dach.html)**
- 📊 **[Was kostet ein Mitarbeiter wirklich? Vom Bruttogehalt zum internen Stundensatz](https://dachdigitalwerk.github.io/was-kostet-ein-mitarbeiter-wirklich-brutto-plus-nebenkosten.html)**
- ⚖️ **[Festanstellung vs. Freelancer 2026: Make-or-Buy-Kostenvergleich für Unternehmen](https://dachdigitalwerk.github.io/festanstellung-vs-freelancer-kostenvergleich-rechner-b2b.html)**
- 🏠 **[DACH Digitalwerk – Alle 34 Self-Serve Web-Tools im Überblick](https://dachdigitalwerk.github.io/)**

---

## ✨ Kernfunktionen

1. **DACH Lohnnebenkosten-Standards 2026:**
   - **🇩🇪 Deutschland:** AG-Anteile KV, PV, RV, AV (unter Berücksichtigung der Beitragsbemessungsgrenzen 2026: 66.150 € KV/PV und 96.600 € RV/AV) + Umlagen U1/U2/Insolvenzgeldumlage + Berufsgenossenschaft (BG).
   - **🇦🇹 Österreich:** ÖGK SV-Dienstgeberbeitrag (~21,03 %) + FLAF-DB (3,7 %) + DZ (~0,36 %) + Kommunalsteuer (3,0 %) + BVK (1,53 % Abfertigung Neu) auf 14 Monatsgehälter.
   - **🇨🇭 Schweiz:** AHV/IV/EO (5,3 %) + ALV (1,1 % bis 148.200 CHF) + BVG/Pensionskasse + UVG + KTG + FAK.
2. **Effektive Produktivstunden & Interner AG-Stundensatz:**
   - Berechnet die Netto-Anwesenheitstage (abzüglich Urlaub, Feiertage, Krankheit/Weiterbildung) und multipliziert mit dem internen Auslastungsgrad.
3. **Make-or-Buy Break-Even (Festanstellung vs. Freelancer):**
   - Ermittelt die exakte Break-Even-Stundenschwelle pro Jahr gegenüber einem externen Freelancer-Stundensatz.

---

## 📦 Installation & CLI-Nutzung

```bash
pip install -e .
dach-arbeitgeberkosten --country DE --monthly-gross 5500 --bonus 3000 --overhead 6800 --freelancer-rate 95
```

---

## ⚠️ Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG)

Dieses Paket dient ausschließlich der unverbindlichen betriebswirtschaftlichen Personalbudgetierung und Make-or-Buy-Kalkulation. Es stellt keine Lohnsteuer-, Rechts- oder Sozialversicherungsberatung dar.
