import streamlit as st
import pandas as pd
from pathlib import Path


# ## Connect Server:
# SQL_SERVER = "10.2.200.7"
# SQL_DATABASE = "sanpham"
# SQL_USERNAME = "sp_khanhhp2"
# SQL_PASSWORD = "Abcd@1234"
#
# def get_connection():
#
#     connection_string = (
#         "DRIVER={ODBC Driver 18 for SQL Server};"
#         f"SERVER={SQL_SERVER};"
#         f"DATABASE={SQL_DATABASE};"
#         f"UID={SQL_USERNAME};"
#         f"PWD={SQL_PASSWORD};"
#         "Encrypt=yes;"
#         "TrustServerCertificate=yes;"
#         "Connection Timeout=10;"
#     )
#
#     conn = pyodbc.connect(connection_string)
#
#     return conn



# CONNECT DATA
EXCEL_FILE = Path(__file__).resolve().parent / "Data.xlsx"

@st.cache_data
def get_data():
    df = pd.read_excel(EXCEL_FILE)
    return df

# BUILD UI:
st.set_page_config(
    page_title="F88 Policy Management",
    page_icon="📋",
    layout="wide"
)

st.html("""
<style>
    .header_bg {
        background-color: #24496D;
        height: 115px;
        padding-left: 25px;
        border-left: 6px solid #F47B20;
    }
    
    .header_title {
        text-align: left;
        padding: 10px;
        margin-left: 25px;
        vertical-align: top;
        color: white;
    }
    
    .header_subtitle {
        text-align: left;
        font-size: 14px;
        margin: 8px 0 0 0;
        color: white;
    }
</style>

<div class="header_bg">
     <h1 class="header_title">PHÒNG PHÁT TRIỂN SẢN PHẨM</h1>
    <p class="header_subtitle">Công cụ tra các điều chỉnh-thay đổi chính sách sản phẩm</p>
</div>

""")

# Create Filter Area:
df = get_data()

## Create Filter Container:
with st.container(border=True):
    st.html("""
    <style> 
        .filter-cont {
        background-color: #24496D;
        font-size: 14px;
        font-weight: bold;
        color: white;
        padding: 6px 15px;
        margin-left: -10px;
        margin_top: -10px;
        }
    </style>
    
    <div class="filter-cont">
    Bộ lọc 
    </div>
    """)


## Create FilterBox:
    with st.form(key="policy_search_form"):

        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)

        with col1:
            filter_a = st.selectbox(
        "Tháng ban hành",
        options = ["ALL"] + df["APPLIED_MONTH"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder = "Lọc tháng ban hành",
        key = 'filter_a'
    )

        with col2:
            filter_b = st.selectbox(
        "Loại tài sản",
        options = ["ALL"] + df["ASSET"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc tài sản",
        key = 'filter_b'
    )

        with col3:
            filter_c = st.selectbox(
        "Status",
        options = ["ALL"] + df["STATUS"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc trạng thái",
        key = 'filter_c'
    )

        with col4:
            filter_d = st.selectbox(
        "Loại khách hàng",
        options = ["ALL"] + df["CUSTOMER_TYPE"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc loại khách hàng",
        key = 'filter_d'
    )

        with col5:
            filter_e = st.selectbox(
        "Nguồn",
        options = ["ALL"] + df["FUND"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc nguồn",
        key = 'filter_e'
    )

        with col6:
            filter_f = st.selectbox(
        "Sản phẩm",
        options = ["ALL"] + df["NHOM_SP"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc sản phẩm",
        key = 'filter_f'
    )

        with col7:
            filter_g = st.selectbox(
        "Loại quyết định",
        options = ["ALL"] + df["POLICY_TYPE"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc loại quyết định",
        key = 'filter_g'
    )

        with col8:
            filter_h = st.selectbox(
        "Đơn vị sở hữu",
        options = ["ALL"] + df["DEPARTMENT"].dropna().unique().tolist(),
        label_visibility = "visible",
        index=None,
        placeholder="Lọc đơn vị sở hữu",
        key = 'filter_h'
    )

        search = st.form_submit_button(
        "Tra cứu",
        type="primary"
    )
if search:
    df_filter = df.copy()
    filter_mapping = {
        "APPLIED_MONTH": filter_a,
        "ASSET": filter_b,
        "STATUS": filter_c,
        "CUSTOMER_TYPE": filter_d,
        "FUND": filter_e,
        "NHOM_SP": filter_f,
        "POLICY_TYPE": filter_g,
        "DEPARTMENT": filter_h
    }
    for col, choice in filter_mapping.items():
        if choice is not None:
            df_filter = df_filter[df_filter[col] == choice]

## Create Info Container:
with st.container(border=True):
    st.html("""
    <style> 
        .filter-cont {
        background-color: #24496D;
        font-size: 14px;
        font-weight: bold;
        color: white;
        padding: 6px 15px;
        margin-left: -10px;
        margin_top: -10px;
        }
    </style>

    <div class="filter-cont">
    Thông tin chi tiết
    </div>
    """)

    if search:
        countpolicy = df_filter['POLICY_ID'].nunique()
        df_display = df_filter.drop_duplicates(
            subset=["POLICY_ID"]
        )

        st.metric(
            label="Tổng số quyết định",
            value=countpolicy,
        )

        st.dataframe(
            df_display,
            column_order=[
                "POLICY_NAME",
                "APPLIED_DATE",
                "DEPARTMENT",
                "PIC",
                "POLICY_TYPE"
            ],
            column_config={
                "POLICY_NAME": "Tên quyết định",
                "APPLIED_DATE": "Ngày ban hành",
                "DEPARTMENT": "Đơn vị ban hành",
                "PIC": "Người phụ trách",
                "POLICY_TYPE": "Loại quyết định",
            },
            use_container_width=True,
            hide_index=True
        )



