from rich import print
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_generator import DataGenerator
from data_storage import DataStorage
from visualizer import Visualizer

def main():
    print("[bold green]🚀 Data Generation & Visualization Project[/bold green]")
    
    # Initialize components
    generator = DataGenerator()
    storage = DataStorage()
    visualizer = Visualizer()
    
    # Generate sample datasets
    print("\n[yellow]📊 Generating sample data...[/yellow]")
    
    # Generate different types of datasets
    sales_data = generator.generate_sales_data(1000)
    weather_data = generator.generate_weather_data(365)
    stock_data = generator.generate_stock_data(252)  # Trading days in a year
    customer_data = generator.generate_customer_data(500)
    
    # Store data in different formats
    print("\n[yellow]💾 Storing data in Data folder...[/yellow]")
    storage.save_to_csv(sales_data, "sales_data.csv")
    storage.save_to_json(weather_data, "weather_data.json")
    storage.save_to_csv(stock_data, "stock_data.csv")
    storage.save_to_json(customer_data, "customer_data.json")
    
    # Create visualizations
    print("\n[yellow]📈 Creating visualizations...[/yellow]")
    
    # Static plots with matplotlib
    visualizer.create_sales_analysis(sales_data)
    visualizer.create_weather_plots(weather_data)
    visualizer.create_stock_analysis(stock_data)
    
    # Interactive plots with plotly
    visualizer.create_interactive_dashboard(sales_data, weather_data, stock_data)
    
    print("\n[bold green]✅ Project completed successfully![/bold green]")
    print("\n[cyan]Generated files:[/cyan]")
    print("• Data/sales_data.csv")
    print("• Data/weather_data.json")
    print("• Data/stock_data.csv")
    print("• Data/customer_data.json")
    print("• Various plot images in the project directory")
    print("• Interactive dashboard HTML file")

if __name__ == "__main__":
    main()
