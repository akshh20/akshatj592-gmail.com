import pandas as pd
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='data_ingestion.log', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Task 1: Data Ingestion and Validation
def ingest_data(data_directory):
    df_combined = pd.DataFrame()
    for csv_file in Path(data_directory).glob('*.csv'):
        try:
            df = pd.read_csv(csv_file, error_bad_lines=False)
            # Add metadata if not present
            building_name = csv_file.stem
            df['building_name'] = building_name
            df_combined = df_combined.append(df, ignore_index=True)
        except FileNotFoundError:
            logging.error(f"File not found: {csv_file}")
        except Exception as e:
            logging.error(f"Error reading {csv_file}: {e}")
    return df_combined

# Task 2: Core Aggregation Logic
def calculate_daily_totals(df):
    return df.resample('D').sum()

def calculate_weekly_aggregates(df):
    return df.resample('W').sum()

def building_wise_summary(df):
    return df.groupby('building_name').agg(['mean', 'min', 'max', 'sum'])

# Task 3: Object-Oriented Modeling
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(reading.kwh for reading in self.meter_readings)

    def generate_report(self):
        total_consumption = self.calculate_total_consumption()
        return f"Building: {self.name}, Total Consumption: {total_consumption} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_building(self, building):
        self.buildings[building.name] = building

# Task 4: Visual Output with Matplotlib
import matplotlib.pyplot as plt

def create_dashboard(df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Trend Line
    df.resample('D').sum()['kwh'].plot(ax=axs[0])
    axs[0].set_title('Daily Consumption Over Time')
    axs[0].set_ylabel('kWh')

    # Bar Chart
    df.groupby('building_name').resample('W').sum()['kwh'].mean().unstack().plot(kind='bar', ax=axs[1])
    axs[1].set_title('Average Weekly Usage Across Buildings')
    axs[1].set_ylabel('Average kWh')

    # Scatter Plot
    axs[2].scatter(df['timestamp'], df['kwh'])
    axs[2].set_title('Peak-Hour Consumption vs Time')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('kWh')

    plt.tight_layout()
    plt.savefig('dashboard.png')

# Task 5: Persistence and Executive Summary
def export_data(df_combined, summary_df):
    df_combined.to_csv('cleaned_energy_data.csv', index=False)
    summary_df.to_csv('building_summary.csv', index=True)

    with open('summary.txt', 'w') as f:
        f.write("Total campus consumption: {}\n".format(df_combined['kwh'].sum()))
        f.write("Highest-consuming building: {}\n".format(summary_df['sum'].idxmax()))
        f.write("Peak load time: {}\n".format(df_combined.loc[df_combined['kwh'].idxmax()]['timestamp']))
        f.write("Weekly/Daily trends: See the attached CSV files.\n")

# Example usage
if __name__ == "__main__":
    data_directory = '/data/'
    df_combined = ingest_data(data_directory)
    daily_totals = calculate_daily_totals(df_combined)
    weekly_aggregates = calculate_weekly_aggregates(df_combined)
    summary_df = building_wise_summary(df_combined)
    create_dashboard(df_combined)
    export_data(df_combined, summary_df)