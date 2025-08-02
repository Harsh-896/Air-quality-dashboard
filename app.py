import streamlit as st 
import pandas as pd
import mysql.connector
import altair as alt
import plotly.express as px
from pytrends.request import TrendReq
from dotenv import load_dotenv
import os

# Load environment variables from .env \
load_dotenv()

# Set page title
st.set_page_config(page_title="Static SQL Viewer", layout="wide")
st.title("📊 AQI Query Result Dashboard")

# Connect to MySQL using env vars
try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT", 3306))
    )
    cursor = conn.cursor()
    st.success("Connected to Our MY SQL Database")
except Exception as e:
    st.stop()
    
# Sidebar: Database Explorer
st.sidebar.title("Database Explorer")

try:
    # Fetch list of tables from MySQL
    cursor.execute("SHOW TABLES")
    all_tables = [row[0] for row in cursor.fetchall()]

    # Filter only target tables
    target_tables = {"population_projection", "aqi", "idsp", "vahan"}
    tables = [table for table in all_tables if table in target_tables]

    if tables:
        st.sidebar.subheader("Available Tables (Filtered)")
        st.sidebar.table(pd.DataFrame(tables, columns=["Table Name"]))

        # Dropdown to select a table
        selected_table = st.sidebar.selectbox("Select a table to view", tables)

        # Preview the selected table (limit rows)
        st.title(f"Table Preview: `{selected_table}`")
        preview_query = f"SELECT * FROM `{selected_table}` LIMIT 100"
        df = pd.read_sql(preview_query, conn)
        st.dataframe(df)

    else:
        st.sidebar.info("None of the specified tables found in the connected database.")

except Exception as e:
    st.sidebar.error(f"Error fetching tables: {e}")
    st.stop()

# Section 1: Stored Procedure - Statewise AQI Dates
st.title("Statewise AQI Records")

try:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT state FROM aqi ORDER BY state;")
    states = [row[0] for row in cursor.fetchall()]
    cursor.close()
except Exception as e:
    st.error(f"Error loading states: {e}")
    st.stop()

selected_state = st.selectbox("Select a State:", states)

if st.button("Execute Stored Procedure"):
    try:
        cursor = conn.cursor()
        cursor.callproc("air_quality_status_by_Statewise", [selected_state])

        for result in cursor.stored_results():
            df = pd.DataFrame(result.fetchall(), columns=[col[0] for col in result.description])
            st.success(f"AQI data for '{selected_state}' loaded successfully.")
            st.dataframe(df)
    except Exception as e:
        st.error(f"Error executing stored procedure: {e}")
    finally:
        cursor.close()

# Section 2 : Top 5 vs Bottom 5 States by AQI
st.title("Top 5 vs Bottom 5 States by AQI Level ")

try:
    with open("aqi1.sql", "r") as file:
        query = file.read()
    df = pd.read_sql(query, conn)

    if 'category' in df.columns:
        top_df = df[df['category'] == 'Top']
        bottom_df = df[df['category'] == 'Bottom']
    else:
        top_df = df.iloc[:5]
        bottom_df = df.iloc[5:]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 States with Highest AQI")
        st.dataframe(top_df)
        st.bar_chart(top_df.set_index("area")["avg_val"])

    with col2:
        st.subheader("Bottom 5 States with Lowest AQI")
        st.dataframe(bottom_df)
        st.bar_chart(bottom_df.set_index("area")["avg_val"])

except Exception as e:
    st.error(f"Failed to load Top/Bottom AQI data: {e}")


# Section 3: Top 10 States with Worst AQI (by Month)
st.title("Top 10 States with Highest AQI by Month")

try:
    with open("aqi4.sql", "r") as file:
        query = file.read()
    df = pd.read_sql(query, conn)
    st.success("Query executed successfully.")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load AQI data: {e}")


# Section 4: Most Reported Disease Illnesses
st.title("Top 2 Most Reported Disease Illnesses")

try:
    with open("disease.sql", "r") as file:
        query = file.read()
    df = pd.read_sql(query, conn)
    st.success("Query executed successfully.")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load disease data: {e}")

# Section 5: AQI Comparison - Weekends vs Weekdays
st.title("AQI Levels: Weekends vs Weekdays in Metro Cities")
st.subheader("📈 AQI Levels: Weekend vs Weekday by State")

try:
    with open("aqi6.sql", "r") as file:
        query = file.read()

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("Query returned no results. Please check the data or filters.")
    else:
        # 🔍 Ensure day_type is categorical (Weekday/Weekend)
        df["day_type"] = df["day_type"].astype("category")

        # Bar chart 
        chart =  alt.Chart(df).mark_bar().encode(
        x=alt.X("state:N",title="State", axis=alt.Axis(labelFontWeight="bold", titleFontWeight="bold")),
        y=alt.Y("avg_aqi:Q",title="Average AQI",axis=alt.Axis(labelFontWeight="bold", titleFontWeight="bold")),
            color=alt.Color("day_type:N",scale=alt.Scale(scheme="reds"), title="Day Type"),
            column=alt.Column("day_type:N", title="Day Type"),
            tooltip=["state", "day_type", "avg_aqi"]
        ).properties(width=150, height=400)

        st.altair_chart(chart, use_container_width=True)
        st.dataframe(df)

except Exception as e:
    st.error(f"Failed to load weekend/weekday AQI data: {e}")

# section 6 : EV Adoption vs AQI Comparison
st.title(" EV Adoption vs AQI Comparison")
try:
    with open("ev.sql", "r") as file:
        query = file.read()
    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("No data returned. Check your tables or filters.")
    else:
        st.success("Query executed successfully.")
        st.dataframe(df)

        # Group-wise AQI comparison
        group_avg = df.groupby("group_type")["avg_aqi"].mean().reset_index()

        st.subheader("📊 Average AQI by Group")
        st.bar_chart(group_avg.set_index("group_type")['avg_aqi'])

        # Optional: display both group data separately
        st.subheader("Top 5 EV States AQI")
        st.dataframe(df[df["group_type"] == "Top 5 EV States"])

        st.subheader("Other States AQI")
        st.dataframe(df[df["group_type"] == "Other States"])


        # Pie Chart for AQI Share by Group using Plotly
        st.subheader("Pie Chart: Average AQI Share by Group (with Labels)")
        import plotly.express as px

        pie_fig = px.pie(  group_avg,
            names='group_type',
            values='avg_aqi',
            color='group_type',
            color_discrete_map={
                "Top 5 EV States": "#0057B7",
                "Other States": "#89CFF0"
            },
            hole=0.4
        )

        pie_fig.update_traces(textinfo='percent+label')
        pie_fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(pie_fig, use_container_width=True)

except Exception as e:
    st.error(f"Error executing or displaying query: {e}")




# Section 7:  Statewise Risk AQI Record
st.title("Top 2 city in AQI degradation in 2024-2025")
st.text("Which Tier 1/2 cities show irreversible AQI degradation? ")
try:
    with open("aqi7.sql", "r") as file:

        query = file.read()
    df = pd.read_sql(query, conn)
    st.success("Query executed successfully.")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load disease data: {e}")


@st.cache_data
def fetch_google_trends(keyword="Air Purifier"):
    pytrends = TrendReq()
    pytrends.build_payload([keyword], timeframe='today 3-m', geo='IN')
    df = pytrends.interest_by_region()
    df = df.sort_values(by=keyword, ascending=False).reset_index()
    df.columns = ['Region', 'Search Interest']
    return df

# Secyion 8:  Statewise Risk AQI Record

st.title("📊 Statewise Risk AQI Record")

# Step 1: Load list of states from population_projection table
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT DISTINCT state FROM population_projection ORDER BY state;")
        states = [row[0] for row in cursor.fetchall()]
except Exception as e:
    st.error(f"❌ Failed to fetch states: {e}")
    st.stop()

# Step 2: Sidebar dropdown to select a state
selected_state = st.selectbox("Select a State", states)

# Step 3: Execute stored procedure and show results
try:
    cursor = conn.cursor()
    cursor.callproc("risk_score_by_state", [selected_state])

    # Fetch result from stored procedure
    for result in cursor.stored_results():
        df = pd.DataFrame(result.fetchall(), columns=[col[0] for col in result.description])

    cursor.close()

    # Step 4: Display table
    if not df.empty:
        st.success(f" Risk Score Data for '{selected_state}' loaded successfully.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No data returned for selected state.")

except Exception as e:
    st.error(f" Error executing stored procedure: {e}")





# Sextion 9: Google Search Interest for 'Air Purifier' (Past 3 Month)

st.title(" Additional Market Reserch")
st.subheader(" Google Search Interest for 'Air Purifier' (Past 3 Months)")
trends_df = fetch_google_trends()

st.dataframe(trends_df.head(15))

trends_chart = alt.Chart(trends_df.head(15)).mark_bar().encode(
    x=alt.X('Region', sort='-y'),
    y='Search Interest',
    color='Region'
).properties(title="Top Regions by Google Search Interest", width=700)
st.altair_chart(trends_chart)

# Footer
st.markdown("---")
st.caption("Developed by Harsh Choudhary | Data from internal metrics + Google Trends API")



