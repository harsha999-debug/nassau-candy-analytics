# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor: An Empirical Business Intelligence & Operations Research Study

**Author:** Harsha Vardhan  
**Program:** Machine Learning Fellowship, Unified Mentor  
**Fellowship ID:** UMID010926107863  
**Domain:** E-commerce & Retail Analytics  
**Date of Submission:** October 2026  

---

## Abstract

In multi-category wholesale distribution networks, gross sales volume is frequently an inaccurate proxy for true financial health. Organizations that optimize solely for top-line revenue risk subsidizing low-margin, cost-heavy products with earnings from high-performing categories. This study presents a rigorous empirical profitability and margin performance analysis of **Nassau Candy Distributor**, evaluating a 24-month transactional dataset comprising 10,194 orders across 15 candy stock-keeping units (SKUs) manufactured at five nationwide facilities. 

Through exploratory data validation, unit economics modeling, 4-quadrant strategic portfolio segmentation, divisional efficiency indexing, and Pareto (80/20) concentration analysis, this study reveals structural operational vulnerabilities:
1. **Severe Portfolio Concentration:** A mere five products (33.3% of SKUs, all from the Chocolate division) generate **95.06% of corporate gross profit** ($88,824.62) and **92.88% of net sales** ($131,692.90).
2. **Hidden Volume Traps & Margin Erosion:** While corporate gross margin stands at an ostensibly healthy **65.91%**, specific lines such as **Kazookles** exhibit a severely compressed gross margin of **7.69%**, where direct manufacturing costs consume 92.3% of revenue.
3. **Divisional Asymmetry:** The Chocolate division functions as a financial powerhouse (1.02x efficiency index), whereas the Other division operates at a margin deficit (0.68x efficiency index), and the high-margin Sugar division (68.10% margin) remains severely under-commercialized (0.25% revenue share).

To operationalize these findings, an interactive Business Intelligence (BI) decision-support dashboard was architected in Streamlit, enabling dynamic threshold simulation, real-time Pareto diagnostics, and automated SKU intervention protocols. Actionable strategic recommendations are formulated across wholesale repricing, supplier contract renegotiation, portfolio rationalization, and supply chain redundancy.

---

## 1. Introduction & Organizational Context

Wholesale and specialty confectionery distribution represents a high-volume, margin-sensitive sector characterized by fluctuating ingredient input costs, seasonal demand spikes, and complex manufacturing networks. Nassau Candy Distributor operates as a regional-to-national distributor sourcing confections from five primary facilities (*Lot's O' Nuts, Wicked Choccy's, Sugar Shack, Secret Factory,* and *The Other Factory*) and delivering across fifty-nine state and provincial territories.

Historically, the organization's commercial strategy has prioritized sales volume expansion under the implicit assumption that top-line revenue growth translates directly to bottom-line profitability. However, distribution businesses frequently encounter the "volume trap"—a scenario in which high-selling items consume disproportionate warehouse handling, freight, and production capacity while delivering negligible gross margins. 

To transition from intuition-based product management to data-driven portfolio optimization, this research establishes an objective analytical framework to quantify SKU-level profitability, evaluate division efficiencies, diagnose cost structures, and assess supply chain vulnerability.

---

## 2. Research Problem Statement & Hypotheses

### 2.1 Problem Statement
Currently, Nassau Candy Distributor lacks visibility into:
1. Which specific products deliver superior gross margins versus those that dilute overall profitability.
2. Whether volume leaders are financially accretive or operationally burdensome.
3. How structural profitability varies across product divisions (*Chocolate*, *Sugar*, *Other*).
4. The degree of corporate reliance on top-performing SKUs (Pareto dependency risk).
5. Which products require immediate repricing, cost renegotiation, or catalog rationalization.

### 2.2 Core Hypotheses
* **Hypothesis 1 ($H_1$):** Top-line sales volume is not uniformly correlated with gross margin efficiency across product lines.
* **Hypothesis 2 ($H_2$):** Corporate profitability is heavily concentrated within a minority subset of products, exposing the firm to single-category supply chain vulnerabilities.
* **Hypothesis 3 ($H_3$):** Certain non-chocolate products exhibit severe manufacturing cost burdens that warrant immediate commercial intervention.

---

## 3. Dataset Description & Exploratory Data Audit

### 3.1 Data Ingestion & Schema Specification
The empirical analysis leverages the official Nassau Candy Distributor historical transaction log spanning 10,194 records. The dataset contains 18 primary attributes:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `Row ID` | Integer | Unique transaction identifier |
| `Order ID` | String | Unique customer order identifier (8,549 distinct orders) |
| `Order Date` | Date | Date transaction was executed (DD-MM-YYYY) |
| `Ship Date` | Date | Target shipment dispatch date (DD-MM-YYYY) |
| `Ship Mode` | String | Logistics class (*Standard Class, Second Class, First Class, Same Day*) |
| `Customer ID` | Integer | Unique wholesale buyer account identifier (5,044 unique buyers) |
| `Country/Region` | String | Destination market (*United States*: 9,994; *Canada*: 200) |
| `City` / `State/Province` | String | Destination municipality and jurisdiction (59 states/provinces, 542 cities) |
| `Region` | String | Geographic market territory (*Pacific, Atlantic, Interior, Gulf*) |
| `Division` | String | Category classification (*Chocolate, Sugar, Other*) |
| `Product ID` | String | Unique SKU identifier (e.g., `CHO-SCR-58000`, `OTH-KAZ-38000`) |
| `Product Name` | String | Complete commercial item name (15 unique products) |
| `Sales` | Float | Gross order transaction value ($) |
| `Units` | Integer | Volume of units ordered per line item |
| `Cost` | Float | Direct manufacturing cost-of-goods-sold ($) |
| `Gross Profit` | Float | Net gross margin value: $\text{Sales} - \text{Cost}$ ($) |

### 3.2 Data Quality & Integrity Validation
Prior to quantitative modeling, an automated data audit was executed via `src/data_cleaning.py`:
1. **Missing Value Audit:** All 10,194 rows and 18 columns contain zero null, blank, or `NaN` cells (100% data completeness).
2. **Mathematical Sanity:** Evaluated the fundamental identity:
   $$\Delta = (\text{Sales} - \text{Cost}) - \text{Gross Profit}$$
   Across all 10,194 observations, the maximum absolute discrepancy was $7.10 \times 10^{-15}$, confirming zero computational inconsistencies.
3. **Non-Negativity Verification:** No records exhibited non-positive sales ($\text{Sales} \le 0$), negative units ($\text{Units} \le 0$), or negative manufacturing costs ($\text{Cost} \le 0$).
4. **Label Harmonization:** Standardized typographical spacing in `"Wonka Bar -Scrumdiddlyumptious"` to `"Wonka Bar - Scrumdiddlyumptious"`. Mapped `"Fizzy Lifting Drinks"` (`OTH-FIZ-56000`) to the *Other* division in accordance with the official project correlation schema.
5. **Temporal Timeline:** Order dates span exactly two calendar years (**January 2, 2024 to December 31, 2025**), representing a continuous operating baseline.

---

## 4. Mathematical Methodology & Metric Formulation

The analytical framework implements five core quantitative formulations:

### 4.1 Unit Economics
For any given product $i$ in transaction $j$:
$$\text{Unit Price}_i = \frac{\text{Sales}_{i,j}}{\text{Units}_{i,j}}$$
$$\text{Unit Cost}_i = \frac{\text{Cost}_{i,j}}{\text{Units}_{i,j}}$$
$$\text{Profit per Unit}_i = \frac{\text{Gross Profit}_{i,j}}{\text{Units}_{i,j}} = \text{Unit Price}_i - \text{Unit Cost}_i$$

### 4.2 Gross Margin Percentage
Gross margin reflects the proportion of revenue retained after direct manufacturing costs:
$$\text{Gross Margin}_i (\%) = \left( \frac{\sum \text{Gross Profit}_i}{\sum \text{Sales}_i} \right) \times 100$$

### 4.3 Portfolio Contribution Shares
$$\text{Revenue Contribution}_i (\%) = \left( \frac{\sum \text{Sales}_i}{\sum_{\text{all } k} \text{Sales}_k} \right) \times 100$$
$$\text{Profit Contribution}_i (\%) = \left( \frac{\sum \text{Gross Profit}_i}{\sum_{\text{all } k} \text{Gross Profit}_k} \right) \times 100$$

### 4.4 Divisional Profit Efficiency Ratio
To measure whether a category generates profit proportionate to its sales scale:
$$\text{Profit Efficiency Index}_d = \frac{\text{Profit Share}_d (\%)}{\text{Revenue Share}_d (\%)} = \frac{\text{Margin}_d}{\text{Corporate Margin}}$$
* $\text{Index} > 1.0$: Value accretive (generates superior profit relative to revenue weight).
* $\text{Index} < 1.0$: Margin dilutive (absorbs revenue volume but reduces overall margin percentage).

### 4.5 Pareto Concentration Formulation
Sorting products in descending order of gross profit, cumulative profit share is computed as:
$$\text{Cumulative Profit Share}_m = \frac{\sum_{i=1}^m \text{Gross Profit}_i}{\sum_{k=1}^N \text{Gross Profit}_k} \times 100$$
Where $N=15$. The cutoff $m^*$ is identified where $\text{Cumulative Profit Share}_{m^*} \ge 80.0\%$.

---

## 5. Empirical Findings: Product-Level Profitability & The 4-Quadrant Matrix

### 5.1 Comprehensive SKU Performance Leaderboard
Aggregation of all 10,194 records reveals marked performance divergence across the 15 candy lines:

| Rank | Product Name | Division | Manufacturing Site | Units | Total Sales ($) | Total Cost ($) | Gross Profit ($) | Gross Margin (%) | Profit Share (%) |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Wonka Bar - Scrumdiddlyumptious | Chocolate | Lot's O' Nuts | 7,743 | \$27,874.80 | \$8,517.30 | **\$19,357.50** | **69.44%** | 20.72% |
| **2** | Wonka Bar - Triple Dazzle Caramel | Chocolate | Wicked Choccy's | 7,596 | \$28,485.00 | \$9,874.80 | **\$18,610.20** | **65.33%** | 19.92% |
| **3** | Wonka Bar - Milk Chocolate | Chocolate | Wicked Choccy's | 8,267 | \$26,867.75 | \$9,424.38 | **\$17,443.37** | **64.92%** | 18.67% |
| **4** | Wonka Bar - Nutty Crunch Surprise | Chocolate | Lot's O' Nuts | 6,755 | \$23,574.95 | \$6,755.00 | **\$16,819.95** | **71.35%** | 18.00% |
| **5** | Wonka Bar - Fudge Mallows | Chocolate | Lot's O' Nuts | 6,914 | \$24,890.40 | \$8,296.80 | **\$16,593.60** | **66.67%** | 17.76% |
| **6** | Lickable Wallpaper | Other | Secret Factory | 393 | \$7,860.00 | \$3,930.00 | **\$3,930.00** | **50.00%** | 4.21% |
| **7** | Wonka Gum | Other | Secret Factory | 478 | \$597.50 | \$286.80 | **\$310.70** | **52.00%** | 0.33% |
| **8** | Everlasting Gobstopper | Sugar | Secret Factory | 13 | \$130.00 | \$26.00 | **\$104.00** | **80.00%** | 0.11% |
| **9** | **Kazookles** | Other | The Other Factory | 371 | \$1,205.75 | \$1,113.00 | **\$92.75** | <mark>**7.69%**</mark> | 0.10% |
| **10** | Hair Toffee | Sugar | The Other Factory | 17 | \$76.50 | \$17.00 | **\$59.50** | **77.78%** | 0.06% |
| **11** | Fizzy Lifting Drinks | Other | Sugar Shack | 21 | \$78.75 | \$31.50 | **\$47.25** | **60.00%** | 0.05% |
| **12** | Laffy Taffy | Sugar | Sugar Shack | 27 | \$53.73 | \$20.25 | **\$33.48** | **62.31%** | 0.04% |
| **13** | SweeTARTS | Sugar | Sugar Shack | 41 | \$61.50 | \$32.80 | **\$28.70** | **46.67%** | 0.03% |
| **14** | Nerds | Sugar | Sugar Shack | 10 | \$15.00 | \$8.00 | **\$7.00** | **46.67%** | 0.01% |
| **15** | Fun Dip | Sugar | Sugar Shack | 8 | \$12.00 | \$7.20 | **\$4.80** | **40.00%** | 0.01% |
| **Total** | **All 15 Products** | — | — | **38,654** | **\$141,783.63** | **\$48,340.83** | **\$93,442.80** | **65.91%** | **100.00%** |

### 5.2 4-Quadrant Strategic Portfolio Segmentation
To convert these empirical measurements into business actions, products are classified into four strategic quadrants using two objective criteria:
* **Margin Benchmark:** 60.0% (Company baseline: 65.91%).
* **Sales Volume Benchmark:** Empirical Median Sales ($1,205.75).

```
                        Gross Margin (%)
                              ▲
                              │
          NICHE               │              WINNERS
      OPPORTUNITIES           │          (Core Assets)
  Everlasting Gobstopper (80%)│   Wonka Nutty Crunch (71.4%)
  Hair Toffee (77.8%)         │   Wonka Scrumdiddly (69.4%)
  Laffy Taffy (62.3%)         │   Wonka Fudge Mallows (66.7%)
  Fizzy Lifting Drinks (60.0%)│   Wonka Triple Dazzle (65.3%)
                              │   Wonka Milk Chocolate (64.9%)
  ── ── ── ── ── ── ── ── ── ─┼── ── ── ── ── ── ── ── ── ─ Margin Benchmark: 60%
                              │
     RATIONALIZATION          │           VOLUME TRAPS
       CANDIDATES             │       (Margin Diluters)
  SweeTARTS (46.7%)           │   Wonka Gum (52.0%)
  Nerds (46.7%)               │   Lickable Wallpaper (50.0%)
  Fun Dip (40.0%)             │   Kazookles (7.69%)  ◄── CRITICAL RISK
                              │
                              └──────────────────────────► Total Sales ($)
                                       Median Sales ($1,205.75)
```

1. **Quadrant 1 — Winners (5 SKUs):** All five Wonka Bar chocolate variants reside here. They generate between \$16.5k and \$19.4k gross profit each, maintaining gross margins between 64.92% and 71.35%.
2. **Quadrant 2 — Volume Traps (3 SKUs):** *Kazookles, Lickable Wallpaper,* and *Wonka Gum*. These achieve above-median sales velocity but dilute profitability with margins below the corporate target.
3. **Quadrant 3 — Niche Opportunities (4 SKUs):** *Everlasting Gobstopper, Hair Toffee, Laffy Taffy,* and *Fizzy Lifting Drinks*. These exhibit excellent margins (60.0% to 80.0%) but suffer from severe distribution deficits (under 30 units sold over 24 months).
4. **Quadrant 4 — Rationalization Candidates (3 SKUs):** *SweeTARTS, Nerds,* and *Fun Dip*. These generate both minimal volume (<45 units) and compressed gross margins (40.0% to 46.7%), making them prime candidates for catalog pruning.

---

## 6. Division-Level Performance & Structural Margin Imbalance

Evaluating operations across product divisions demonstrates profound category distortion:

| Division | Orders | Units Sold | Total Revenue ($) | Gross Profit ($) | Gross Margin (%) | Revenue Share (%) | Profit Share (%) | Profit Efficiency Index |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Chocolate** | 9,844 | 37,275 | \$131,692.90 | \$88,824.62 | **67.45%** | 92.88% | 95.06% | **1.02x** |
| **Other** | 316 | 1,263 | \$9,742.00 | \$4,380.70 | **44.97%** | 6.87% | 4.69% | **0.68x** |
| **Sugar** | 34 | 116 | \$348.73 | \$237.48 | **68.10%** | 0.25% | 0.25% | **1.00x** |

### Key Divisional Insights:
1. **Chocolate Supremacy:** Comprising 96.6% of order volume, Chocolate sustains Nassau Candy's business model. Its efficiency index of 1.02x confirms it produces more profit than its substantial revenue share.
2. **The "Other" Category Drag:** Despite accounting for nearly 7% of net sales, the *Other* division delivers an efficiency index of just 0.68x due to substandard gross margins (44.97%), driven downwards by Kazookles.
3. **Sugar Division Underutilization:** Sugar delivers the highest gross margin of any division (**68.10%**), yet represents merely 34 transactions out of 10,194. This represents an unexploited commercial opportunity.

---

## 7. Profit Concentration & Pareto (80/20) Risk Analysis

A classical Pareto concentration analysis was executed across the product portfolio:

```
Cumulative Gross Profit Contribution (%)
100% ┼─────────────────────────────────────────────────────────────●──●──●
 95% ┼                                                  ● (95.06%)
 90% ┼
 80% ┼ - - - - - - - - - - - - - - - - - - - - - - - - - - - 80% Benchmark
     │                                     ● (77.30%)
 60% ┼                       ● (59.30%)
 40% ┼         ● (40.64%)
 20% ┼  ● (20.72%)
  0% ┼──┴──────────┴───────────┴───────────┴───────────┴───────────┴─────
       Scrumdid   Triple Daz   Milk Choc   Nutty Crunch  Fudge Mallows  Other 10 SKUs
```

### Pareto Analysis Conclusions:
* **80% Profit Threshold:** Just **4 products** (26.7% of catalog) are required to exceed 77.3% of corporate profit; by the 5th product, **95.06% of total company gross profit is accounted for**.
* **Corporate Vulnerability:** A portfolio where 33.3% of SKUs generate 95.1% of profit presents severe supply-chain fragility. Any manufacturing disruption at *Lot's O' Nuts* or *Wicked Choccy's* (which produce these five bars) would immediately jeopardize corporate profitability.

---

## 8. Cost Structure Diagnostics & Pricing Risk: The Kazookles Case Study

A critical objective of this investigation was diagnosing cost structures to uncover pricing inefficiencies.

### 8.1 The Kazookles Anomaly
The most egregious margin risk identified in the catalog is **Kazookles**:
* **Total Sales Revenue:** \$1,205.75 (Rank 7 in Sales)
* **Direct Manufacturing Cost:** \$1,113.00 (Rank 6 in Cost)
* **Net Gross Profit:** **\$92.75** (Rank 9 in Profit)
* **Gross Margin:** **7.69%** (Company average: 65.91%)
* **Unit Economics:**
  * Unit Wholesale Selling Price: **\$3.25**
  * Unit Manufacturing Cost: **\$3.00**
  * Net Gross Profit per Unit: **\$0.25**

```
Unit Price Breakdown ($/unit)
Kazookles:          [═══════════════════════════════════ Cost: $3.00 (92.3%) ═══════════════════════════════════][ Profit: $0.25 (7.7%) ]  = $3.25
Wonka Nutty Crunch: [════ Cost: $1.00 (28.7%) ════][═══════════════════ Profit: $2.49 (71.3%) ═══════════════════]                        = $3.49
```

### 8.2 Diagnostic Assessment
Kazookles is manufactured at *The Other Factory*. Direct manufacturing cost consumes **92.3% of wholesale revenue**. A modest 8.5% increase in packaging, raw sugar, or freight would render this product directly cash-negative. Nassau Candy is effectively utilizing working capital and warehousing capacity to distribute Kazookles at breakeven.

---

## 9. Temporal Margin Dynamics & Portfolio Mix Shifts

Analysis of transactional timelines across 2024 and 2025 demonstrates distinct commercial dynamics:
1. **SKU Price & Cost Rigidity:** Unit selling prices and unit manufacturing costs are fixed across the entire historical period. No price escalation or cost variance occurred within individual SKUs.
2. **Portfolio Mix-Driven Margin Volatility:** Because unit margins are constant, company-wide gross margin fluctuates month-to-month strictly as a function of **product mix shift**:
   * Minimum Monthly Margin: **64.54%** (March 2024)
   * Maximum Monthly Margin: **66.75%** (November 2025)
   * Monthly Standard Deviation: **0.53%**
3. **Seasonal Volume Trends:** Order volume follows classic confectionery holiday seasonality:
   * **Q1 Baseline:** January–February represent low-order months (\$1.3k to \$2.1k monthly sales).
   * **Autumn Surge:** September orders surge to \$7.9k (Halloween wholesale stocking).
   * **Holiday Peak:** November and December represent peak velocity (\$8.9k each, Thanksgiving & Christmas distribution).

---

## 10. Strategic Business Recommendations

Based on empirical modeling, Nassau Candy Distributor should implement a four-pillar operational restructuring program:

### Pillar 1: Targeted Wholesale Repricing & Sourcing Interventions
* **Reprice Kazookles Immediately:** Adjust wholesale list price from \$3.25 to **\$4.50 per unit**. At a \$3.00 unit cost, this elevates gross margin from **7.69% to 33.33%**, transforming it from a margin drain into a viable line.
* **Supplier Renegotiation with The Other Factory:** Audit production efficiencies at *The Other Factory* to target a 20% reduction in unit cost (from \$3.00 to \$2.40).

### Pillar 2: Promotional Discipline for Volume Traps
* **Lickable Wallpaper (\$20.00 price, \$10.00 cost, 50.0% margin):** Eliminate off-invoice discounting. Establish strict minimum advertised pricing (MAP) to protect its \$10.00/unit profit contribution.
* **Wonka Gum (\$1.25 price, \$0.60 cost, 52.0% margin):** Restructure into multi-pack wholesale cartons to reduce per-unit picking and logistics handling expenses.

### Pillar 3: Catalog Pruning & Minimum Order Quantities (MOQs)
* **Rationalize Sugar Laggards:** *SweeTARTS* (\$61.50 sales), *Nerds* (\$15.00 sales), and *Fun Dip* (\$12.00 sales) collectively generated under \$90 in sales over two years while tying up SKU slots and catalog administration.
* **Action:** Institute a minimum order quantity (MOQ) of 25 cases or discontinue individual SKU distribution in favor of a unified "Sugar Variety Sampler Pack".

### Pillar 4: Commercial Expansion of High-Margin Niches
* **Scale Everlasting Gobstopper & Hair Toffee:** Everlasting Gobstopper boasts an **80.00% gross margin** (\$8.00 profit/unit) and Hair Toffee boasts **77.78%** (\$3.50 profit/unit). Both lines suffer from chronic under-distribution (<20 units sold).
* **Action:** Deploy sales rep incentives and bundled promotional placement with Wonka Chocolate orders to expand retail penetration.

---

## 11. Interactive Decision Support System (Streamlit BI Architecture)

To ensure continuous executive oversight, the analytical engine was operationalized into a production-grade Streamlit application (`app.py`):

```
┌────────────────────────────────────────────────────────────────────────┐
│                        NASSAU CANDY DISTRIBUTOR                        │
│             Executive Profitability & Margin Analytics Portal          │
├────────────────────────────────┬───────────────────────────────────────┤
│ SIDEBAR CONTROLS               │ TOP KPI EXECUTIVE SUMMARY             │
│ • Date Range Picker            │ • Total Revenue: $141,783.63          │
│ • Division Multi-Select        │ • Gross Profit:  $93,442.80           │
│ • Margin Target Benchmark (60%)│ • Gross Margin:  65.91%               │
│ • Real-time SKU Search Box     │ • Cost of Goods: $48,340.83           │
│ • Reset All Filters Button     │ • Units Sold:    38,654               │
├────────────────────────────────┴───────────────────────────────────────┤
│ FIVE SPECIALIZED ANALYTICAL MODULES (TABS)                             │
│ 1. 📊 Product Profitability & 4-Quadrant Strategic Portfolio Matrix    │
│ 2. 🏢 Division Performance & Profit Efficiency Index (Grouped Bars)    │
│ 3. ⚠️ Cost Diagnostics, Unit Economics & Dynamic Strategic Risk Cards   │
│ 4. 📈 Profit Concentration & Pareto (80/20) Dual-Axis Curve            │
│ 5. 🏭 Factory & Supply Chain Intelligence (US Geospatial Facility Map) │
├────────────────────────────────────────────────────────────────────────┤
│ EXPORT ENGINE: On-Demand Filtered Transaction Dataset Download (CSV)   │
└────────────────────────────────────────────────────────────────────────┘
```

The system features auto-padded scaling, linear/logarithmic toggles, interactive Plotly tooltips, and dynamic alert cards that adapt in real time to managerial parameter adjustments.

---

## 12. Conclusion & Operational Roadmap

This empirical investigation disproves the premise that sales volume corresponds reliably with gross margin performance at Nassau Candy Distributor. By uncovering that five chocolate products account for 95% of corporate profitability while lines like Kazookles operate at 7.7% margin, this research provides the executive committee with actionable intelligence to reprice, renegotiate, and rebalance the corporate portfolio.

Executing the recommended interventions will protect core chocolate revenue lines, eliminate margin diluters, scale high-margin niche candies, and enhance the firm's long-term commercial resilience.

---

## References & Author Statement

1. **Analytical Dataset:** Nassau Candy Distributor Historical Confectionery Wholesale Log (10,194 records, Jan 2024 – Dec 2025).
2. **Codebase Implementation:** Python 3.12, Pandas 3.0.6, Plotly 7.1.0, Streamlit 1.65.0.
3. **Repository Architecture:** Hosted locally at `Nassau Candy Distributor project/`.
4. **Author Statement:** This study was authored by Harsha Vardhan as part of the Unified Mentor Machine Learning Fellowship capstone submission. All data transformations, metrics, visualizations, and documentation reflect original analytical work.
