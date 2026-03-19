TAX_EXEMPTION_THRESHOLD = 450.0

def get_float_input(prompt: str, default: float = None) -> float:
    """Safely retrieves and validates numerical user input."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input and default is not None:
                return default
            return float(user_input)
        except ValueError:
            print("Input error: Please enter a valid numerical value.")

def calculate_investment_metrics(
    holding_period: int,
    future_sale_price: float,
    monthly_rent: float,
    nominal_discount_rate: float,
    inflation_rate: float,
    tax_rate: float
) -> tuple:
    """Calculates all nominal and inflation-adjusted (real) metrics for the property."""
    # Fisher Equation for Real Discount Rate
    real_discount_rate = (nominal_discount_rate - inflation_rate) / (1 + inflation_rate)

    annual_rent_income = monthly_rent * 12.0
    annual_rent_tax = annual_rent_income * (tax_rate / 100.0)
    net_annual_rent = annual_rent_income - annual_rent_tax

    # Total Nominal Rent
    total_nominal_net_rent = net_annual_rent * holding_period

    # Real Present Value (RPV) of the sale
    present_value_of_sale = future_sale_price / (1 + real_discount_rate) ** holding_period

    # Real Present Value (RPV) of the rents
    total_present_value_of_rent = sum(
        net_annual_rent / (1 + real_discount_rate) ** year
        for year in range(1, holding_period + 1)
    )

    total_real_value = total_present_value_of_rent + present_value_of_sale

    return total_nominal_net_rent, total_present_value_of_rent, present_value_of_sale, total_real_value

def main() -> None:
    print("--- Comprehensive Real Estate Valuation & Opportunity Cost ---")

    current_asking_price = get_float_input("Current asking price of the property: ")
    holding_period = int(get_float_input("Holding period (years): "))
    future_sale_price = get_float_input("Target future sale price: ")
    monthly_rent = get_float_input("Expected monthly rental income: ")

    nominal_discount_rate = get_float_input("Nominal Interest/Discount Rate (%) (e.g., 15): ") / 100.0
    inflation_rate = get_float_input("Expected Annual Inflation Rate (%) (e.g., 10): ") / 100.0

    tax_rate = 0.0
    if monthly_rent > TAX_EXEMPTION_THRESHOLD:
        tax_rate = get_float_input(
            "Rental Income Tax Rate (%) [Press Enter for default 15%]: ",
            default=15.0
        )

    # 1. Process Real Estate Metrics
    metrics = calculate_investment_metrics(
        holding_period,
        future_sale_price,
        monthly_rent,
        nominal_discount_rate,
        inflation_rate,
        tax_rate
    )
    total_nominal_net_rent, pv_rents, pv_sale, total_real_property_value = metrics

    # 2. Alternative Investment (Opportunity Cost) Calculation
    alternative_future_value = current_asking_price * (1 + nominal_discount_rate) ** holding_period
    alternative_interest_gained = alternative_future_value - current_asking_price

    # 3. Output Generation
    print("\n" + "="*50)
    print("1. NOMINAL CASH FLOWS (Unadjusted for Inflation)")
    print("="*50)
    print(f"Total Net Rental Income ({holding_period} years): {total_nominal_net_rent:,.2f}")
    print(f"Target Future Sale Price:               {future_sale_price:,.2f}")

    print("\n" + "="*50)
    print("2. INFLATION-ADJUSTED PRESENT VALUES (Real Value Today)")
    print("="*50)
    print(f"Present Value of Total Rents:           {pv_rents:,.2f}")
    print(f"Present Value of Future Sale:           {pv_sale:,.2f}")
    print(f"TOTAL REAL VALUE OF PROPERTY:           {total_real_property_value:,.2f}")

    print("\n" + "="*50)
    print("3. OPPORTUNITY COST (Bank Interest Alternative)")
    print("="*50)
    print(f"Total Future Value if invested in Bank: {alternative_future_value:,.2f}")
    print(f"Net Interest Income Gained:             {alternative_interest_gained:,.2f}")

    print("\n" + "="*50)
    print("4. STRATEGIC ANALYSIS")
    print("="*50)
    if current_asking_price <= total_real_property_value:
        print("ANALYSIS: LOGICAL. (Asking price <= Total Real Value of the property)")
    else:
        print("ANALYSIS: ILLOGICAL. (Asking price > Total Real Value of the property)")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()