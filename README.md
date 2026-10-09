# Product Line Profitability & Margin Performance Analysis
## Nassau Candy Distributor — Executive Business Intelligence Dashboard

**Author:** Harsha Vardhan  
**Fellowship ID:** UMID010926107863  
**Organization:** Unified Mentor Machine Learning & Data Analytics Fellowship  
**Domain:** E-commerce & Retail Analytics  

---

### 📌 Project Overview
This project addresses the "volume trap" in wholesale distribution. By auditing **10,194 historical orders** across 15 candy products and 5 nationwide manufacturing facilities, this interactive BI platform identifies which products and divisions truly drive corporate profits versus those that dilute operating margins.

### 🎯 Key Business Findings
- **Financial Baseline:** $141,783.63 Gross Revenue, $93,442.80 Gross Profit (65.91% Corporate Margin).
- **Extreme Profit Concentration (Pareto Risk):** Just 5 chocolate products account for **95.06% of total company profit** ($88,824.62) and are concentrated at only two factories (*Lot's O' Nuts* and *Wicked Choccy's*).
- **Volume Trap Discovered:** **Kazookles** sells for $3.25 with a $3.00 manufacturing cost, yielding an unsustainable **7.69% gross margin** (direct costs consume 92.3% of revenue).
- **Divisional Asymmetry:** Chocolate generates 95.1% of profit (1.02x efficiency index), whereas Other acts as a drag (0.68x efficiency index), and Sugar is under-commercialized (68.10% margin, but only 0.25% revenue share).

### 🚀 Interactive Dashboard Features (`app.py`)
1. **Executive KPI Scorecard:** Real-time top-line metrics and baseline health status.
2. **Product Profitability & 4-Quadrant Strategic Matrix:** Segmenting SKUs into *Winners, Volume Traps, Niche Opportunities,* and *Rationalization Candidates* with dynamic axes and Linear/Logarithmic scaling.
3. **Division Performance:** Revenue vs. profit imbalance and category margin distributions.
4. **Cost vs. Margin Diagnostics:** SKU-level cost scatter plot and automated unit-economics intervention alerts.
5. **Pareto (80/20) Concentration:** Cumulative profit curve tracking single-category vulnerability.
6. **Nationwide Supply Chain Mapping:** Production breakdown across all 5 manufacturing facilities.

### 🛠️ Local Installation & Run
```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit Web Application
streamlit run app.py
```
