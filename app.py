import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import numpy as np

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------
st.set_page_config(
    page_title="Scion Amazon Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b, #111827);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.35);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    transition: 0.3s ease;
}

div[data-testid="stDataFrame"] {
    background-color: #111827;
    border-radius: 12px;
    padding: 10px;
}

h1, h2, h3 {
    color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# TITLE
# --------------------------------------------------------
st.title("🚀 Scion Amazon Executive Dashboard")
st.markdown("### Advanced Amazon Sales & Performance Analytics")

# --------------------------------------------------------
# FILE PATH
# --------------------------------------------------------
FILE_PATH = "Scion_Amazon_Overall_Sales (Oct - Apr) (1).xlsx"

# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------
try:

    df = pd.read_excel(FILE_PATH, sheet_name="Overall Sales Data")

    # --------------------------------------------------------
    # MONTH ORDER
    # --------------------------------------------------------
    month_order = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']

    df['Month'] = pd.Categorical(
        df['Month'],
        categories=month_order,
        ordered=True
    )

    # --------------------------------------------------------
    # MONTHLY SUMMARY
    # --------------------------------------------------------
    monthly = df.groupby('Month', as_index=False).agg({
        'Ordered Product Sales': 'sum',
        'Units Ordered': 'sum',
        'Sessions - Total': 'sum',
        'Page Views - Total': 'sum',
        'Featured Offer (Buy Box) Percentage': 'mean',
        'Unit Session Percentage': 'mean',
        'Total Order Items': 'sum'
    })

    # --------------------------------------------------------
    # EXTRA CALCULATIONS
    # --------------------------------------------------------
    monthly['Revenue Growth %'] = (
        monthly['Ordered Product Sales'].pct_change() * 100
    )

    monthly['Traffic Growth %'] = (
        monthly['Sessions - Total'].pct_change() * 100
    )

    monthly['Unit Growth %'] = (
        monthly['Units Ordered'].pct_change() * 100
    )

    monthly['Avg Selling Price'] = (
        monthly['Ordered Product Sales'] /
        monthly['Units Ordered']
    )

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------
    total_revenue = monthly['Ordered Product Sales'].sum()

    total_units = monthly['Units Ordered'].sum()

    total_sessions = monthly['Sessions - Total'].sum()

    avg_conversion = (
        monthly['Unit Session Percentage'].mean() * 100
    )

    avg_buybox = (
        monthly['Featured Offer (Buy Box) Percentage'].mean() * 100
    )

    avg_asp = monthly['Avg Selling Price'].mean()

    # --------------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------------
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric(
        "💰 Revenue",
        f"AED {total_revenue:,.0f}",
        delta=f"{monthly['Revenue Growth %'].iloc[-1]:.1f}%"
    )

    k2.metric(
        "📦 Units Sold",
        f"{total_units:,}",
        delta=f"{monthly['Unit Growth %'].iloc[-1]:.1f}%"
    )

    k3.metric(
        "👥 Sessions",
        f"{total_sessions:,}",
        delta=f"{monthly['Traffic Growth %'].iloc[-1]:.1f}%"
    )

    k4.metric(
        "📈 Conversion",
        f"{avg_conversion:.2f}%"
    )

    k5.metric(
        "🛒 Buy Box %",
        f"{avg_buybox:.2f}%"
    )

    k6.metric(
        "💵 Avg Selling Price",
        f"AED {avg_asp:.2f}"
    )

    st.divider()

    # --------------------------------------------------------
    # REVENUE + UNITS CHART
    # --------------------------------------------------------
    c1, c2 = st.columns(2)

    with c1:

        st.subheader("💰 Revenue vs Units Performance")

        fig_rev = go.Figure()

        fig_rev.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['Ordered Product Sales'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#00E5FF', width=5),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(0,229,255,0.15)'
        ))

        fig_rev.add_trace(go.Bar(
            x=monthly['Month'],
            y=monthly['Units Ordered'],
            name='Units Ordered',
            marker=dict(
                color=monthly['Units Ordered'],
                colorscale='Turbo'
            ),
            opacity=0.8,
            yaxis='y2'
        ))

        fig_rev.update_layout(
            template='plotly_dark',
            paper_bgcolor='#111827',
            plot_bgcolor='#111827',
            height=500,
            yaxis2=dict(
                overlaying='y',
                side='right'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        st.plotly_chart(fig_rev, use_container_width=True)

    # --------------------------------------------------------
    # TRAFFIC + CONVERSION CHART
    # --------------------------------------------------------
    with c2:

        st.subheader("📈 Traffic & Conversion Trend")

        fig_conv = go.Figure()

        fig_conv.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['Sessions - Total'],
            mode='lines+markers',
            name='Sessions',
            line=dict(color='#8b5cf6', width=4),
            fill='tozeroy',
            fillcolor='rgba(139,92,246,0.15)'
        ))

        fig_conv.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['Unit Session Percentage'] * 100,
            mode='lines+markers',
            name='Conversion %',
            line=dict(color='#22c55e', width=4),
            yaxis='y2'
        ))

        fig_conv.update_layout(
            template='plotly_dark',
            paper_bgcolor='#111827',
            plot_bgcolor='#111827',
            height=500,
            yaxis2=dict(
                overlaying='y',
                side='right'
            )
        )

        st.plotly_chart(fig_conv, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # BRAND ANALYSIS
    # --------------------------------------------------------
    b1, b2 = st.columns(2)

    with b1:

        st.subheader("🏷️ Top Brands by Revenue")

        brand_data = (
            df.groupby('Brand')['Ordered Product Sales']
            .sum()
            .sort_values(ascending=True)
            .tail(10)
        )

        fig_brand = px.bar(
            brand_data,
            orientation='h',
            color=brand_data.values,
            color_continuous_scale='Sunset',
            text_auto='.2s'
        )

        fig_brand.update_layout(
            template='plotly_dark',
            paper_bgcolor='#111827',
            plot_bgcolor='#111827',
            height=500,
            showlegend=False
        )

        st.plotly_chart(fig_brand, use_container_width=True)

    # --------------------------------------------------------
    # BUY BOX GAUGE
    # --------------------------------------------------------
    with b2:

        st.subheader("🎯 Buy Box Health Score")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_buybox,
            title={'text': "Buy Box Percentage"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#06b6d4"},
                'steps': [
                    {'range': [0, 50], 'color': "#ef4444"},
                    {'range': [50, 80], 'color': "#f59e0b"},
                    {'range': [80, 100], 'color': "#22c55e"}
                ]
            }
        ))

        fig_gauge.update_layout(
            template='plotly_dark',
            paper_bgcolor='#111827',
            height=500
        )

        st.plotly_chart(fig_gauge, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------
    st.subheader("🔥 Revenue Heatmap")

    heat_values = [monthly['Ordered Product Sales'].values]

    fig_heat = px.imshow(
        heat_values,
        labels=dict(color="Revenue"),
        x=monthly['Month'],
        y=['Revenue'],
        color_continuous_scale='Turbo',
        aspect='auto'
    )

    fig_heat.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        height=300
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------
    st.subheader("🏆 Top 10 Products by Revenue")

    top_products = (
        df.groupby('Title')
        .agg({
            'Ordered Product Sales': 'sum',
            'Units Ordered': 'sum',
            'Sessions - Total': 'sum'
        })
        .sort_values(by='Ordered Product Sales', ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x='Ordered Product Sales',
        y='Title',
        orientation='h',
        color='Ordered Product Sales',
        color_continuous_scale='Plasma',
        text_auto='.2s'
    )

    fig_products.update_layout(
        template='plotly_dark',
        paper_bgcolor='#111827',
        plot_bgcolor='#111827',
        height=700,
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(fig_products, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # EXECUTIVE SCORE
    # --------------------------------------------------------
    performance_score = (
        avg_conversion +
        avg_buybox
    ) / 2

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg,#7c3aed,#06b6d4);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 25px rgba(0,0,0,0.4);
    ">

        <h2 style="color:white;">
            Executive Marketplace Score
        </h2>

        <h1 style="
            font-size:70px;
            color:white;
            margin-bottom:10px;
        ">
            {performance_score:.1f}
        </h1>

        <p style="
            color:white;
            font-size:18px;
        ">
            Overall Amazon Marketplace Health
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --------------------------------------------------------
    # MONTHLY TABLE
    # --------------------------------------------------------
    st.subheader("📋 Monthly Performance Summary")

    display_df = monthly.copy()

    display_df['Ordered Product Sales'] = (
        display_df['Ordered Product Sales']
        .map('AED {:,.2f}'.format)
    )

    display_df['Featured Offer (Buy Box) Percentage'] = (
        display_df['Featured Offer (Buy Box) Percentage']
        .mul(100)
        .map('{:.2f}%'.format)
    )

    display_df['Unit Session Percentage'] = (
        display_df['Unit Session Percentage']
        .mul(100)
        .map('{:.2f}%'.format)
    )

    display_df['Revenue Growth %'] = (
        display_df['Revenue Growth %']
        .fillna(0)
        .map('{:.2f}%'.format)
    )

    display_df['Traffic Growth %'] = (
        display_df['Traffic Growth %']
        .fillna(0)
        .map('{:.2f}%'.format)
    )

    display_df['Unit Growth %'] = (
        display_df['Unit Growth %']
        .fillna(0)
        .map('{:.2f}%'.format)
    )

    display_df['Avg Selling Price'] = (
        display_df['Avg Selling Price']
        .map('AED {:.2f}'.format)
    )

    st.dataframe(display_df, use_container_width=True)

    st.divider()

    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------
    html_report = f"""
    <html>
    <body style="
        background:#111827;
        color:white;
        font-family:Arial;
        padding:30px;
    ">

    <h1 style="color:#00E5FF;">
        Scion Amazon Executive Report
    </h1>

    <h2>Total Revenue: AED {total_revenue:,.2f}</h2>

    <h3>Total Units Sold: {total_units:,}</h3>

    <h3>Total Sessions: {total_sessions:,}</h3>

    <h3>Average Conversion: {avg_conversion:.2f}%</h3>

    <h3>Average Buy Box: {avg_buybox:.2f}%</h3>

    {monthly.to_html(index=False)}

    </body>
    </html>
    """

    b64 = base64.b64encode(
        html_report.encode()
    ).decode()

    href = f"""
    <a href="data:text/html;base64,{b64}"
    download="Scion_Amazon_Report.html">

    <button style="
        width:100%;
        padding:18px;
        background:linear-gradient(135deg,#06b6d4,#8b5cf6);
        color:white;
        font-size:18px;
        font-weight:bold;
        border:none;
        border-radius:12px;
        cursor:pointer;
    ">
        ⬇ Download Executive HTML Report
    </button>

    </a>
    """

    st.markdown(href, unsafe_allow_html=True)

except Exception as e:

    st.error(f"Error loading file: {e}")
