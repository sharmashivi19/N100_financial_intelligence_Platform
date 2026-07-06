# Sprint 2 Retrospective

## Completed

- Profitability Ratios
- Leverage Ratios
- CAGR Engine
- Cash Flow KPIs
- Financial Ratios Table
- Edge Case Logging

## Formula Decisions

- Return None when denominator is zero
- Return None for negative equity
- Debt-free companies return D/E = 0
- Interest = 0 returns ICR = None
- CAGR handles turnaround, decline-to-loss and zero-base separately

## Edge Cases

- Negative Equity
- Zero Sales
- Zero Assets
- Zero Interest
- Debt Free Companies
- CAGR Turnaround
- Zero Base CAGR

## Issues

- companies table does not contain company_id
- Financial sector mapping unavailable
- ROE/ROCE comparison limited by available schema

## Sprint Outcome

Successfully implemented the financial ratio engine and populated the financial_ratios SQLite table.