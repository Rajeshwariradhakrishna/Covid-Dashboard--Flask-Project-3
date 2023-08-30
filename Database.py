
#Import the dependencies
from sqlalchemy import create_engine, text, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import date
from pathlib import Path
import json

import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def LoadData():
    #Load your PostGres database
    userName = "postgres"
    password = "postgres" #use your postgres password if you changed it
    database = "COVID-19 Data" #you can use any db you want, I just happened to use this one
    engine = create_engine(f"postgresql+psycopg2://{userName}:{password}@localhost:5432/{database}")
    conn = engine.connect()

    #Pull the data into pandas. We are filtering by the period    
    try:
        # Query All Records in the the Database
        query = text("SELECT * FROM Countries")
        countries_df = pd.read_sql(query, conn)
        
    except:
        print("No data Available")
        
    return countries_df
    
def LoadCountryData():
    #Load your PostGres database
    userName = "postgres"
    password = "postgres"
    database = "COVID-19 Data"
    engine = create_engine(f"postgresql+psycopg2://{userName}:{password}@localhost:5432/{database}")
    conn = engine.connect()

    #Pull the data into pandas. We are filtering by the period    
    try:
        # Query Records for Countries in the the Database
        query_country = text("SELECT * FROM Countries")
        countries_df = pd.read_sql(query_country, conn)

    except:
        print("No data Available")
        
    return countries_df

def LoadCaseData():
    #Load your PostGres database
    userName = "postgres"
    password = "postgres"
    database = "COVID-19 Data"
    engine = create_engine(f"postgresql+psycopg2://{userName}:{password}@localhost:5432/{database}")
    conn = engine.connect()

    #Pull the data into pandas. We are filtering by the period    
    try:
        # Query Records for Cases in the Database
        query_cases = text("SELECT * FROM Cases")
        cases_df = pd.read_sql(query_cases, conn)

    except:
        print("No data Available")
        
    return cases_df

def LoadVaxData():
    #Load your PostGres database
    userName = "postgres"
    password = "postgres"
    database = "COVID-19 Data"
    engine = create_engine(f"postgresql+psycopg2://{userName}:{password}@localhost:5432/{database}")
    conn = engine.connect()

    #Pull the data into pandas. We are filtering by the period    
    try:
        # Query Records for Cases in the Database
        query_vax = text("SELECT * FROM Vaccinations")
        vaccination_df = pd.read_sql(query_vax, conn)

    except:
        print("No data Available")
        
    return vaccination_df

# Create a base class for declarating class definitions to produce Table objects
Base = declarative_base()

class Countries(Base): 
    __tablename__ = "Countries"

    Country = Column(String, primary_key=True)
    WHO_Region = Column(String)

class Cases(Base): 
    __tablename__ = "Cases"

    Country = Column(String)
    WHO_Region = Column(String)
    Cases_Cumulative_Total = Column(Integer)
    New_Cases_Last_7_Days = Column(Integer)
    Deaths_Cumulative_Total = Column(Integer)
    New_Deaths_Last_7_Days = Column(Integer)
    Latitude = Column(Integer)
    Longitude = Column(Integer)
    Case_ID = Column(Integer, primary_key=True)

class Vaccination(Base): 
    __tablename__ = "Vaccinations"

    Country = Column(String)
    WHO_Region = Column(String)
    Date_Updated = Column(Date)
    Total_Vaccinations = Column(Integer)
    Persons_Vaccinated_Plus1_Dose = Column(Integer)
    First_Vaccine_Date = Column(Date)
    Persons__Booster_Add_Dose = Column(Integer)
    Vax_ID = Column(Integer, primary_key=True)

def deaths_vs_vaccination():
    countries_df = LoadCountryData()
    countries_df.head()

    # Create dataframe for Cases 
    cases_df = LoadCaseData()
    cases_df = cases_df.drop(cases_df.index[0])
    cases_df.head().to_dict("records")

    vaccination_df = LoadVaxData()
    vaccination_df.head()

    #Groupby to find total vaccinations and total deaths
    total_vaccination = vaccination_df.groupby("country")["total_vaccinations"].sum()
    total_deaths = cases_df.groupby("country")["deaths_cumulative_total"].sum()

    total_death_in_countries = cases_df.groupby("country")["deaths_cumulative_total"].sum()
    top_20_highest_death_countries = total_death_in_countries.nlargest(20)

    # Identifying the countries that are present in the both top_20_highest_death_countries and total_vaccination
    common_countries = top_20_highest_death_countries.index.intersection(total_vaccination.index)
    total_vaccination = total_vaccination[common_countries]
    total_deaths = total_deaths[common_countries]

    # Create a DataFrame for the data
    data = {
        "Country": common_countries,
        "Total Deaths": total_deaths,
        "Total Vaccinations": total_vaccination
    }
    df = pd.DataFrame(data)
    return df


def new_cases_last_7_days():
    countries_df = LoadCountryData()
    countries_df.head()

    # Create dataframe for Cases 
    cases_df = LoadCaseData()
    cases_df = cases_df.drop(cases_df.index[0])
    cases_df.head().to_dict("records")

    vaccination_df = LoadVaxData()
    vaccination_df.head()
    
    #Groupby to find the new Covid cases in last 7 days and sorting
    new_cases_last_7_days = cases_df.groupby("country")["new_cases_last_7_days"].sum()
    sorting_new_cases = cases_df.sort_values(by='new_cases_last_7_days', ascending=False)
    top_10_values_new_cases_last_7_days = sorting_new_cases.head(10)
    top_10_values_new_cases_last_7_days

    # Create a DataFrame for the data
    data = {
    "Country" : top_10_values_new_cases_last_7_days["country"],
    "New Covid Cases in Last 7 days" : top_10_values_new_cases_last_7_days["new_cases_last_7_days"]
    }
    new_cases_last_7_days_df = pd.DataFrame(data)
    return new_cases_last_7_days_df

def country_info():
    world_file = open('data/WHO-Data.json', 'r') 
    return world_file.read()
