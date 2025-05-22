import streamlit as st
#st.set_page_config(layout = 'wide')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Set page config (optional)
st.set_page_config(page_title="Nutrition App", layout="wide")

# Function to load and encode local jpg image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Local image filename (same folder)
image_file = 'iii.jpg'

# Get base64 string
img_base64 = get_base64_of_bin_file(image_file)

# Inject HTML + CSS for background
page_bg_img = f"""
<style>
.stApp {{
  background-image: url("data:image/jpg;base64,{img_base64}");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}}
</style>
"""

# Load CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

import mysql.connector

conn = mysql.connector.connect(
    host      ="localhost",
    user      ="root",
    password  ="Sudhan140695@",
    database  = "project2"
    
)
cursor = conn.cursor()
print("MySQL connection established!")


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Project Introduction", "Plots", "SQL Queries", "Suggestions" , "Creator Info"])

# -------------------------------- PAGE 1: Introduction --------------------------------
if page == "Project Introduction":
    st.title("⚖️ Nutrition Paradox: A Global View on Obesity and Malnutrition")
    st.subheader("📊 A Streamlit App for a Global View on Obesity and Malnutrition Insights")
    st.write("""
    **This project analyzes Obesity and Malnutrition Insights data from different Years using an MySQL database :-**

    ●  Nutrition Risk Monitoring: Identify countries with extremely high obesity or malnutrition
    levels, flagging them for public health intervention\n
    ● Demographic Disparity Analysis: Understand how gender and age groups contribute
    differently to obesity and malnutrition statistics.\n
    ● Data-Driven Policy Planning: Help policymakers prioritize regions for funding and
    nutrition-related programs based on multi-dimensional data.\n
    ● Comparative Region Analysis: Enable researchers to compare regional trends and
    draw correlations between health indicators and socio-economic conditions.\n  
    ● Public Health Reporting: Provide government or NGOs with a summarized SQL 
    dashboard showing country-level nutrition trends.

    **Features:**
    - View and filter Nutrition data by Country, Region, Year, etc,.
    - Generate dynamic visualizations.
    - Run predefined SQL queries to explore insights.

    **Database Used:** `project2`
    """)
    st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\images (11).jpeg', width=152)

# -------------------------------- PAGE 2: Plots --------------------------------
elif page == "Plots":
    
    st.title("Obesity & Malnutrition Dashboard")
    "\n"
    "\n"
    "\n"

    obesity = "select * from obesity"
    malnutrition = "select * from malnutrition"

    obesity_df = pd.read_sql(obesity,conn)
    malnutrition_df = pd.read_sql(malnutrition,conn)

    pl = st.sidebar.radio("Choose Options", ["Filtered Plots", "Plots"])
    
    if pl == "Filtered Plots":
    
        
        # Sidebar filters
        countries = sorted(obesity_df['Country'].unique())
        years = sorted(obesity_df['Year'].unique())
        
        selected_country = st.sidebar.selectbox("Select a Country", countries)
        selected_year_range = st.sidebar.slider("Select Year Range", min_value=min(years), max_value=max(years),
                                                value=(min(years), max(years)))
        
        # Filtered Data
        filtered_obesity = obesity_df[
            (obesity_df['Country'] == selected_country) &
            (obesity_df['Year'] >= selected_year_range[0]) &
            (obesity_df['Year'] <= selected_year_range[1])
        ]
        
        filtered_malnutrition = malnutrition_df[
            (malnutrition_df['Country'] == selected_country) &
            (malnutrition_df['Year'] >= selected_year_range[0]) &
            (malnutrition_df['Year'] <= selected_year_range[1])
        ]
        
        # Plot 1: Obesity Trend
        st.header(f"Obesity Trend in {selected_country} ({selected_year_range[0]}–{selected_year_range[1]})")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=filtered_obesity, x="Year", y="Mean_Estimate", hue="Gender", marker="o", ax=ax1)
        ax1.set_title("Obesity Estimate Over Time")
        ax1.set_ylabel("Mean Estimate")
        st.pyplot(fig1)
        st.markdown("""## Client Summary : """)
        st.markdown("""
        ### This plot reveals the historical obesity trend in the selected country. You can clearly see if obesity is rising or falling over the years. The color-coded lines allow comparison between male and female obesity levels, highlighting gender-specific health disparities.
        """)
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"

        
        # Plot 2: Malnutrition Trend
        st.header(f"Malnutrition Trend in {selected_country} ({selected_year_range[0]}–{selected_year_range[1]})")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=filtered_malnutrition, x="Year", y="Mean_Estimate", hue="Gender", marker="o", ax=ax2)
        ax2.set_title("Malnutrition Estimate Over Time")
        ax2.set_ylabel("Mean Estimate")
        st.pyplot(fig2)
        st.markdown("""## Client Summary : """)
        st.markdown("""
        ### This visualization shows how malnutrition estimates have evolved. A rising trend may signal worsening food insecurity, while a decline suggests improved nutrition access. The comparison by gender can reveal if interventions are reaching both males and females equitably.
        """)
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        
        # Plot 3: Obesity vs Malnutrition Comparison
        st.header(f"Obesity vs Malnutrition in {selected_country}")
        merged = filtered_obesity[["Year", "Mean_Estimate"]].rename(columns={"Mean_Estimate": "Obesity"}).merge(
            filtered_malnutrition[["Year", "Mean_Estimate"]].rename(columns={"Mean_Estimate": "Malnutrition"}), 
            on="Year"
        )
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        sns.scatterplot(data=merged, x="Obesity", y="Malnutrition", s=100, ax=ax3)
        ax3.set_title("Obesity vs Malnutrition")
        st.pyplot(fig3)
        st.markdown("""## Client Summary : """)
        st.markdown("""
        ### This plot shows whether higher obesity is associated with lower or higher malnutrition in the same country and time range. In some cases, you may find both rising (indicating a double burden of malnutrition), or an inverse relationship (suggesting nutritional transitions).
        """)
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"


    elif pl == "Plots":

        # 1. Heatmap: Obesity Mean by Country and Year
       
        
        st.subheader("Obesity Heatmap (Mean Estimate by Country & Year)")
        pivot = obesity_df.pivot_table(values="Mean_Estimate", index="Country", columns="Year")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt=".1f", ax=ax)
        ax.set_title("Obesity Estimates Heatmap")
        st.pyplot(fig)
        st.text('Purpose :')
        st.text('Easily spot changes in obesity levels over time by country.')
        "\n"
        "\n"
        "\n"
        st.text('Client Summary :')
        st.text("""
        The obesity heatmap provides a visual representation of the mean
        estimate of obesity levels across various countries from 2012 to 
        2022. The data reveals a concerning trend of increasing obesity
        levels in many countries, with some regions exhibiting more 
        pronounced changes.
       """)
        "\n"
        "\n"
        "\n"

        
        # 2. Box Plot: CI_Width by Gender
        
        st.subheader("CI_Width Distribution by Gender (Obesity)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=obesity_df, x="Gender", y="CI_Width", palette="Set2", ax=ax)
        ax.set_title("Confidence Interval Width by Gender")
        st.pyplot(fig)
        st.text('Purpose :')
        st.text('Compare variability (confidence interval width) between genders.')
        "\n"
        "\n"
        "\n"
        st.text('Client Summary :')
        st.text("""
        This plot shows that males have the highest variability in 
        confidence interval (CI) widths for obesity, followed by females. 
        The 'Both' gender group shows the least variability, indicating 
        more consistent estimates.
       """)
        "\n"
        "\n"
        "\n"
         
        # 3. Box Plot: CI_Width by Gender
        
        st.subheader("CI_Width Distribution by Gender (Malnutrition)")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=malnutrition_df, x="Gender", y="CI_Width", palette="Set2", ax=ax)
        ax.set_title("Confidence Interval Width by Gender")
        st.pyplot(fig)
        st.text('Purpose :')
        st.text('Compare variability (confidence interval width) between genders.')
        "\n"
        "\n"
        "\n"
        st.text('Client Summary :')
        st.text("""
        This plot shows that the confidence interval (CI) width 
        for malnutrition varies by gender, with males generally 
        having wider CIs and more variability. The lowest variability 
        is observed in the "Both Gender" group.
       """)
        "\n"
        "\n"
        "\n"
        
        # 4. Pair Plot: CI_Width vs. Mean_Estimate (Obesity)

        st.subheader("Pair Plot: Obesity Confidence & Estimate")
        fig = sns.pairplot(obesity_df[['Mean_Estimate', 'CI_Width']], kind="scatter")
        st.pyplot(fig)
        st.text('Purpose :')
        st.text('Understand correlation between CI and estimate values.')
        "\n"
        "\n"
        "\n"
        st.text('Client Summary :')
        st.text("""
        This plot appears to be analyzing the relationship between 
        the mean estimate of Obesity and the confidence interval (CI) width. 
        The plot is divided into four quadrants, each displaying 
        a different aspects of the data.
       """)
        "\n"
        "\n"
        "\n"




# -------------------------------- PAGE 3: SQL Queries --------------------------------

elif page == "SQL Queries":
    st.title("📋 SQL Query Results")

    def get_data(query, params=None):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sudhan140695@",
            database="project2"
        )
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df

    obesity_queries = {
        "1. Top 5 regions with the highest average obesity levels in the most recent year(2022) " : " select Region, avg(Mean_Estimate) as 'Avg obesity' from obesity where Year = 2022 group by Region order by avg(Mean_Estimate) desc limit 5;",
        "2. Top 5 countries with highest obesity estimates :  " : " select Country, avg(Mean_Estimate) as 'obesity estimates' from obesity group by Country order by avg(Mean_Estimate) desc limit 5;",
        "3. Obesity trend in India over the years(Mean_estimate) " : "select Country, Year, avg(Mean_Estimate) as 'obesity trend' from obesity where Country = 'India' group by Year order by Year asc;",
        "4. Average obesity by gender " : "select Gender, avg(Mean_Estimate) 'Avg Obesity'  from obesity group by Gender;",
        "5. Country count by obesity level category and age group " : "select count(Country) 'Country Count', age_group, Obesity_level from obesity group by age_group, Obesity_level;",
        "6. Top 5 countries least reliable countries(with highest CI_Width) " : "select Country, avg(CI_width) as least_reliable_countries from obesity group by Country order by least_reliable_countries desc limit 5;",
        "7. Top 5 most consistent countries (smallest average CI_Width) " : "select Country, avg(CI_width) as consistent_countries from obesity group by Country order by consistent_countries asc limit 5",
        "8. Average obesity by age group" : "select age_group, Avg(Mean_Estimate) 'Avg Obesity' from obesity group by age_group;",
        "9. Top 10 Countries with consistent low obesity (low average + low CI)over the years" : "select Country, avg(Mean_Estimate) as Avg_Obesity, avg(CI_Width) as Avg_CI_Width from obesity group by Country order by Avg_Obesity asc, Avg_CI_Width asc Limit 10;",
        "10. Countries where female obesity exceeds male by large margin (same year) " : "select f.Country, f.Year, f.Region, f.age_group, f.Mean_Estimate as Female_Obesity, m.Mean_Estimate as Male_Obesity,  (f.Mean_Estimate - m.Mean_Estimate) as Obesity_Difference from obesity f join obesity m  on f.Country = m.Country and f.Year = m.Year and f.Region = m.Region and  f.age_group =  m.age_group where f.Gender = 'Female' and m.Gender = 'Male' and  (f.Mean_Estimate - m.Mean_Estimate) > 5 order by Obesity_Difference desc;",
        "11. Global average obesity percentage per year  " : "select Country, avg(Mean_Estimate) 'Avg Obesity', year from obesity where Country = 'Global' group by Country, year order by year asc;"
                  }
        
    malnutrition_queries = {
            "1. Avg. malnutrition by age group " : " select age_group, avg(Mean_Estimate) 'Avg malnutrition' from malnutrition group by age_group;",
            "2. Top 5 countries with highest malnutrition(mean_estimate)  " : " select Country, avg(Mean_Estimate) as 'Mean_Estimate' from malnutrition group by Country order by avg(Mean_Estimate) desc limit 5;",
            "3. Malnutrition trend in African region over the years " : "select Region, Year, avg(Mean_Estimate) as 'Malnutrition_trend' from malnutrition where Region = 'Africa' group by Year order by Year asc;",
            "4. Gender-based average malnutrition " : "select Gender, avg(Mean_Estimate) as Avg_Mean_Estimate from malnutrition group by Gender;",
            "5. Malnutrition level-wise (average CI_Width by age group)  " : "select age_group, avg(CI_Width) as Avg_CI_Width from malnutrition group by age_group;",
            "6. Yearly malnutrition change in specific countries(India, Nigeria, Brazil) " : "select Country, Year, avg(Mean_Estimate) as malnutrition from malnutrition where Country in ('India','Nigeria','Brazil') group by Country, year order by Country, Year asc;",
            "7. Regions with lowest malnutrition averages " : "select Region, avg(Mean_Estimate) as Lowest_Malnutrition_Avg from malnutrition group by Region order by avg(Mean_Estimate) asc;",
            "8. Countries with increasing malnutrition " : "select Country, Min(Year) as Start_Year, Max(Year) as End_Year, Min(Mean_Estimate) as Earliest_Mean, Max(Mean_Estimate) as Latest_Mean, (Max(Mean_Estimate) - Min(Mean_Estimate)) as Increase from malnutrition group by Country having Latest_Mean > Earliest_Mean order by Increase desc;",
            "9. Min/Max malnutrition levels year-wise comparison" : "select Year,avg(UpperBound) as Max_Malnutrition_Avg, avg(LowerBound) as Min_Malnutrition_Avg, avg(UpperBound)-avg(LowerBound)  as Min_Max_Comparison from malnutrition group by Year order by Year asc;",
            "10. High CI_Width flags for monitoring(CI_width > 5) " : "select Region, Year, CI_Width from malnutrition where CI_Width > 5 order by CI_Width desc;"
                   }
        
        
    combined_queries = {
            "1. Obesity vs malnutrition comparison by country(any 5 countries) " : "select A.Country as 'Country', A.Region as 'Region', A.Year as 'Year', avg(A.Mean_Estimate) as 'Obesity_Mean_Estimate', avg(B.Mean_Estimate) as 'Malnutrition_Mean_Estimate'  from obesity A join malnutrition B on A.Country = B.Country and A.Year = B.Year where A.Country in ('India','Iraq','Afghanistan','Zimbabwe','Canada') group by A.Country, A.Region, A.Year order by A.Country, A.Year Asc;",
            "2. Gender-based disparity in both obesity and malnutrition alter  " : " select A.Region as 'Region', A.Gender as 'Gender', avg(A.Mean_Estimate) as 'Obesity_Mean_Estimate', avg(B.Mean_Estimate) as 'Malnutrition_Mean_Estimate' from obesity A join malnutrition B on A.Country = B.Country and A.Gender = B.Gender group by A.Region, A.Gender order by A.Region, A.Gender Asc;",
            "3. Region-wise avg estimates side-by-side(Africa and America) " : "select A.Region as 'Region', A.Country as 'Country', avg(A.Mean_Estimate) as 'Obesity_Mean_Estimate', avg(B.Mean_Estimate) as 'Malnutrition_Mean_Estimate'  from obesity A join malnutrition B on A.Country = B.Country and A.Region = B.Region where A.Region in ('Africa', 'Americas') group by A.Country, A.Region order by A.Region Asc;",
            "4. Countries with obesity up & malnutrition down " : "select A.Country as 'Country', min(A.Mean_Estimate) as 'Obesity_Earliest', max(A.Mean_Estimate) as 'Obesity_Latest', min(B.Mean_Estimate) as 'Malnutrition_Earliest', max(B.Mean_Estimate) as 'Malnutrition_Latest' from obesity A join malnutrition B on A.Country = B.Country and A.Year = B.Year group by A.Country having Obesity_Latest > Obesity_Earliest and Malnutrition_Latest > Malnutrition_Earliest order by Obesity_Latest - Obesity_Earliest desc;",
            "5. Age-wise trend analysis " : "select A.age_group as 'Age_Group', A.Region as 'Region', A.Gender as 'Gender',  A.Obesity_level as 'Obesity_Level', B.Malnutrition_Level as 'Malnutrition_Level', avg(A.Mean_Estimate) as 'Obesity_Mean_Estimate', avg(B.Mean_Estimate) as 'Malnutrition_Mean_Estimate' from obesity A join malnutrition B On A.Country = B.Country and A.Region = B.Region and A.age_group = B.age_group and A.Gender = B.Gender group by A.Region, A.Gender, A.age_group, A.Obesity_level, B.Malnutrition_Level order by A.age_group, A.Region Asc;" 
        }
         
    selected_box = st.selectbox("Choose a Query Options", ["Obesity", "Malnutrition", "Combined"])
    if selected_box == "Obesity":
        st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\ij.jpeg', width=150)
        selected_query = st.selectbox("Choose a Query", list(obesity_queries.keys()))
        query_result = get_data(obesity_queries[selected_query])
    elif selected_box == "Malnutrition":
        st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\uhk.jpeg', width=230)
        selected_query = st.selectbox("Choose a Query", list(malnutrition_queries.keys()))
        query_result = get_data(malnutrition_queries[selected_query])
    elif selected_box == "Combined":
        st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\images (4).jpeg', width=230)
        selected_query = st.selectbox("Choose a Query", list(combined_queries.keys()))
        query_result = get_data(combined_queries[selected_query])

    st.write("### Query Result:")
    st.dataframe(query_result)

# -------------------------------- PAGE 4: Creator Info --------------------------------
elif page == "Suggestions" :
    
    st.markdown("""
    # Which regions require urgent intervention?
    ## Africa and South-East-Asia Region show critical sign in both malnutrition and rising obisity trends. these regions may benefit most from immediate public health intervensions and targeted nutrition policies.
        """)
    
 
    st.markdown("""
    # Are there noticeable trends in obesity or malnutrition over time?
    ##  Obesity is steadily increasing globally, highlighting a growing public health concern. While malnutrition has declined in some regions, persistent or rising trends in others indicate the need for targeted interventions. 
        """)

    st.markdown("""
    # Which demographic groups are most vulnerable?
    ##  Females and populations in low-income regions are among the most vulnerable to both obesity and malnutrition. Tailored health policies are essential to address these overlapping risks.
    """)
    st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\images (9).jpeg', width=250)
   
    st.markdown("""
    # How reliable is the data across regions (based on CI_Width)?
    ## Regions like Africa and South-East Asia exhibit wider confidence intervals in obesity and malnutrition data, indicating less reliable estimates. In contrast, Europe and the Americas show narrower intervals, reflecting more consistent and dependable data.
    """)
    
    st.markdown("""
    # What health strategies could be informed by these findings?
    ## To effectively address the intertwined issues of obesity and malnutrition, a multifaceted approach is essential. This includes implementing double-duty actions, enhancing nutrition education, addressing socioeconomic and environmental determinants, leveraging technology, and strengthening data systems. Tailoring these strategies to specific regional and demographic contexts will maximize their impact.
    """)

    
    

# -------------------------------- PAGE 5: Creator Info --------------------------------
elif page == "Creator Info":
    st.title("👩‍💻 Creator of this Project")
    st.write("""
#    **Developed by:** Sudharsan M S
#    **Skills:** Python, MySQL, Streamlit
    """)
    st.image(r'C:\Users\91968\OneDrive\Desktop\Pthon DS GuVi\Project\Project2\cacx.png', width=150)
