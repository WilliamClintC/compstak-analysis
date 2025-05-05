import streamlit as st
import pandas as pd

# ---- Inline dataset ----
data = [
    {"Field": "GDP", "Definition": "Gross Domestic Product", "Main Category": "Economics", "Subcategory": "Macro"},
    {"Field": "CPI", "Definition": "Consumer Price Index", "Main Category": "Economics", "Subcategory": "Macro"},
    {"Field": "Demand", "Definition": "Consumer demand", "Main Category": "Economics", "Subcategory": "Micro"},
    {"Field": "OLS", "Definition": "Ordinary Least Squares", "Main Category": "Statistics", "Subcategory": "Regression"},
    {"Field": "t-test", "Definition": "Statistical hypothesis test", "Main Category": "Statistics", "Subcategory": "Inference"},
    {"Field": "Variance", "Definition": "Spread of values", "Main Category": "Statistics", "Subcategory": "Descriptive"},
]

# ---- Convert to DataFrame ----
df = pd.DataFrame(data)

# ---- Sidebar: Select main category ----
main_categories = sorted(df['Main Category'].unique())
selected_category = st.sidebar.selectbox("Select Main Category", main_categories)

# ---- Filtered table ----
filtered_df = df[df['Main Category'] == selected_category]

# ---- App title ----
st.title("📘 Field Definitions Viewer")

# ---- Header ----
st.markdown(f"### Showing fields in **{selected_category}**")

# ---- Highlighting function ----
def highlight_selected(row):
    return ['background-color: #e0f7e0'] * len(row) if row['Main Category'] == selected_category else [''] * len(row)

# ---- Display filtered + highlighted table ----
st.dataframe(
    filtered_df.style.apply(highlight_selected, axis=1),
    use_container_width=True
)
