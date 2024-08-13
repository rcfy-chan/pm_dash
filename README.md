Project Management Dashboard
This repository contains a Streamlit application for visualizing and managing project data. The dashboard provides various charts and metrics to help track project status, duration, priority, and more.

Overview
The Project Management Dashboard offers the following features:

Total number of projects, average duration, median duration, and delayed projects count.
Donut charts displaying the distribution of projects by priority and status.
Scatter plot and bar charts showing the number of projects assigned to individuals and project components.
Gantt chart to visualize the timeline of projects based on their status and priority.
Additionally, a Power BI dashboard is included to complement the Streamlit application, offering further analysis and visualization of project data. The Power BI dashboard can be accessed through the provided link or embedded within your reports.

Features
Metrics: Display key project metrics such as total projects, delayed projects, average duration, and median duration.
Donut Charts: Visual representation of project distribution by priority and status.
Scatter Plot and Bar Charts: Analysis of projects by responsible individuals and project components.
Gantt Chart: Visual timeline of projects filtered by status, year range, and priority.
Power BI Dashboard: A supplementary dashboard created in Power BI to provide additional insights and visualizations of project data.
Setup
Prerequisites
Ensure you have the following installed:

Python 3.7+
Streamlit
Pandas
Altair
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/project-management-dashboard.git
cd project-management-dashboard
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Place your PM_Data.csv file in the root directory of the project.

Running the Application
To run the Streamlit application, use the following command:

bash
Copy code
streamlit run app.py
Accessing the Power BI Dashboard
You can access the Power BI dashboard by following the link provided in the repository or by embedding it into your reports. This dashboard offers additional analysis and visualizations to support your project management efforts.
