import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# Configure Streamlit page
st.set_page_config(page_title="Amazon Performance Dashboard", layout="wide")

st.title("📈 Amazon 6-Month Trend Analyzer")
st.markdown("Upload the **Scion_Amazon_Overall_Sales (Oct - Apr) (1).xlsx** report to visualize performance trends.")

# File uploader widget
uploaded_file = st.file_uploader("Choose the raw Excel report", type="xlsx")

if uploaded_file:
    # Load specific sheet
    df = pd.read_excel(uploaded_file, sheet_name='Overall Sales Data')
    
    # Define and apply chronological month order
    month_order = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    
    # Aggregate metrics by Month
    monthly_trend = df.groupby('Month', as_index=False).agg({
        'Ordered Product Sales': 'sum',
        'Units Ordered': 'sum',
        'Sessions - Total': 'sum',
        'Page Views - Total': 'sum'
    })

    # High-level Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_sales = monthly_trend['Ordered Product Sales'].sum()
    total_units = monthly_trend['Units Ordered'].sum()
    
    col1.metric("Total Sales (6M)", f"AED {total_sales:,.2f}")
    col2.metric("Total Units", f"{total_units:,}")
    col3.metric("Avg. Monthly Sales", f"AED {total_sales/6:,.2f}")
    col4.metric("Avg. Conversion Rate", f"{(total_units/monthly_trend['Sessions - Total'].sum())*100:.2f}%")

    # Visual Trend Analysis
    st.subheader("Monthly Revenue & Volume Trend")
    fig = px.line(monthly_trend, x='Month', y='Ordered Product Sales', 
                  title="Sales Trend (Oct - Apr)", markers=True,
                  line_shape="spline", color_discrete_sequence=["#2E7D32"])
    
    # Add units as a secondary bar chart
    fig.add_bar(x=monthly_trend['Month'], y=monthly_trend['Units Ordered'], name="Units", yaxis="y2")
    fig.update_layout(yaxis2=dict(overlaying='y', side='right'))
    st.plotly_chart(fig, use_container_width=True)

    # Summary Table with formatting
    styled_df = monthly_trend.style.format({
        'Ordered Product Sales': 'AED {:,.2f}',
        'Units Ordered': '{:,}'
    }).background_gradient(cmap='Greens', subset=['Ordered Product Sales'])

    st.subheader("Summary Table")
    st.table(styled_df)

    # Generate Downloadable HTML Report
    html_content = f'''
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h2 {{ color: #2E7D32; border-bottom: 2px solid #2E7D32; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #2E7D32; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Amazon 6-Month Performance Report</h2>
        {monthly_trend.to_html(classes='table', index=False)}
    </body>
    </html>
    '''
    
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="Amazon_Trend_Report.html"><button style="padding:10px; background-color:#2E7D32; color:white; border:none; border-radius:5px; cursor:pointer;">Download HTML Report</button></a>'
    st.markdown(href, unsafe_allow_html=True)
