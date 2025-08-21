# Options Risk Analytics (Pricing + 1-Day VaR/ES)

Small Python project for options pricing and next day risk.

- Black–Scholes for European options  
- CRR binomial tree (European & American with early exercise)  
- Monte Carlo pricing under GBM  
- 1-day P&L: VaR/ES (95%/99%) on a small portfolio by simulating tomorrow’s spot with GBM (μ≈0), cutting maturity by one day, then re-pricing with Black–Scholes.
