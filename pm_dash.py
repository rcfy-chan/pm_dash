import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(layout="wide")

# Load data
df = pd.read_csv('PM_Data.csv', nrows=200)

# Convert 'Start' and 'End' to datetime
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
today = pd.to_datetime(datetime.today())

total_projects = df['ProjectTitle'].nunique()                                   
average_duration = df['Duration'].mean()
median_duration = df['Duration'].median()
delayed_projects_count = df[df['Status'] == 'Delayed'].shape[0]

years = pd.to_datetime(df[['Start', 'End']].stack()).dt.year.unique()
start_year1, end_year1 = min(years), max(years)

# Preprocess data
agg_df = df.groupby('ProjectTitle').agg({
    'Start': 'first',
    'End': 'first',
    'Status': 'first',
    'Priority': 'first' 
}).reset_index()
# Create donut chart
priority_counts = agg_df['Priority'].value_counts().reset_index()
priority_counts.columns = ['Priority', 'Count']
donut_chart = alt.Chart(priority_counts).mark_arc(
    innerRadius=30, outerRadius=85, opacity=0.7
).encode(
    theta=alt.Theta("Count:Q").stack(True),
    color=alt.Color(field="Priority", legend=None),
    tooltip=['Priority', 'Count']
).properties(
    title=f'Projects Distribution by Priority ({start_year1}-{end_year1})'
)
text = donut_chart.mark_text(radius=60, align='center', fontSize=12, fontWeight='bold').encode(text='Count')
text1 = donut_chart.mark_text(radius=120, align='center', fontSize=12, fontWeight='bold').encode(text='Priority')
donut = donut_chart + text + text1

# Create donut chart
status_counts = agg_df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']
status_chart = alt.Chart(status_counts).mark_arc(
    innerRadius=30, outerRadius=85, opacity=0.7
).encode(
    theta=alt.Theta("Count:Q").stack(True),
    color=alt.Color(field="Status", legend=None),
    tooltip=['Status', 'Count']
).properties(
    title=f'Projects Distribution by Status ({start_year1}-{end_year1})'
)
text_status = status_chart.mark_text(radius=60, align='center', fontSize=12, fontWeight='bold').encode(text='Count')
text_status1 = status_chart.mark_text(radius=120, align='center', fontSize=12, fontWeight='bold').encode(text='Status')
status_donut = status_chart + text_status + text_status1

# Create scatter plot
assigned_to_project_counts = df.groupby(['AssignedTo', 'ProjectComponents'])['ProjectTitle'].nunique().reset_index()
assigned_to_project_counts.columns = ['AssignedTo', 'ProjectComponents', 'Count']
assigned_counts = df.groupby(['AssignedTo'])['ProjectTitle'].nunique().reset_index()
assigned_counts.columns = ['AssignedTo', 'Count']

projcomp_counts = df.groupby(['ProjectComponents'])['ProjectTitle'].nunique().reset_index()
projcomp_counts.columns = ['ProjectComponents', 'Count']

sorted_assigned_to = assigned_counts.sort_values('Count', ascending=False)['AssignedTo'].tolist()
sorted_project_component = projcomp_counts.sort_values('Count', ascending=False)['ProjectComponents'].tolist()

project_scatter_plot = alt.Chart(assigned_to_project_counts).mark_circle(size=100).encode(
    x=alt.X('AssignedTo:N', title='Responsible', sort=sorted_assigned_to, axis=None),
    y=alt.Y('ProjectComponents:N', title='Project Components', sort=sorted_project_component),
    size='Count:Q',
    tooltip=['AssignedTo', 'Count', 'ProjectComponents']
).properties(
    width=600,
    height=400,
    title=f'Distribution of Projects by Responsible Individuals and Project Components ({start_year1}-{end_year1})'
)
# Create bar chart
bar = alt.Chart(assigned_counts).mark_bar().encode(
    x=alt.X('AssignedTo:N', title='Responsible', sort=sorted_assigned_to),
    y='Count:Q',
    tooltip=['AssignedTo', 'Count']
).properties(
    width=600,
    height=200
)

# Sidebar chart for project components
project_component_bar = alt.Chart(projcomp_counts).mark_bar().encode(
    y=alt.Y('ProjectComponents:N', title='Project Components', sort=sorted_project_component, axis=None),
    x=alt.X('sum(Count):Q', title='Count'),
    tooltip=['ProjectComponents', 'sum(Count)']
).properties(
    width=200,
    height=400
)

# Combine scatter plot and bar chart
combined_chart = alt.hconcat(alt.vconcat(project_scatter_plot, bar), project_component_bar).resolve_legend(
    color="independent"
)

# Streamlit app layout
st.title('Project Management Dashboard')

head_col1, head_col2, head_col3, head_col4 = st.columns(4)
with head_col1:
    st.metric(label='Total Projects', value=total_projects)

with head_col2:  
    st.metric(label='Delayed Projects', value=delayed_projects_count)
    
with head_col3:    
    st.metric(label='Average Duration', value=f"{int(average_duration)} days")

with head_col4:        
    st.metric(label='Median Duration', value=f"{int(median_duration)} days")

tab1, tab2 = st.tabs(["Overview", "Timeline"])

with tab1:
    tab1_col1, tab1_col2 = st.columns([1.5,5])
    with tab1_col1:
        st.altair_chart(donut, use_container_width=True)
        st.altair_chart(status_donut, use_container_width=True)
    with tab1_col2:
        st.altair_chart(combined_chart, use_container_width=True)

with tab2:

    # Organize widgets into three columns
    col1, col2, col3 = st.columns([1,7,2.5])
    
    # Radio buttons for project status
    with col1:
        project_status = st.radio("Project Status", options=['All','Ongoing', 'Completed'], index=0, format_func=lambda x: x)

    if project_status == 'All':

        #Filter  
        df_filtered = df.copy()
        
        # Get unique years from the 'Start' and 'End' dates
        years = pd.to_datetime(df_filtered[['Start', 'End']].stack()).dt.year.unique()
        years = sorted(years)

        with col2: 
            year_range = st.slider('Select Year Range', min_value=min(years), max_value=max(years), value=(min(years), max(years)))
            start_year, end_year = year_range
            df_filtered = df_filtered[(df_filtered['End'].dt.year <= end_year) & (df_filtered['Start'].dt.year >= start_year)]


    # Filter data based on selected project status
    elif project_status == 'Ongoing':

        #Filter  
        df_filtered = df[df['Status'].isin(['Ongoing', 'Delayed'])]

        # Get unique years from the 'Start' and 'End' dates
        years = pd.to_datetime(df_filtered[['Start', 'End']].stack()).dt.year.unique()
        years = sorted(years)

        with col2: 
            year_range = st.slider('Select Year Range', min_value=min(years), max_value=max(years), value=(min(years), max(years)))
            start_year, end_year = year_range
            df_filtered = df_filtered[(df_filtered['End'].dt.year <= end_year) & (df_filtered['Start'].dt.year >= start_year)]

    elif project_status == 'Completed':
        #Filter  
        df_filtered = df[df['Status'].isin(['Completed'])]

        # Get unique years from the 'Start' and 'End' dates
        years = pd.to_datetime(df_filtered[['Start', 'End']].stack()).dt.year.unique()
        years = sorted(years)

        with col2: 
            year_range = st.slider('Select Year Range', min_value=min(years), max_value=max(years), value=(min(years), max(years)))
            start_year, end_year = year_range
            df_filtered = df_filtered[(df_filtered['End'].dt.year <= end_year) & (df_filtered['Start'].dt.year >= start_year)]


    # Multiselect box for priority
    with col3:
        priority_order = ['High', 'Medium', 'Low']
        selected_priorities = st.multiselect("Select Priority", options=priority_order, default=priority_order)

    # Filter data based on selected priorities
    df_filtered = df_filtered[df_filtered['Priority'].isin(selected_priorities)]

    unique_statuses = df['Status'].unique().tolist()

    gantt_chart = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X('Start:T', title='Time'),
        x2='End:T',
        y=alt.Y('ProjectTitle:N', sort=alt.SortField(field='Start', order='ascending')),
        color=alt.Color('Status:N', scale=alt.Scale(domain=['Delayed', 'Ongoing', 'Completed'], range=['red', 'orange', 'green'])),
        ).properties(
        width=600,
        height=1000,
        title=f'Gantt Chart of {project_status} Projects ({start_year}-{end_year})'
        )

    # Display charts
    st.header(' ')
    st.altair_chart(gantt_chart, use_container_width=True)

