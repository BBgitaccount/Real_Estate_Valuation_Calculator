# 🏠 Real Estate Valuation & Opportunity Cost Calculator

![photo.jpg](photo.jpg)

A Python command-line tool that evaluates whether a real estate investment is financially rational by comparing its **inflation-adjusted real value** against its asking price and the opportunity cost of an alternative bank investment.

---

## 📌 What It Does

This tool helps you answer a simple but critical question:

> *Is the property worth what they're asking — in real, inflation-adjusted terms?*

It does so in four steps:

1. Calculates the **net rental income** after tax
2. Discounts all future cash flows back to **today's real value** using the Fisher-adjusted rate
3. Computes the **opportunity cost** of putting that money in a bank instead
4. Outputs a clear **LOGICAL / ILLOGICAL** verdict on the investment

---

## 📥 Inputs

| Parameter                 | Description                                                   |
| ------------------------- | ------------------------------------------------------------- |
| Current asking price      | The price the property is listed at today                     |
| Holding period (years)    | How long you plan to keep the property                        |
| Target future sale price  | The price you expect to sell for at the end                   |
| Monthly rental income     | Expected monthly rent                                         |
| Nominal discount rate (%) | Your required rate of return / bank interest rate             |
| Inflation rate (%)        | Expected average annual inflation                             |
| Rental tax rate (%)       | Tax on rental income (only if rent > 450 exemption threshold) |

---

## 🧮 Core Formulas

### Step 1 — Real Discount Rate (Fisher Equation)

Converts the nominal interest rate into a real rate that accounts for inflation:

Where `i` is the annual inflation rate.

---

### Step 2 — Net Annual Rent

```
Annual Rent    = Monthly Rent × 12
Rent Tax       = Annual Rent × (tax_rate / 100)
K_net          = Annual Rent − Rent Tax
```

> If monthly rent is below the `TAX_EXEMPTION_THRESHOLD` (450), tax rate is automatically set to 0%.

---

### Step 3 — Total Real Value of the Property

This is the **main formula** of the model. It computes the inflation-adjusted present value of all future cash flows:

$$V_{\text{real}} = \underbrace{\sum_{t=1}^{n} \frac{K_{\text{net}}}{\left(1 + r_{\text{real}}\right)^{t}}}*{\text{Present value of rents}} + \underbrace{\frac{FV*{\text{sale}}}{\left(1 + r_{\text{real}}\right)^{n}}}_{\text{Present value of future sale}}$$

Where:

- `n` = holding period in years
- `K_net` = net annual rental income (after tax)
- `FV_sale` = target future sale price
- `r_real` = real discount rate (from Fisher equation)

The first term is an **annuity series** — each year's rent is discounted separately and summed. The second term discounts the lump-sum sale price back to today.

---

### Step 4 — Opportunity Cost (Bank Alternative)

What would happen if you invested the same amount in a bank instead?

$$FV_{\text{bank}} = P_{\text{asking}} \times (1 + r_{\text{nominal}})^{n}$$

$$\text{Net Interest} = FV_{\text{bank}} - P_{\text{asking}}$$

---

### Decision Rule

```
IF  asking_price ≤ V_real  →  ✅ LOGICAL   (property is worth at least what they ask)
IF  asking_price >  V_real  →  ❌ ILLOGICAL (you're overpaying in real terms)
```

---

## 🚀 How to Run

No external libraries required — pure Python standard library.

```bash
python valuation.py
```

Follow the prompts. All inputs are validated; entering a non-numeric value will prompt you to try again.

---

## 📁 Project Structure

```
.
└── valuation.py       # Main script (single file, no dependencies)
```

---

## 💡 Key Concepts

**Why use the Fisher Equation?** Nominal rates include inflation. If you discount future cash flows with a nominal rate, you're comparing inflated future dollars against today's prices — an unfair comparison. The Fisher equation strips out inflation so all values are expressed in the same real purchasing power.

**Why discount each rent year separately?** A sum received next year is worth more than the same sum received in 10 years. The annuity series (Σ) handles this by applying a progressively larger discount for each future year.

**What is opportunity cost here?** It's the theoretical return you *give up* by choosing real estate over a risk-free bank deposit. If the bank offers more, the property investment needs strong appreciation or rental yield to justify the risk.

---

## ⚙️ Configuration

One constant can be adjusted at the top of the script:

```python
TAX_EXEMPTION_THRESHOLD = 450.0  # Monthly rent below this is tax-exempt
```


