import logging


logging.basicConfig(
    level=logging.INFO
)


logger = logging.getLogger(__name__)


# ---------------------------------
# Net Profit Margin
# ---------------------------------

def net_profit_margin(net_profit, sales):

    if sales is None:
        return None

    if sales == 0:
        return None

    return (net_profit / sales) * 100



# ---------------------------------
# Operating Profit Margin
# ---------------------------------

def operating_profit_margin(
        operating_profit,
        sales,
        reported_opm=None
):

    if sales is None or sales == 0:
        return None


    calculated_opm = (
        operating_profit / sales
    ) * 100


    if reported_opm is not None:

        difference = abs(
            calculated_opm - reported_opm
        )


        if difference > 1:

            logger.warning(
                f"OPM mismatch detected. "
                f"Calculated={calculated_opm:.2f}, "
                f"Reported={reported_opm:.2f}"
            )


    return round(calculated_opm,2)




# ---------------------------------
# Return On Equity
# ---------------------------------

def return_on_equity(
        net_profit,
        equity_capital,
        reserves
):

    if equity_capital is None:
        return None

    if reserves is None:
        return None


    equity = (
        equity_capital + reserves
    )


    # negative equity handling

    if equity <= 0:
        return None


    return (
        net_profit / equity
    ) * 100




# ---------------------------------
# Return On Capital Employed
# ---------------------------------

def return_on_capital_employed(
        ebit,
        equity,
        reserves,
        borrowings
):

    if None in [
        equity,
        reserves,
        borrowings
    ]:
        return None


    capital = (
        equity +
        reserves +
        borrowings
    )


    if capital <= 0:
        return None


    return (
        ebit / capital
    ) * 100





# ---------------------------------
# Return On Assets
# ---------------------------------

def return_on_assets(
        net_profit,
        total_assets
):

    if total_assets is None:
        return None


    if total_assets == 0:
        return None


    return (
        net_profit /
        total_assets
    ) * 100
def debt_to_equity(
        borrowings,
        equity_capital,
        reserves
):

    if borrowings == 0:
        return 0


    if equity_capital is None or reserves is None:
        return None


    equity = equity_capital + reserves


    if equity <= 0:
        return None


    return borrowings / equity
def high_leverage_flag(
        debt_equity,
        sector
):

    if debt_equity is None:
        return False


    if (
        debt_equity > 5
        and sector != "Financials"
    ):
        return True


    return False
def interest_coverage_ratio(
        operating_profit,
        other_income,
        interest
):

    if interest == 0:
        return None


    if interest is None:
        return None


    return (
        operating_profit +
        other_income
    ) / interest
def icr_label(icr):

    if icr is None:
        return "Debt Free"

    return None
def icr_warning_flag(icr):

    if icr is None:
        return False


    if icr < 1.5:
        return True


    return False
def net_debt(
        borrowings,
        investments
):

    if investments is None:
        investments = 0


    return borrowings - investments
def net_debt(
        borrowings,
        investments
):

    if investments is None:
        investments = 0


    return borrowings - investments
def asset_turnover(sales, total_assets):
    """
    Asset Turnover Ratio

    Formula:
    Sales / Total Assets

    Returns:
        None if total_assets = 0
    """

    if total_assets == 0:
        return None

    return sales / total_assets