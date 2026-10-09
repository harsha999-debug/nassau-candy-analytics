"""
Nassau Candy Distributor - Product Line Profitability & Margin Performance Dashboard
Executive Business Intelligence & Margin Analytics System
Author: Harsha Vardhan & Antigravity Assistant
Tech Stack: Python, Streamlit, Pandas, Plotly Express & Graph Objects
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & EXECUTIVE THEME
# ==============================================================================
st.set_page_config(
    page_title="Nassau Candy - Profitability & Margin Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for executive dashboard styling & clean typography
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    
    /* Executive Metric Cards */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-container:hover {
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08);
    }
    .metric-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 4px;
    }
    .metric-number {
        font-size: 1.7rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .metric-caption {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    /* Alert & Recommendation Cards (Clean HTML, No raw Markdown) */
    .rec-card {
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-left: 4px solid;
    }
    .rec-critical {
        background-color: #FEF2F2;
        border-color: #EF4444;
        color: #991B1B;
    }
    .rec-warning {
        background-color: #FFFBEB;
        border-color: #F59E0B;
        color: #92400E;
    }
    .rec-success {
        background-color: #F0FDF4;
        border-color: #10B981;
        color: #166534;
    }
    .rec-info {
        background-color: #EFF6FF;
        border-color: #3B82F6;
        color: #1E40AF;
    }
    .rec-header {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }
    .rec-body {
        font-size: 0.85rem;
        line-height: 1.45;
    }

    /* Filter Badge */
    .filter-chip {
        display: inline-block;
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.78rem;
        color: #334155;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)


import os

# ==============================================================================
# 2. DATA INGESTION & ROBUST CACHING
# ==============================================================================
@st.cache_data
def load_data():
    data_path = "clean_candy_sales.csv" if os.path.exists("clean_candy_sales.csv") else "data/processed/clean_candy_sales.csv"
    df = pd.read_csv(data_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

df_raw = load_data()


# ==============================================================================
# 3. SIDEBAR CONTROLS & DYNAMIC FILTERING
# ==============================================================================
st.sidebar.markdown("### 🍬 Nassau Candy Analytics")
st.sidebar.caption("Executive Decision Support System")
st.sidebar.markdown("---")

# Quick Reset Mechanism
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("#### 📅 1. Order Timeline")
min_date = df_raw['Order Date'].min().date()
max_date = df_raw['Order Date'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    label_visibility="collapsed"
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

st.sidebar.markdown("#### 🏢 2. Product Divisions")
all_divisions = sorted(df_raw['Division'].unique().tolist())
selected_divisions = st.sidebar.multiselect(
    "Select Divisions",
    options=all_divisions,
    default=all_divisions,
    label_visibility="collapsed"
)

st.sidebar.markdown("#### 🎯 3. Margin Target Benchmark")
margin_threshold = st.sidebar.slider(
    "Gross Margin Benchmark (%)",
    min_value=10.0,
    max_value=90.0,
    value=60.0,
    step=2.5,
    help="Target gross margin percentage. Used to classify Winners vs Volume Traps and trigger margin-risk alerts."
)

st.sidebar.markdown("#### 🔍 4. Product SKU Search")
search_query = st.sidebar.text_input(
    "Search Candy Product",
    placeholder="Type product name...",
    label_visibility="collapsed"
).strip().lower()

# Apply Filters Strictly
filtered_df = df_raw[
    (df_raw['Order Date'].dt.date >= start_date) &
    (df_raw['Order Date'].dt.date <= end_date) &
    (df_raw['Division'].isin(selected_divisions))
]

if search_query:
    filtered_df = filtered_df[filtered_df['Product Name'].str.lower().str.contains(search_query)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Active Filter Records: **{len(filtered_df):,}** / {len(df_raw):,}")


# ==============================================================================
# 4. TOP EXECUTIVE KPI SUMMARY
# ==============================================================================
st.markdown('<div class="main-header">Nassau Candy Distributor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Product Line Profitability, Margin Performance & Portfolio Strategy Dashboard</div>', unsafe_allow_html=True)

# Active Filter Chips
filter_info = f"<span class='filter-chip'>📅 {start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}</span>"
filter_info += f"<span class='filter-chip'>🏢 Divisions: {', '.join(selected_divisions) if selected_divisions else 'None'}</span>"
filter_info += f"<span class='filter-chip'>🎯 Margin Benchmark: {margin_threshold:.1f}%</span>"
if search_query:
    filter_info += f"<span class='filter-chip'>🔍 Search: '{search_query}'</span>"
st.markdown(filter_info, unsafe_allow_html=True)
st.write("")

if filtered_df.empty:
    st.warning("⚠️ No records match your selected filter criteria. Please broaden your date range or division selection.")
    st.stop()

# Exact Financial Calculations
total_sales = float(filtered_df['Sales'].sum())
total_cost = float(filtered_df['Cost'].sum())
total_profit = float(filtered_df['Gross Profit'].sum())
total_units = int(filtered_df['Units'].sum())
total_orders = int(filtered_df['Order ID'].nunique())
overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-number">${total_sales:,.2f}</div>
        <div class="metric-caption">{total_orders:,} unique orders</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Gross Profit</div>
        <div class="metric-number" style="color: #10B981;">${total_profit:,.2f}</div>
        <div class="metric-caption">${(total_profit / total_units):.2f} avg profit/unit</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    margin_color = "#10B981" if overall_margin >= margin_threshold else "#EF4444"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Overall Gross Margin</div>
        <div class="metric-number" style="color: {margin_color};">{overall_margin:.2f}%</div>
        <div class="metric-caption">Target: {margin_threshold:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    cost_ratio = (total_cost / total_sales * 100) if total_sales > 0 else 0.0
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Manufacturing Cost</div>
        <div class="metric-number" style="color: #F97316;">${total_cost:,.2f}</div>
        <div class="metric-caption">{cost_ratio:.1f}% of gross revenue</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">Total Units Sold</div>
        <div class="metric-number">{total_units:,}</div>
        <div class="metric-caption">{filtered_df['Product Name'].nunique()} active SKUs</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ==============================================================================
# 5. PRODUCT AGGREGATION & STRATEGIC QUADRANT MATRIX LOGIC
# ==============================================================================
prod_summary = filtered_df.groupby(['Division', 'Product ID', 'Product Name', 'Factory']).agg(
    orders=('Order ID', 'count'),
    units=('Units', 'sum'),
    sales=('Sales', 'sum'),
    cost=('Cost', 'sum'),
    profit=('Gross Profit', 'sum')
).reset_index()

# Accurate Per-Product Metrics
prod_summary['gross_margin_pct'] = np.where(
    prod_summary['sales'] > 0,
    (prod_summary['profit'] / prod_summary['sales'] * 100).round(2),
    0.0
)
prod_summary['unit_price'] = np.where(
    prod_summary['units'] > 0,
    (prod_summary['sales'] / prod_summary['units']).round(2),
    0.0
)
prod_summary['unit_cost'] = np.where(
    prod_summary['units'] > 0,
    (prod_summary['cost'] / prod_summary['units']).round(2),
    0.0
)
prod_summary['profit_per_unit'] = np.where(
    prod_summary['units'] > 0,
    (prod_summary['profit'] / prod_summary['units']).round(2),
    0.0
)
prod_summary['profit_share_pct'] = (prod_summary['profit'] / total_profit * 100).round(2)
prod_summary['revenue_share_pct'] = (prod_summary['sales'] / total_sales * 100).round(2)

# Transparent, Defensible Thresholds for the 4-Quadrant Matrix
# Sales threshold: Median of active filtered products ensures balanced categorization
sales_benchmark = float(prod_summary['sales'].median()) if not prod_summary.empty else 0.0

def assign_strategic_quadrant(row):
    high_margin = row['gross_margin_pct'] >= margin_threshold
    high_sales = row['sales'] >= sales_benchmark

    if high_margin and high_sales:
        return "Winners (High Sales & High Margin)"
    elif not high_margin and high_sales:
        return "Volume Traps (High Sales & Low Margin)"
    elif high_margin and not high_sales:
        return "Niche Opportunities (Low Sales & High Margin)"
    else:
        return "Rationalization Candidates (Low Sales & Low Margin)"

prod_summary['quadrant'] = prod_summary.apply(assign_strategic_quadrant, axis=1)

# Dynamic, Data-Grounded Recommendations (No Hard-coding)
def generate_sku_recommendation(row):
    margin = row['gross_margin_pct']
    price = row['unit_price']
    cost = row['unit_cost']
    units = row['units']
    quad = row['quadrant']
    cost_pct = (cost / price * 100) if price > 0 else 0.0

    if cost_pct > 75.0 or margin < 30.0:
        return {
            "level": "critical",
            "title": f"🚨 Critical Margin Risk — {row['Product Name']}",
            "finding": f"Severe manufacturing cost burden: Unit cost is ${cost:.2f} on a ${price:.2f} price ({cost_pct:.1f}% cost-of-goods), yielding only a {margin:.1f}% margin and ${row['profit_per_unit']:.2f} profit/unit.",
            "action": "Immediate Action: Renegotiate supplier contract with manufacturing facility or enact an immediate wholesale price increase."
        }
    elif quad == "Volume Traps (High Sales & Low Margin)":
        return {
            "level": "warning",
            "title": f"⚠️ Volume Trap — {row['Product Name']}",
            "finding": f"High sales volume (${row['sales']:,.2f}) but margin of {margin:.1f}% falls below the {margin_threshold:.1f}% target benchmark.",
            "action": "Margin Optimization: Restructure promotional discounts and evaluate tiered wholesale contract terms."
        }
    elif quad == "Rationalization Candidates (Low Sales & Low Margin)":
        return {
            "level": "warning",
            "title": f"⚠️ Portfolio Review Needed — {row['Product Name']}",
            "finding": f"Low customer demand ({units:,} units) paired with compressed margin ({margin:.1f}%).",
            "action": "Portfolio Rationalization: Evaluate catalog continuation, minimum order quantities (MOQ), or product bundling."
        }
    elif quad == "Niche Opportunities (Low Sales & High Margin)":
        return {
            "level": "info",
            "title": f"💡 Niche Growth Target — {row['Product Name']}",
            "finding": f"Highly lucrative unit economics ({margin:.1f}% gross margin, ${row['profit_per_unit']:.2f} profit/unit) but under-distributed ({units:,} units sold).",
            "action": "Growth Initiative: Expand retail placement and channel marketing to scale unit volume."
        }
    else:
        return {
            "level": "success",
            "title": f"✅ Core Profit Engine — {row['Product Name']}",
            "finding": f"Exceptional health: Delivers {margin:.1f}% gross margin with high volume (${row['sales']:,.2f} revenue, {units:,} units).",
            "action": "Asset Protection: Secure manufacturing plant capacity and protect raw material supply lines."
        }

prod_summary['rec_data'] = prod_summary.apply(generate_sku_recommendation, axis=1)

# Sort by gross profit descending
prod_summary = prod_summary.sort_values('profit', ascending=False).reset_index(drop=True)
prod_summary['rank'] = prod_summary.index + 1


# ==============================================================================
# 6. DASHBOARD MODULE TABS
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Product Profitability & Matrix",
    "🏢 Division Performance",
    "⚠️ Cost Diagnostics & Risk Flags",
    "📈 Profit Concentration (Pareto)",
    "🏭 Factory & Supply Chain"
])

# ------------------------------------------------------------------------------
# TAB 1: PRODUCT PROFITABILITY OVERVIEW & 4-QUADRANT MATRIX
# ------------------------------------------------------------------------------
with tab1:
    st.markdown("### Product Profitability Leaderboard & Strategic Matrix")
    st.caption("Detailed ranking of product lines by gross profit contribution, unit margins, and portfolio quadrant positioning.")

    col_t1, col_t2 = st.columns([3, 2])

    with col_t1:
        st.markdown("##### 🏆 Product Margin Leaderboard")
        leaderboard_cols = [
            'rank', 'Product Name', 'Division', 'units', 'sales', 'profit',
            'gross_margin_pct', 'profit_per_unit', 'quadrant'
        ]
        lb_display = prod_summary[leaderboard_cols].copy()
        lb_display.columns = [
            'Rank', 'Product Name', 'Division', 'Units', 'Sales ($)',
            'Gross Profit ($)', 'Margin (%)', 'Profit/Unit ($)', 'Quadrant'
        ]

        # Resilient styling
        styled_lb = lb_display.style.format({
            'Sales ($)': '${:,.2f}',
            'Gross Profit ($)': '${:,.2f}',
            'Margin (%)': '{:.2f}%',
            'Profit/Unit ($)': '${:.2f}',
            'Units': '{:,}'
        })
        try:
            styled_lb = styled_lb.background_gradient(subset=['Margin (%)'], cmap='Greens', vmin=30, vmax=80)
        except Exception:
            pass

        st.dataframe(styled_lb, use_container_width=True, height=380)

    with col_t2:
        st.markdown("##### 🍰 Gross Profit Contribution Share")
        fig_donut = px.pie(
            prod_summary.head(8),
            names='Product Name',
            values='profit',
            hole=0.48,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Gross Profit: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
        )
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            height=380
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # --------------------------------------------------------------------------
    # 4-QUADRANT STRATEGIC PRODUCT PORTFOLIO MATRIX (FULLY AUDITED & RESOLVED)
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 4-Quadrant Strategic Product Portfolio Matrix")
    st.caption(
        f"Plots actual **Gross Margin (%)** vs. actual **Total Sales ($)** for all {len(prod_summary)} active products. "
        f"Quadrants are split by **Margin Benchmark ({margin_threshold:.1f}%)** on Y-axis and **Median Sales (${sales_benchmark:,.2f})** on X-axis."
    )

    # Scale Toggle for Enhanced Usability (Allows inspecting low-volume SKUs without clustering)
    scale_col1, scale_col2 = st.columns([3, 1])
    with scale_col2:
        x_scale_choice = st.radio(
            "X-Axis Scale",
            options=["Linear Scale", "Logarithmic Scale (Expand Low-Sales SKUs)"],
            horizontal=False,
            label_visibility="collapsed"
        )
    is_log = "Logarithmic" in x_scale_choice

    # Calculate bubble sizing: ensure min 10px so small volume SKUs (e.g. 8 units) are distinctly visible
    # We apply sqrt transformation for marker sizing to avoid sub-pixel rendering
    min_units = max(1, prod_summary['units'].min())
    max_units = max(min_units + 1, prod_summary['units'].max())
    norm_sizes = 10 + 26 * ((np.sqrt(prod_summary['units']) - np.sqrt(min_units)) / (np.sqrt(max_units) - np.sqrt(min_units) + 1e-6))
    prod_summary['display_size'] = norm_sizes

    # Prepare custom hover data cleanly
    hover_matrix = np.stack((
        prod_summary['Product Name'],
        prod_summary['Division'],
        prod_summary['Factory'],
        prod_summary['profit'],
        prod_summary['units'],
        prod_summary['profit_per_unit'],
        prod_summary['quadrant']
    ), axis=-1)

    color_quad_map = {
        "Winners (High Sales & High Margin)": "#10B981",
        "Volume Traps (High Sales & Low Margin)": "#F59E0B",
        "Niche Opportunities (Low Sales & High Margin)": "#3B82F6",
        "Rationalization Candidates (Low Sales & Low Margin)": "#EF4444"
    }

    fig_matrix = px.scatter(
        prod_summary,
        x='sales',
        y='gross_margin_pct',
        color='quadrant',
        text='Product Name',
        color_discrete_map=color_quad_map,
        labels={'sales': 'Total Sales Revenue ($)', 'gross_margin_pct': 'Gross Margin (%)'}
    )

    fig_matrix.update_traces(
        marker=dict(
            size=prod_summary['display_size'],
            line=dict(width=1.5, color='#1E293B'),
            opacity=0.9
        ),
        textposition="top center",
        textfont=dict(size=9.5, color='#334155'),
        customdata=hover_matrix,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Division: %{customdata[1]} | Factory: %{customdata[2]}<br>"
            "Total Sales: $%{x:,.2f}<br>"
            "Gross Margin: %{y:.2f}%<br>"
            "Gross Profit: $%{customdata[3]:,.2f}<br>"
            "Units Sold: %{customdata[4]:,}<br>"
            "Profit per Unit: $%{customdata[5]:.2f}<br>"
            "Quadrant: <b>%{customdata[6]}</b>"
            "<extra></extra>"
        )
    )

    # Reference Threshold Lines
    fig_matrix.add_hline(
        y=margin_threshold,
        line_dash="dash",
        line_color="#64748B",
        annotation_text=f"Margin Target: {margin_threshold:.1f}%",
        annotation_position="bottom right"
    )
    fig_matrix.add_vline(
        x=sales_benchmark,
        line_dash="dash",
        line_color="#64748B",
        annotation_text=f"Median Sales: ${sales_benchmark:,.0f}",
        annotation_position="top left"
    )

    # Auto-Padded Axis Ranges to ensure NO points are cut off
    max_sales_val = prod_summary['sales'].max() * 1.12
    min_sales_val = max(1.0, prod_summary['sales'].min() * 0.7)
    max_margin_val = min(105.0, max(85.0, prod_summary['gross_margin_pct'].max() + 8.0))
    min_margin_val = max(-2.0, prod_summary['gross_margin_pct'].min() - 8.0)

    fig_matrix.update_layout(
        title=dict(
            text="Strategic Product Matrix: Gross Margin (%) vs. Total Sales ($)",
            font=dict(size=15, color='#0F172A')
        ),
        xaxis=dict(
            title="Total Sales Revenue ($)",
            type="log" if is_log else "linear",
            range=[np.log10(min_sales_val), np.log10(max_sales_val)] if is_log else [0, max_sales_val],
            tickformat="$,.0f",
            gridcolor="#F1F5F9"
        ),
        yaxis=dict(
            title="Gross Margin (%)",
            range=[min_margin_val, max_margin_val],
            tickformat=".0f",
            ticksuffix="%",
            gridcolor="#F1F5F9"
        ),
        legend=dict(
            title=dict(text="Strategic Quadrant"),
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=50, b=90, l=40, r=40),
        height=540,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF"
    )

    st.plotly_chart(fig_matrix, use_container_width=True)

    # Quadrant Summary Statistics
    q_counts = prod_summary['quadrant'].value_counts()
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        st.markdown(f"**🟢 Winners**: {q_counts.get('Winners (High Sales & High Margin)', 0)} SKUs")
    with qc2:
        st.markdown(f"**🟡 Volume Traps**: {q_counts.get('Volume Traps (High Sales & Low Margin)', 0)} SKUs")
    with qc3:
        st.markdown(f"**🔵 Niche Opportunities**: {q_counts.get('Niche Opportunities (Low Sales & High Margin)', 0)} SKUs")
    with qc4:
        st.markdown(f"**🔴 Rationalization**: {q_counts.get('Rationalization Candidates (Low Sales & Low Margin)', 0)} SKUs")


# ------------------------------------------------------------------------------
# TAB 2: DIVISION PERFORMANCE DASHBOARD
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("### Division Financial Performance & Structural Efficiency")
    st.caption("Aggregated assessment of revenue contribution, cost absorption, and margin generation across product divisions.")

    div_summary = filtered_df.groupby('Division').agg(
        orders=('Order ID', 'count'),
        units=('Units', 'sum'),
        sales=('Sales', 'sum'),
        cost=('Cost', 'sum'),
        profit=('Gross Profit', 'sum')
    ).reset_index()

    div_summary['margin_pct'] = (div_summary['profit'] / div_summary['sales'] * 100).round(2)
    div_summary['rev_share'] = (div_summary['sales'] / total_sales * 100).round(2)
    div_summary['prof_share'] = (div_summary['profit'] / total_profit * 100).round(2)
    div_summary['efficiency_index'] = np.where(
        div_summary['rev_share'] > 0,
        (div_summary['prof_share'] / div_summary['rev_share']).round(2),
        0.0
    )

    col_d1, col_d2 = st.columns([3, 2])

    with col_d1:
        # Grouped Bar Chart: Revenue vs Cost vs Profit
        fig_div_bars = go.Figure(data=[
            go.Bar(
                name='Revenue ($)',
                x=div_summary['Division'],
                y=div_summary['sales'],
                marker_color='#3B82F6',
                hovertemplate='Division: %{x}<br>Revenue: $%{y:,.2f}<extra></extra>'
            ),
            go.Bar(
                name='Manufacturing Cost ($)',
                x=div_summary['Division'],
                y=div_summary['cost'],
                marker_color='#F97316',
                hovertemplate='Division: %{x}<br>Cost: $%{y:,.2f}<extra></extra>'
            ),
            go.Bar(
                name='Gross Profit ($)',
                x=div_summary['Division'],
                y=div_summary['profit'],
                marker_color='#10B981',
                hovertemplate='Division: %{x}<br>Gross Profit: $%{y:,.2f}<extra></extra>'
            )
        ])
        fig_div_bars.update_layout(
            barmode='group',
            title="Revenue, Cost & Profit Comparison by Division",
            yaxis=dict(title="Amount ($)", tickformat="$,.0f"),
            legend=dict(orientation="h", y=1.1, x=0),
            margin=dict(t=50, b=30, l=40, r=20),
            height=400,
            plot_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_div_bars, use_container_width=True)

    with col_d2:
        # Profit Efficiency Index Chart
        fig_eff = px.bar(
            div_summary,
            x='Division',
            y='efficiency_index',
            color='efficiency_index',
            color_continuous_scale='Tealgrn',
            title="Profit Efficiency Ratio (Profit Share % ÷ Revenue Share %)",
            labels={'efficiency_index': 'Efficiency Ratio'},
            text='efficiency_index'
        )
        fig_eff.add_hline(y=1.0, line_dash="dash", line_color="#EF4444", annotation_text="Parity (1.0)")
        fig_eff.update_traces(
            texttemplate='%{text:.2f}x',
            textposition='outside',
            hovertemplate='Division: %{x}<br>Efficiency Ratio: %{y:.2f}x<extra></extra>'
        )
        fig_eff.update_layout(
            yaxis=dict(title="Efficiency Ratio", range=[0, max(1.5, div_summary['efficiency_index'].max() * 1.25)]),
            margin=dict(t=50, b=30, l=30, r=20),
            height=400,
            plot_bgcolor="#FFFFFF",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_eff, use_container_width=True)

    # Division Summary Table
    st.markdown("##### 📋 Division Breakdown Table")
    div_table = div_summary[['Division', 'orders', 'units', 'sales', 'cost', 'profit', 'margin_pct', 'efficiency_index']].copy()
    div_table.columns = ['Division', 'Orders', 'Units Sold', 'Revenue ($)', 'Cost ($)', 'Gross Profit ($)', 'Gross Margin (%)', 'Efficiency Index']
    st.dataframe(
        div_table.style.format({
            'Revenue ($)': '${:,.2f}',
            'Cost ($)': '${:,.2f}',
            'Gross Profit ($)': '${:,.2f}',
            'Gross Margin (%)': '{:.2f}%',
            'Orders': '{:,}',
            'Units Sold': '{:,}',
            'Efficiency Index': '{:.2f}x'
        }),
        use_container_width=True
    )


# ------------------------------------------------------------------------------
# TAB 3: COST VS MARGIN DIAGNOSTICS & ACTIONABLE ALERTS
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("### Cost Structure Diagnostics & Strategic Risk Alerts")
    st.caption("Pinpointing manufacturing cost inflation, pricing inefficiencies, and high-risk SKUs.")

    col_c1, col_c2 = st.columns([3, 2])

    with col_c1:
        # Scatter: Cost vs Sales with Breakeven Diagonal Line
        fig_cost_scatter = px.scatter(
            prod_summary,
            x='cost',
            y='sales',
            size='units',
            color='quadrant',
            color_discrete_map=color_quad_map,
            labels={'cost': 'Total Manufacturing Cost ($)', 'sales': 'Total Sales Revenue ($)'}
        )
        
        # 1:1 Breakeven Line (Sales = Cost -> 0% Margin)
        max_cost_val = max(prod_summary['sales'].max(), prod_summary['cost'].max()) * 1.05
        fig_cost_scatter.add_shape(
            type="line", x0=0, y0=0, x1=max_cost_val, y1=max_cost_val,
            line=dict(color="#CBD5E1", dash="dot", width=1.5)
        )
        fig_cost_scatter.add_annotation(
            x=max_cost_val * 0.85, y=max_cost_val * 0.85,
            text="Breakeven (0% Margin)", showarrow=False,
            font=dict(size=10, color="#94A3B8")
        )

        fig_cost_scatter.update_traces(
            marker=dict(size=prod_summary['display_size'], line=dict(width=1, color='#0F172A')),
            customdata=hover_matrix,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Division: %{customdata[1]} | Factory: %{customdata[2]}<br>"
                "Sales: $%{y:,.2f}<br>"
                "Cost: $%{x:,.2f}<br>"
                "Gross Margin: %{customdata[5]}%<br>"
                "Units: %{customdata[4]:,}"
                "<extra></extra>"
            )
        )
        fig_cost_scatter.update_layout(
            title="Manufacturing Cost vs. Sales Revenue ($)",
            xaxis=dict(title="Manufacturing Cost ($)", tickformat="$,.0f", gridcolor="#F1F5F9"),
            yaxis=dict(title="Sales Revenue ($)", tickformat="$,.0f", gridcolor="#F1F5F9"),
            legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
            margin=dict(t=40, b=60, l=40, r=20),
            height=460,
            plot_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_cost_scatter, use_container_width=True)

    with col_c2:
        # Unit Price vs. Unit Cost (Horizontal Bar Chart)
        # Sort by unit margin descending
        top_unit_df = prod_summary.sort_values('unit_price', ascending=False).head(10).copy()
        fig_unit_comp = go.Figure(data=[
            go.Bar(
                name='Unit Selling Price ($)',
                y=top_unit_df['Product Name'],
                x=top_unit_df['unit_price'],
                orientation='h',
                marker_color='#3B82F6',
                hovertemplate='Price: $%{x:.2f}<extra></extra>'
            ),
            go.Bar(
                name='Unit Manufacturing Cost ($)',
                y=top_unit_df['Product Name'],
                x=top_unit_df['unit_cost'],
                orientation='h',
                marker_color='#EF4444',
                hovertemplate='Cost: $%{x:.2f}<extra></extra>'
            )
        ])
        fig_unit_comp.update_layout(
            barmode='group',
            title="Unit Price vs. Unit Cost ($/unit)",
            xaxis=dict(title="Dollars ($)", tickformat="$,.2f"),
            yaxis=dict(autorange="reversed"),
            legend=dict(orientation="h", y=1.1, x=0),
            margin=dict(t=50, b=30, l=160, r=20),
            height=460,
            plot_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_unit_comp, use_container_width=True)

    # --------------------------------------------------------------------------
    # CLEAN, DATA-GROUNDED RECOMMENDATION CARDS (NO RAW MARKDOWN SYNTAX)
    # --------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 🎯 Automated SKU Recommendations & Strategic Interventions")
    st.caption("Recommendations are dynamically derived from cost-to-price ratios, sales volume, and target margin thresholds.")

    # Render Clean Alert Cards
    for _, row in prod_summary.iterrows():
        rec = row['rec_data']
        level_class = f"rec-{rec['level']}"
        st.markdown(f"""
        <div class="rec-card {level_class}">
            <div class="rec-header">{rec['title']} &nbsp;·&nbsp; Division: {row['Division']} &nbsp;·&nbsp; Plant: {row['Factory']}</div>
            <div class="rec-body">
                <b>Diagnostic:</b> {rec['finding']}<br>
                <b>Recommended Action:</b> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 4: PROFIT CONCENTRATION (PARETO 80/20 ANALYSIS)
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("### Profit Concentration & Portfolio Dependency (Pareto 80/20)")
    st.caption("Quantifying corporate reliance on top revenue and gross profit drivers to evaluate portfolio vulnerability.")

    pareto_df = prod_summary.sort_values('profit', ascending=False).reset_index(drop=True)
    pareto_df['cum_profit'] = pareto_df['profit'].cumsum()
    pareto_df['cum_profit_pct'] = (pareto_df['cum_profit'] / total_profit * 100).round(2)
    pareto_df['sku_rank'] = pareto_df.index + 1
    pareto_df['sku_pct'] = (pareto_df['sku_rank'] / len(pareto_df) * 100).round(2)

    cutoff_row = pareto_df[pareto_df['cum_profit_pct'] >= 80.0].iloc[0]
    num_skus_80 = int(cutoff_row['sku_rank'])
    pct_skus_80 = float(cutoff_row['sku_pct'])

    cp1, cp2 = st.columns([1, 2])

    with cp1:
        st.markdown(f"""
        <div class="rec-card rec-warning" style="margin-top: 15px;">
            <div class="rec-header">⚠️ Single-Line Concentration Risk</div>
            <div class="rec-body">
                Just <b>{num_skus_80} out of {len(pareto_df)} products</b> ({pct_skus_80:.1f}% of catalog) deliver 
                <b>{cutoff_row['cum_profit_pct']:.1f}% of corporate gross profit</b>.
                <br><br>
                <b>Primary Profit Engines:</b>
                <ul style="margin-top: 6px; padding-left: 18px;">
                    {"".join([f"<li>{name} ({pareto_df.loc[i, 'gross_margin_pct']:.1f}% margin)</li>" for i, name in enumerate(pareto_df.head(num_skus_80)['Product Name'])])}
                </ul>
                <b>Strategic Vulnerability:</b> Supply chain disruption or cocoa ingredient inflation directly imperils overall company solvency.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with cp2:
        # Pareto Dual-Axis Curve
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(
            x=pareto_df['Product Name'],
            y=pareto_df['profit'],
            name='Gross Profit ($)',
            marker_color='#3B82F6',
            yaxis='y1',
            hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.2f}<extra></extra>'
        ))
        fig_pareto.add_trace(go.Scatter(
            x=pareto_df['Product Name'],
            y=pareto_df['cum_profit_pct'],
            name='Cumulative Profit (%)',
            marker_color='#EF4444',
            mode='lines+markers',
            yaxis='y2',
            hovertemplate='Cumulative Profit: %{y:.2f}%<extra></extra>'
        ))
        fig_pareto.add_hline(
            y=80.0, line_dash="dash", line_color="#EF4444", yref="y2",
            annotation_text="80% Threshold", annotation_position="top left"
        )
        fig_pareto.update_layout(
            title="Pareto 80/20 Cumulative Gross Profit Concentration",
            yaxis=dict(title="Gross Profit ($)", tickformat="$,.0f"),
            yaxis2=dict(title="Cumulative Profit (%)", overlaying="y", side="right", range=[0, 105], ticksuffix="%"),
            xaxis=dict(tickangle=45, tickfont=dict(size=10)),
            legend=dict(x=0.02, y=0.98),
            margin=dict(t=50, b=110, l=30, r=30),
            height=460,
            plot_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig_pareto, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 5: FACTORY & SUPPLY CHAIN INTELLIGENCE
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("### Manufacturing Facilities & Nationwide Sourcing Analytics")
    st.caption("Correlating manufacturing plant locations, capacity production, and plant gross margin output.")

    factory_summary = filtered_df.groupby(['Factory', 'Factory Latitude', 'Factory Longitude']).agg(
        orders=('Order ID', 'count'),
        units=('Units', 'sum'),
        sales=('Sales', 'sum'),
        cost=('Cost', 'sum'),
        profit=('Gross Profit', 'sum'),
        products_made=('Product Name', 'nunique')
    ).reset_index()

    factory_summary['margin_pct'] = (factory_summary['profit'] / factory_summary['sales'] * 100).round(2)
    factory_summary['profit_share'] = (factory_summary['profit'] / total_profit * 100).round(2)

    col_f1, col_f2 = st.columns([3, 2])

    with col_f1:
        # Nationwide Geospatial Facility Map
        fig_map = px.scatter_geo(
            factory_summary,
            lat='Factory Latitude',
            lon='Factory Longitude',
            hover_name='Factory',
            size='profit',
            color='margin_pct',
            scope='usa',
            title="Manufacturing Plants: Gross Profit & Plant Margin (%)",
            color_continuous_scale='Viridis',
            hover_data={'sales': ':$,.2f', 'profit': ':$,.2f', 'margin_pct': ':.2f%', 'products_made': True}
        )
        fig_map.update_layout(margin=dict(t=40, b=10, l=10, r=10), height=430)
        st.plotly_chart(fig_map, use_container_width=True)

    with col_f2:
        # Plant Output Bar Chart
        fig_fact_bar = px.bar(
            factory_summary.sort_values('profit', ascending=True),
            x='profit',
            y='Factory',
            orientation='h',
            title="Total Profit Generated by Manufacturing Site ($)",
            labels={'profit': 'Gross Profit ($)', 'Factory': 'Plant Facility'},
            color='margin_pct',
            color_continuous_scale='Greens',
            text='profit'
        )
        fig_fact_bar.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_fact_bar.update_layout(margin=dict(t=40, b=10, l=10, r=10), height=430)
        st.plotly_chart(fig_fact_bar, use_container_width=True)

    st.markdown("##### 🏭 Facility Operational & Financial Scorecard")
    fact_table = factory_summary[['Factory', 'products_made', 'units', 'sales', 'profit', 'margin_pct', 'profit_share']].copy()
    fact_table.columns = ['Manufacturing Plant', 'SKUs Produced', 'Units Built', 'Total Revenue ($)', 'Gross Profit ($)', 'Plant Margin (%)', 'Corporate Profit Share (%)']
    st.dataframe(
        fact_table.style.format({
            'Total Revenue ($)': '${:,.2f}',
            'Gross Profit ($)': '${:,.2f}',
            'Plant Margin (%)': '{:.2f}%',
            'Corporate Profit Share (%)': '{:.2f}%',
            'Units Built': '{:,}'
        }),
        use_container_width=True
    )


# ==============================================================================
# 7. STAKEHOLDER EXPORT MODULE
# ==============================================================================
st.markdown("---")
down_col1, down_col2 = st.columns([3, 1])
with down_col1:
    st.caption("Nassau Candy Distributor BI Analytics Engine | Unified Mentor Fellowship Submission")
with down_col2:
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Active Dataset (CSV)",
        data=csv_bytes,
        file_name=f"nassau_candy_active_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )
