import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from datetime import datetime, timedelta, timezone
import plotly.express as px
import os
import json
import time
# import jwt
# st.set_page_config(page_title="📊 Sales Dashboard", layout="wide", page_icon="onus_logo.png",initial_sidebar_state="collapsed")
# ###TOKEN AUTHENTICATION START
# # Set Page Config

# # Constants
# SECRET_KEY = "MTlnqhdW4KvxCuS"
# STORAGE_TYPE = "json"  # Change to "json" if needed

# PARQUET_FILE = r"used_tokens.parquet"
# JSON_FILE = r"used_tokens.json"

# LOCK_FILE = (PARQUET_FILE if STORAGE_TYPE == "parquet" else JSON_FILE) + ".lock"

# # ------------------------
# # Storage Backends
# # ------------------------

# def load_used_tokens_parquet():
#     if os.path.exists(PARQUET_FILE):
#         df = pd.read_parquet(PARQUET_FILE)
#         return set(df["token"])
#     return set()

# def mark_token_used_parquet(token):
#     df_new = pd.DataFrame([{"token": token, "used_at": time.time()}])
#     if os.path.exists(PARQUET_FILE):
#         df_existing = pd.read_parquet(PARQUET_FILE)
#         df_combined = pd.concat([df_existing, df_new], ignore_index=True)
#     else:
#         df_combined = df_new
#     df_combined.to_parquet(PARQUET_FILE, index=False)

# def load_used_tokens_json():
#     if os.path.exists(JSON_FILE):
#         with open(JSON_FILE, "r") as f:
#             data = json.load(f)
#             return set(data.get("tokens", []))
#     return set()

# def mark_token_used_json(token):
#     if os.path.exists(JSON_FILE):
#         with open(JSON_FILE, "r") as f:
#             data = json.load(f)
#     else:
#         data = {"tokens": []}
#     data["tokens"].append(token)
#     with open(JSON_FILE, "w") as f:
#         json.dump(data, f)

# # ------------------------
# # Unified Interface
# # ------------------------

# def load_used_tokens():
#     return (
#         load_used_tokens_parquet()
#         if STORAGE_TYPE == "parquet"
#         else load_used_tokens_json()
#     )

# def mark_token_used(token):
#     return (
#         mark_token_used_parquet(token)
#         if STORAGE_TYPE == "parquet"
#         else mark_token_used_json(token)
#     )

# # ------------------------
# # Token Validation Logic
# # ------------------------

# def validate_token_locally(token):
#     try:
#         decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         used_tokens = load_used_tokens()
#         if token in used_tokens:
#             return {"error": "Token has already been used"}
#         mark_token_used(token)
#         return {"message": "Token is valid"}
#     except jwt.InvalidTokenError:
#         return {"error": "Invalid token"}

# # ------------------------
# # Streamlit App
# # ------------------------

# token = st.query_params.get("token", "")
# print(token, "token")

# if "authenticated" not in st.session_state:
#     if token and token != "e":
#         result = validate_token_locally(token)
#         if result.get("error"):
#             st.session_state.authenticated = False
#             st.error(f"❌ Token validation failed: {result['error']}")
#         else:
#             st.session_state.authenticated = True
#        #    st.success("✅ Token validated successfully!")
#     else:
#         st.session_state.authenticated = False
#         st.error("❌ No valid token found in URL!")

# if st.session_state.get("authenticated"):


# ####TOKEN AUTHENTICATION END

def load_column_state(store_id):
    """
    Load saved AgGrid column state from JSON file for a specific store.
    Returns the state if found, otherwise None.
    """
    json_path = f"all_store/{store_id}/last_update.json"
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get("column_state", None)
    return None

def save_column_state(store_id, column_state):
    """
    Save AgGrid column state (order, visibility) to JSON for a specific store.
    Keeps existing data like last_id and last_update.
    """
    json_path = f"all_store/{store_id}/last_update.json"
    data = {}
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)

    data["column_state"] = column_state

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, default=str)


    # Set Page Config
st.set_page_config(page_title="📊 Sales Dashboard", layout="wide", page_icon="onus_logo.png",initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
        /* Remove left and right padding of the main container */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        /* Optional: Remove padding in wide mode */
        @media (min-width: 768px) {
            .block-container {
                padding-left: 4rem !important;
                padding-right: 1rem !important;
            }
        }
        /* Only affect visible sidebar (not collapsed) */
        section[data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 315px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
/* Remove Streamlit header */
header, [data-testid="stHeader"] {
    display: none !important;
}

/* Remove excessive top padding from main container */
.block-container {
    padding-top: 1rem !important;  /* Reduce from 6rem (96px) to 1rem */
}

/* Optional: Remove bottom padding too if not needed */
.block-container {
    padding-bottom: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: black;
        background-color: #F0F0F0;
        border-radius: 5px 5px 0 0;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #00B776 !important;
        color: white !important;
        background-color: #00B776;
    }
    </style>
""", unsafe_allow_html=True)


# st.title("📊 Sales Dashboard")
st.markdown(
    """
    <style>
        .custom-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.5rem;
        }
    </style>
    <div class="custom-title">📊 Sales Dashboard</div>
    """,
    unsafe_allow_html=True
)


# Placeholder for the loader
placeholder = st.empty()

# CSS for full-screen centered loader
loading_css = """
<style>
#overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    background: white;
    top: 0;
    left: 0;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}
</style>
"""

# HTML for overlay loader
loading_html = """
<div id="overlay">
    <img src="https://i.gifer.com/ZC9Y.gif" width="300">
    <h2>Loading Sales Dashboard...</h2>
</div>
"""

def render_centered_table(df, max_height="350px"):
    html = f"""
    <style>
    .scroll-container {{
        max-height: {max_height};
        overflow-y: auto;
        border: 1px solid #ddd;
        border-radius: 6px;
    }}
    table.custom-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        table-layout: fixed;
    }}
    .custom-table th, .custom-table td {{
        text-align: center;
        padding: 5px;
        border: 1px solid #e0e0e0;
        word-wrap: break-word;
    }}
    .custom-table th {{
        background-color: #f7f9fa;
        font-weight: 600;
        position: sticky;
        top: 0;
        z-index: 1;
        text-transform: uppercase;
    }}
    .custom-table tr:nth-child(even) {{
        background-color: #fbfbfb;
    }}
    </style>
    <div class="scroll-container">
        <table class="custom-table">
            <thead><tr>{''.join(f'<th>{col}</th>' for col in df.columns)}</tr></thead>
            <tbody>
                {''.join(
                    f"<tr>{''.join(f'<td>{val}</td>' for val in row)}</tr>" 
                    for _, row in df.iterrows()
                )}
            </tbody>
        </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# Display the loader inside the placeholder
placeholder.markdown(loading_css + loading_html, unsafe_allow_html=True)

query_params = st.query_params
store_id = query_params.get("store_id", '348')

@st.cache_data(ttl=50)  # Refresh cache every 5 minutes automatically
def load_parquet(store_id, cache_bust):
    filepath = f"all_store/{store_id}/sales_history_products_{store_id}.parquet"
    try:
        df = pd.read_parquet(filepath)
        df['loaded_at'] = datetime.now()  # Add timestamp to verify refresh
        return df
    except FileNotFoundError:
        st.error(f"No data found for Store ID: {store_id}")
        st.stop()

# Silent cache-busting every interval without noticeable refresh
def auto_refresh_cache(interval_sec=50):
    if 'last_cache_refresh' not in st.session_state:
        st.session_state['last_cache_refresh'] = time.time()

    current_time = time.time()
    if current_time - st.session_state['last_cache_refresh'] > interval_sec:
        st.session_state['cache_bust'] = current_time
        st.session_state['last_cache_refresh'] = current_time

auto_refresh_cache(interval_sec=50)
cache_bust = st.session_state.get('cache_bust', 0)

print("product start time from file:", datetime.now())
df = load_parquet(store_id, cache_bust=cache_bust)
print("Data fetching complete:", datetime.now())

# st.title("📊 Store Product Sales Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Date Range Selection with Shortcuts
today = datetime.combine(datetime.today().date(), datetime.min.time()).replace(tzinfo=timezone.utc)
yesterday = today - timedelta(days=1)
last_7_days = today - timedelta(days=7)
last_6_months = today - timedelta(days=180)
last_year = today.replace(year=today.year - 1)

# Last Month Calculation (First & Last Day)
first_day_of_current_month = today.replace(day=1)
last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
first_day_of_last_month = last_day_of_last_month.replace(day=1)

# 6 months ago
first_day_of_6_months_ago = (first_day_of_current_month - timedelta(days=180)).replace(day=1)
last_day_of_last_6_months = first_day_of_current_month - timedelta(days=1)

# Last Year Calculation (First & Last Day)
first_day_of_last_year = today.replace(year=today.year - 1, month=1, day=1)
last_day_of_last_year = today.replace(year=today.year - 1, month=12, day=31)
date_option = st.sidebar.radio("📅 Quick Date Range",
                            ["Today", "Yesterday", "Last 7 Days", "Last Month", "Last 6 Months", "Last Year", "Custom"],
                            index=2)

# Set boundaries
two_years_ago = today.year - 2
# Set min date to January 1st of that year
min_date = datetime(two_years_ago, 1, 1).date()

max_date = today.date()

# Set date ranges based on selection
if date_option == "Today":
    date_range = [today, today + timedelta(hours=23, minutes=59, seconds=59)]
elif date_option == "Yesterday":
    date_range = [yesterday, yesterday + timedelta(hours=23, minutes=59, seconds=59)]
elif date_option == "Last 7 Days":
    date_range = [last_7_days, yesterday + timedelta(hours=23, minutes=59, seconds=59)]
elif date_option == "Last Month":
    date_range = [first_day_of_last_month, last_day_of_last_month + timedelta(hours=23, minutes=59, seconds=59)]
elif date_option == "Last 6 Months":
    date_range = [first_day_of_6_months_ago, last_day_of_last_6_months + timedelta(hours=23, minutes=59, seconds=59)]
elif date_option == "Last Year":
    date_range = [first_day_of_last_year, last_day_of_last_year + timedelta(hours=23, minutes=59, seconds=59)]
else:
    date_range = st.sidebar.date_input("📅 Select Date Range", [last_7_days + timedelta(days=1), today],min_value=min_date,max_value=max_date)

top_n = st.sidebar.slider("🏆 Select Top N Products", 5, 25, 10)

df_filtered = df.copy()

if df_filtered.empty:
    placeholder.empty()
    st.warning(f"⚠️ No data found for Store ID: {store_id}")
    st.stop()

# Ensure both start and end dates are selected
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)
    start_date = start_date.tz_localize('UTC') if start_date.tzinfo is None else start_date.astimezone(timezone.utc)
    end_date = end_date.tz_localize('UTC') if end_date.tzinfo is None else end_date.astimezone(timezone.utc)
    df_filtered = df_filtered[(df_filtered["date"] >= start_date) & (df_filtered["date"] <= end_date)]
    df_filtered.drop_duplicates(subset=['product_id','date','unit_qty','order_id'],inplace=True)
    df_filtered['total_sale'] = df_filtered.groupby('product_id')['unit_qty'].transform('sum')
    df_filtered.drop_duplicates(subset=['product_id'],inplace=True)
else:
    st.warning(":warning: Please select both a start and an end date.")
    placeholder.empty()
    st.stop()

def tooltip_header(title: str, tooltip: str, emoji: str = "ℹ️"):
    """
    Displays a styled header with an inline tooltip icon using your custom HTML and CSS.
    
    Args:
        title (str): The main header text.
        tooltip (str): The text to display when hovering the tooltip icon.
        emoji (str): Optional emoji to prefix the header title.
    """
    st.markdown(f"""
    <style>
    .ag-header-cell {{
        width: 140px !important;
    }}
    .header-with-tooltip {{
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 14px; /* ⬅️ Add space below the whole header */
    }}
    .header-title {{
        font-size: 2rem;     /* ⬅️ Increase title size */
        font-weight: 600;
        margin: 0;
        padding: 0;
        line-height: 1.3;
        display: inline-block;
        font-family: inherit;
        color: inherit;
    }}
    .tooltip-icon {{
        position: relative;
        display: inline-block;
        cursor: help;
        font-size: 0.8rem;
        color: #3498db;
        line-height: 1.2;
        padding: 0;
        margin: 0;
        vertical-align: middle;
        background: none;
        border: none;
    }}
    .tooltip-icon .tooltiptext {{
        visibility: hidden;
        width: 240px;
        background-color: #333;
        color: #fff;
        text-align: left;
        padding: 6px 10px;
        border-radius: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 13px;
    }}
    .tooltip-icon:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    </style>

    <div class='header-with-tooltip'>
    <span class='header-title'>{emoji} {title}</span>
    <span class='tooltip-icon'>ℹ️
        <span class='tooltiptext'>{tooltip}</span>
    </span>
    </div>
    """, unsafe_allow_html=True)

default_column_state = [
    {"colId": "product_name", "width": 282, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": True},
    {"colId": "size", "width": 86, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "SKU(s)", "width": 129, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "unit_price", "width": 114, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "category_name", "width": 200, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "division_name", "width": 200, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "7-D", "width": 78, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "30-D", "width": 84, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "60-D", "width": 84, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "90-D", "width": 84, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "180-D", "width": 100, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None},
    {"colId": "total_sale", "width": 100, "hide": False, "pinned": None, "sort": None, "sortIndex": None, "aggFunc": None, "rowGroup": False, "rowGroupIndex": None, "pivot": False, "pivotIndex": None, "flex": None}
]

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "🏆 Top Products", "📉 Low Products", "📦 Category Sales", "🏢 Division Sales", "📈 Sales Trend Analysis"
])

with tab1:

    # st.subheader("📌 Sales Summary")
    tooltip_header(
        title="Sales Summary",
        tooltip="Overview of filtered sales data, including total orders, units sold, and product count.",
        emoji="📌"
    )

    if df_filtered.empty:
        st.info("ℹ️ No sales data available for the selected filters.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", len(df_filtered["order_id"].unique()))
        col2.metric("Total Units Sold", df_filtered["total_sale"].sum())
        col3.metric("Total Unique Products Sold", df_filtered["product_id"].nunique())

        # st.subheader("📝 Filtered Sales Data")
        st.markdown(
            """
            <style>
                .custom-subheader {
                    font-size: 1.6rem;
                    font-weight: 600;
                    color: #444;
                    margin-top: 1.2rem;
                    margin-bottom: 0.8rem;
                }
            </style>
            <div class="custom-subheader">📝 Filtered Sales Data</div>
            """,
            unsafe_allow_html=True
        )
        

        df_filtered_new = df_filtered.copy()

        # Define the default column order
        default_column_order = ['product_name', 'size', 'SKU(s)', 'unit_price', 'category_name','division_name','7-D','30-D','60-D','90-D','180-D','total_sale']

        df_display = df_filtered_new[default_column_order] 

        # Load previously saved column state
        saved_column_state = load_column_state(store_id)

        if saved_column_state:
            # Extract column order based on colId
            ordered_cols = [col["colId"] for col in saved_column_state if col["colId"] in df_filtered_new.columns]
            df_display = df_filtered_new[ordered_cols]
        else:
            df_display = df_filtered_new[default_column_order]
            
        # 🔹 Configure Ag-Grid for filtering inside 'product_name'
        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_default_column(editable=False, filter='agSetColumnFilter')  # Enable filtering for all columns
        # gb.configure_default_column(resizable=True,width=500)
        for col_id in ["7-D", "30-D", "60-D", "90-D"]:
            gb.configure_column(col_id, width=80, resizable=False)

        gb.configure_column("180-D",width = 110,resizable=False)
        gb.configure_column("total_sale",width = 110,resizable=False)
        gb.configure_column("size",width = 80,resizable=False)
        gb.configure_column("SKU(s)",width = 110,resizable=False)
        gb.configure_column("unit_price",width = 80,resizable=True)
        gb.configure_column("product_name",width = 250,resizable=True)
        

        
        header_renames = {
        "product_name": "Product Name",
        "size": "Size",
        "SKU(s)": "SKU(s)",  # Keep the same or change as needed
        "unit_price": "Unit Price",
        "category_name": "Category Name",
        "division_name": "Division Name",
        "7-D": "7-D",
        "30-D": "30-D",
        "60-D": "60-D",
        "90-D": "90-D",
        "180-D": "180-D",
        "total_sale": "Total Sale"
        }
        # 🔹 Display the DataFrame with interactive filtering
        filter_params = {
        "buttons": ["apply", "clear", "reset", "cancel"],  # Enables Apply, Clear, Reset, Cancel
        "closeOnApply": True  # Closes filter menu after Apply is clicked
        }

        for col_id, header_name in header_renames.items():
            gb.configure_column(col_id, header_name=header_name, filterParams=filter_params,resizable=True)

        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=25)

        # # Apply these filter settings to each column
        # for col in df_display.columns:
        #     gb.configure_column(col, filterParams=filter_params)
        
        # Enable charting features
        gb.configure_grid_options(enableCharts=True, cellSelection=True)
        # Optional: enable range selection
        gb.configure_grid_options(cellSelection =True)

        grid_options = gb.build()

        grid_options["paginationPageSizeSelector"] = [25, 50, 100, 500, 1000]

        grid_options["quickFilterText"] = ""  # Default empty Quick Filter

        # 🔹 Quick Filter Input in Streamlit
        quick_filter_text = st.text_input(label="", placeholder="🔍 Use the search bar to find products across all columns")

        # 🔹 Apply Quick Filter Using Ag-Grid API
        if quick_filter_text:
            grid_options["quickFilterText"] = quick_filter_text  # Set Quick Filter text dynamically
        
        # 🔹 Display the DataFrame with interactive filtering
        grid_response = AgGrid(
            df_display,
            gridOptions=grid_options,
            height=400,
            update_mode=GridUpdateMode.MODEL_CHANGED,  # Prevents rerun on sorting & filtering
            reload_data=False,  # Keeps user interactions intact
            enable_enterprise_modules=True
        )
        
        # Safely try to get the column order
        column_state = grid_response.grid_response.get('columnsState', [])

        if column_state:
            save_column_state(store_id, column_state)

        if st.button("🔄 Reset Column Order"):
            save_column_state(store_id, default_column_state)  # You’ll need to implement this function
            st.rerun()  # This forces the app to rerun and reflect the reset

        # 📥 Download full dataset
        csv_data = df_filtered_new[['product_name', 'size', 'SKU(s)', 'unit_price', 'case_price', 'category_name','division_name','7-D','30-D','60-D','90-D','180-D','total_sale']].to_csv(index=False)
        st.download_button("📥 Download Sales Data", csv_data, "sales_summary.csv", "text/csv")


with tab2:

    # st.subheader("🔥 Top-Selling Products")
    col1, col2 = st.columns([4, 1])

    with col1:
        tooltip_header(
            title="Top-Selling Products",
            tooltip="View the highest-selling products based on total units sold during the selected period.",
            emoji="🔥"
        )
    with col2:
        show_top_sales = st.toggle("Show Top-Selling Products", value=True, key="Key1")

    if df_filtered.empty:
        st.info("ℹ️ No product sales data available for the selected filters.")
    else:
        top_products = df_filtered.groupby("product_name")["total_sale"].sum().reset_index().nlargest(top_n, "total_sale")
        top_products1 = top_products.rename(columns={'product_name': 'Product Name','total_sale':'Total Sold Units'})
        if show_top_sales:
            with st.expander("📝 Data Used in Chart",expanded=True):
                st.dataframe(top_products1.reset_index(), use_container_width=True,hide_index=True)
        
        # Padding for y-axis max
        max_y = top_products["total_sale"].max()
        padded_max_y = ((max_y * 1.35) // 10 + 1) * 10 

        fig_product = px.bar(top_products, x="product_name", y="total_sale",text="total_sale", title=f"🏆 Top {top_n} Products",labels={"product_name": "Product Name", "total_sale": "Total Unit Sold"},color_discrete_sequence=["#536fbf"])
        fig_product.update_layout(
            xaxis_title_font=dict(size=16, family="Arial", color="black", weight="bold"),
            yaxis_title_font=dict(size=16, family="Arial", color="black", weight="bold"),
        )
        fig_product.update_traces(textposition="auto")  # Options: "outside", "inside", "auto"
        fig_product.update_yaxes(range=[0, padded_max_y])
        st.plotly_chart(fig_product, use_container_width=True ,config={
            "displaylogo": False,  # Hide Plotly logo
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d",
                "hoverClosestCartesian", "hoverCompareCartesian",
                "toggleSpikelines"
            ],
            "displayModeBar": True,  # Show mode bar
            "toImageButtonOptions": {
                "format": "png",  # Download as PNG
                "filename": "custom_chart",
                "height": 500,
                "width": 700,
                "scale": 1
            }
        })
        
        st.download_button("📥 Download Top Products Data", top_products.to_csv(index=False), "top_products.csv", "text/csv")


with tab3:

    # Title with inline checkbox
    col1, col2 = st.columns([4, 1])
    with col1:
        tooltip_header(
            title="Low-Selling Products",
            tooltip="View the lowest-selling products based on total units sold during the selected period.",
            emoji="📉"
        )
    with col2:
        show_low_sales = st.toggle("Show Data Table", value=True, key="Key2")

    if df_filtered.empty:
        st.info("ℹ️ No product sales data available for the selected filters.")
    else:
        # If toggle is on, scroll to anchor and show table
        
        # --- Prepare lowest-selling product data ---
        down_products = (
            df_filtered.groupby("product_name")["total_sale"]
            .sum()
            .reset_index()
            .nsmallest(top_n, "total_sale")
        )

        # --- Round to int to avoid decimals like 0.9, 1.2, etc. ---
        down_products["total_sale"] = down_products["total_sale"].round(0).astype(int)
        down_products1 = down_products.rename(columns={'product_name': 'Product Name','total_sale':'Total Sold Units'})
        if show_low_sales:
            
            with st.expander("📝 Data Used in Chart", expanded=True):
                st.dataframe(down_products1, use_container_width=True,hide_index=True)
        # --- Y-axis padding logic ---
        max_y = down_products["total_sale"].max()
        padded_max_y = ((max_y * 1.35) // 10 + 1) * 10

        # --- Bar Chart with text labels ---
        fig_product2 = px.bar(
            down_products,
            x="product_name",
            y="total_sale",
            title=f"📉 Lowest {top_n} Selling Products",
            labels={"product_name": "Product Name", "total_sale": "Total Units Sold"},
            color_discrete_sequence=["#E57373"],  
            text_auto=True  # <-- Add labels on bars
        )

        # --- Text style and positioning ---
        fig_product2.update_traces(
            textfont_size=12,
            textangle=0,
            textposition="outside",  # Options: "inside", "outside", "auto"
            cliponaxis=False  # Ensures text outside bar isn't clipped
        )

        # --- Layout styling ---
        fig_product2.update_layout(
            yaxis_range=[0, padded_max_y],
            xaxis_tickangle=-45,
            xaxis_title_font=dict(size=16, family="Arial", color="black",),
            yaxis_title_font=dict(size=16, family="Arial", color="black",),
            margin=dict(t=60, b=120),
            height=550,
            plot_bgcolor="white",
        )

        # --- Show chart ---
        st.plotly_chart(fig_product2, use_container_width=True, config={
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d",
                "hoverClosestCartesian", "hoverCompareCartesian",
                "toggleSpikelines"
            ],
            "displayModeBar": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "low_selling_chart",
                "height": 500,
                "width": 700,
                "scale": 1
            }
        })
        
        # --- Download CSV ---
        st.download_button(
            "📥 Download Low-Selling Products Data",
            down_products.to_csv(index=False),
            "low_selling_products.csv",
            "text/csv"
        )

with tab4:

    col1, col2 = st.columns([4, 1])
    with col1:
        tooltip_header(
            title="Sales by Category",
            tooltip="Analyze total units sold across different product categories based on the selected filters.",
            emoji="📦"
        )
    with col2:
        show_category_data = st.toggle("Show Data Table", value=True, key="Key3")

    if df_filtered.empty:
        st.info("ℹ️ No category sales data available for the selected filters.")
    else:
        # Step 1: Split category names into lists (only on commas)
        df_filtered["category_name"] = df_filtered["category_name"].astype(str)
        df_filtered["category_list"] = df_filtered["category_name"].str.split(",")  # Split only on comma

        # Step 2: Explode DataFrame to create separate rows
        df_exploded = df_filtered.explode("category_list")

        # Step 3: Trim whitespace from category names
        df_exploded["category_list"] = df_exploded["category_list"].str.strip()

        # Step 4: Aggregate sales by the new category names
        category_sales = df_exploded.groupby("category_list")["total_sale"].sum().reset_index()

        # Step 5: Sort categories by sales in descending order
        category_sales = category_sales.sort_values(by="total_sale", ascending=True)


        if show_category_data:
            with st.expander("📝 Data Used in Chart", expanded=True):
                # st.dataframe(down_products.reset_index(drop=True), use_container_width=True)
                category_sales_reset = (
                    category_sales.sort_values(by="total_sale", ascending=False)
                    .reset_index(drop=True)
                    .assign(**{'S.No.': lambda df: df.index + 1})
                    .rename(columns={'category_list': 'Category Name', 'total_sale': 'Total Units Sold'})
                )
                # Reorder columns to put 'S.No.' first
                category_sales_reset = category_sales_reset[['S.No.'] + [col for col in category_sales_reset.columns if col != 'S.No.']]
                render_centered_table(category_sales_reset)

        # Create bar chart
        fig_category = px.bar(
            category_sales,
            x="total_sale",
            y="category_list",
            orientation="h",
            # title="📊 Sales by Category",
            color="total_sale",
            color_continuous_scale="viridis",  # Better color scheme
            text="total_sale",
        )

        # Update layout for better readability
        fig_category.update_layout(
            xaxis_title="Total Units Sold",
            yaxis_title="Category Name",
            xaxis_title_font=dict(size=16, family="Arial", color="black",weight="bold"),
            yaxis_title_font=dict(size=16, family="Arial", color="black",weight="bold"),
            height=600,  # Adjust height for better spacing
            margin=dict(l=150, r=20, t=50, b=50),  # Adjust margins
        )

        st.plotly_chart(fig_category, use_container_width=True,config={
            "displaylogo": False,  # Hide Plotly logo
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d",
                "hoverClosestCartesian", "hoverCompareCartesian",
                "toggleSpikelines"
            ],
            "displayModeBar": True,  # Show mode bar
            "toImageButtonOptions": {
                "format": "png",  # Download as PNG
                "filename": "custom_chart",
                "height": 500,
                "width": 700,
                "scale": 1
            }
        })

        st.download_button("📥 Download Category Data", category_sales.to_csv(index=False), "category_sales.csv", "text/csv")

with tab5:

    col1, col2 = st.columns([4, 1])

    with col1:
        tooltip_header(
            title="Sales by Division",
            tooltip="Visual representation of total units sold across business divisions using a treemap. Filtered by selected date range and store.",
            emoji="🏢"
        )
    with col2:
        show_division_data = st.toggle("Show Data Table", value=True, key="Key4")
    # st.subheader("🏢 Sales by Division")

    if df_filtered.empty:
        st.info("ℹ️ No division sales data available for the selected filters.")
    else:
        if "division_name" in df_filtered.columns:
            df_filtered["division_name"] = df_filtered["division_name"].astype(str)
            df_filtered["division_list"] = df_filtered["division_name"].str.split(",")  # Split only on comma
            df_exploded = df_filtered.explode("division_list")
            df_exploded["division_list"] = df_exploded["division_list"].str.strip()
            division_sales = df_exploded.groupby("division_list")["total_sale"].sum().reset_index()

            if show_division_data:
                with st.expander("📝 Data Used in Chart", expanded=True):
                    # st.dataframe(down_products.reset_index(drop=True), use_container_width=True)
                    division_sales_reset = (
                        division_sales.sort_values(by="total_sale", ascending=False)
                        .reset_index(drop=True)
                        .assign(**{'S.No.': lambda df: df.index + 1})
                        .rename(columns={'division_list': 'Division Name', 'total_sale': 'Total Units Sold'})
                    )
                    # Reorder columns to put 'S.No.' first
                    division_sales_reset = division_sales_reset[['S.No.'] + [col for col in division_sales_reset.columns if col != 'S.No.']]
                    render_centered_table(division_sales_reset)

            # Create treemap chart
            fig_division = px.treemap(
                division_sales,
                path=["division_list"],
                values="total_sale",
                color="total_sale",
                color_continuous_scale="greens",  # You can change the color scheme
            )

            st.plotly_chart(fig_division, use_container_width=True,config={
            "displaylogo": False,  # Hide Plotly logo
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d",
                "hoverClosestCartesian", "hoverCompareCartesian",
                "toggleSpikelines"
            ],
            "displayModeBar": True,  # Show mode bar
            "toImageButtonOptions": {
                "format": "png",  # Download as PNG
                "filename": "custom_chart",
                "height": 500,
                "width": 700,
                "scale": 1
            }
        })
            st.download_button("📥 Download Division Data", division_sales.to_csv(index=False), "division_sales.csv", "text/csv")
        else:
            st.warning("⚠️ No division data available.")

# Tab 6: Sales Trend Analysis
with tab6:
    # --- Tooltip Header ---
    tooltip_header(
        title="Sales Trend Analysis",
        tooltip="Track how sales performance changes over time. Group data by day, week, or month to spot trends, spikes, or drops in sales.",
        emoji="📈"
    )

    diff = end_date - start_date 
    date_diff = diff.days + 1
    default_view = None

    if df_filtered.empty:
        st.info("ℹ️ No sales trend data available for the selected filters.")
        placeholder.empty()
    else:
        # --- In-Tab Trend Settings ---
        with st.container():
            col1, col2 = st.columns([2, 1])

            with col1:
                # Dynamically determine grouping options based on date range
                if date_diff <= 7:
                    view_options = ["Day"]
                    default_view = "Day"
                elif date_diff <= 30:
                    view_options = ["Day", "Week"]
                    default_view = "Week"
                else:
                    view_options = ["Day", "Week", "Month"]
                    default_view = "Month"

                date_grouping = st.radio(
                    "How would you like to view the sales trend?",
                    view_options,
                    index=view_options.index(default_view),
                    horizontal=True,
                )

            with col2:
                show_data_table = st.toggle("Show Data Table", value=True,key="Key5")

        # --- Prepare Data ---
        df_filtered_new["date"] = pd.to_datetime(df_filtered_new["date"])

        if date_grouping == "Day":
            df_filtered_new["period"] = df_filtered_new["date"].dt.date
        elif date_grouping == "Week":
            df_filtered_new["period"] = df_filtered_new["date"].dt.to_period("W").apply(lambda r: r.start_time.date())
        elif date_grouping == "Month":
            df_filtered_new["period"] = df_filtered_new["date"].dt.to_period("M").apply(lambda r: r.start_time.date())

        trend_df = (
            df_filtered_new.groupby("period")["total_sale"]
            .sum()
            .reset_index()
            .sort_values("period")
        )
        trend_df["period"] = pd.to_datetime(trend_df["period"])
        trend_df = trend_df.reset_index(drop=True)
        trend_df = trend_df.loc[:, ~trend_df.columns.str.startswith('Unnamed')]
        trend_df1 = trend_df.rename(columns={'period': 'Time Period','total_sale':'Total Sold Units'})
        # --- Optional Data Table ---
        if show_data_table:
            with st.expander("📋 Sales Trend Data Table",expanded=True):
                st.dataframe(trend_df1, use_container_width=True,hide_index=True)

        # --- Generate tooltip labels based on period range ---
        if date_grouping == "Day":
            trend_df["label"] = trend_df["period"].dt.strftime("%d %b %Y")
            chart_type = "line"
        elif date_grouping == "Week":
            trend_df["end_period"] = trend_df["period"] + pd.Timedelta(days=6)
            trend_df["label"] = trend_df["period"].dt.strftime("%d %b") + " - " + trend_df["end_period"].dt.strftime("%d %b")
            chart_type = "bar"  # Use bar chart for week
        elif date_grouping == "Month":
            trend_df["end_period"] = trend_df["period"] + pd.offsets.MonthEnd(0)
            trend_df["label"] = trend_df["period"].dt.strftime("%b %Y")
            chart_type = "bar"  # Use bar chart for month

        # --- Chart: Sales Over Time ---
        st.markdown("#### 📊 Sales Over Time")

        if chart_type == "line":
            fig = px.line(
                trend_df,
                x="period",
                y="total_sale",
                markers=True,
                line_shape="spline",
                title="Sales Trend",
                labels={"period": "Date", "total_sale": "Total Sales"},
                hover_data={"label": True, "total_sale": True}
            )
            fig.update_traces(line=dict(color="royalblue", width=3))
        else:
            fig = px.bar(
                trend_df,
                x="period",
                y="total_sale",
                title="Sales Trend",
                text_auto=True,
                labels={"period": "Date", "total_sale": "Total Sales"},
                hover_data={"label": True, "total_sale": True}
            )
            fig.update_traces(marker_color="royalblue", marker_line_width=0)

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Total Sales (unit)",
            yaxis_title_font=dict(size=16, family="Arial", color="black"),
            hovermode="x unified",
            height=450,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        st.plotly_chart(fig, use_container_width=True)

        csv = trend_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Trend Data as CSV",
            data=csv,
            file_name="sales_trend.csv",
            mime="text/csv"
        )

# Remove the loader and show the main content
placeholder.empty()