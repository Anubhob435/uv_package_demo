"""
Visualization Module

This module provides functionality to create various types of plots and visualizations
using matplotlib for static plots and plotly for interactive visualizations.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from rich import print

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class Visualizer:
    """Creates various types of static and interactive visualizations."""
    
    def __init__(self, output_dir: str = "plots"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save plot images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def create_sales_analysis(self, sales_data: pd.DataFrame) -> None:
        """
        Create comprehensive sales analysis plots.
        
        Args:
            sales_data: DataFrame with sales data
        """
        print("[yellow]📊 Creating sales analysis plots...[/yellow]")
        
        # Convert date column to datetime
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        
        # Create a figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Sales Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Sales trend over time
        monthly_sales = sales_data.groupby(sales_data['date'].dt.to_period('M'))['total_amount'].sum()
        axes[0, 0].plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', linewidth=2)
        axes[0, 0].set_title('Monthly Sales Trend')
        axes[0, 0].set_xlabel('Month')
        axes[0, 0].set_ylabel('Total Sales ($)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Sales by product
        product_sales = sales_data.groupby('product')['total_amount'].sum().sort_values(ascending=True)
        axes[0, 1].barh(product_sales.index, product_sales.values)
        axes[0, 1].set_title('Sales by Product')
        axes[0, 1].set_xlabel('Total Sales ($)')
        
        # 3. Sales by region
        region_sales = sales_data.groupby('region')['total_amount'].sum()
        colors = plt.cm.Set3(np.linspace(0, 1, len(region_sales)))
        wedges, texts, autotexts = axes[1, 0].pie(region_sales.values, labels=region_sales.index, 
                                                  autopct='%1.1f%%', colors=colors)
        axes[1, 0].set_title('Sales Distribution by Region')
        
        # 4. Salesperson performance
        salesperson_sales = sales_data.groupby('salesperson')['total_amount'].sum().sort_values(ascending=False)
        axes[1, 1].bar(range(len(salesperson_sales)), salesperson_sales.values)
        axes[1, 1].set_title('Salesperson Performance')
        axes[1, 1].set_xlabel('Salesperson')
        axes[1, 1].set_ylabel('Total Sales ($)')
        axes[1, 1].set_xticks(range(len(salesperson_sales)))
        axes[1, 1].set_xticklabels(salesperson_sales.index, rotation=45, ha='right')
        
        plt.tight_layout()
        filepath = self.output_dir / 'sales_analysis.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"[green]✓[/green] Saved sales analysis: {filepath}")
        
        # Additional detailed plot: Sales heatmap by day of week and hour
        self._create_sales_heatmap(sales_data)
    
    def create_weather_plots(self, weather_data: pd.DataFrame) -> None:
        """
        Create weather analysis plots.
        
        Args:
            weather_data: DataFrame with weather data
        """
        print("[yellow]🌤️ Creating weather analysis plots...[/yellow]")
        
        # Convert date column to datetime
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Weather Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Temperature trend
        axes[0, 0].plot(weather_data['date'], weather_data['temperature_celsius'], 
                       color='red', alpha=0.7, linewidth=1)
        axes[0, 0].set_title('Temperature Trend Over Time')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Temperature (°C)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Format x-axis dates
        axes[0, 0].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45)
        
        # 2. Temperature distribution by season
        sns.boxplot(data=weather_data, x='season', y='temperature_celsius', ax=axes[0, 1])
        axes[0, 1].set_title('Temperature Distribution by Season')
        axes[0, 1].set_ylabel('Temperature (°C)')
        
        # 3. Humidity vs Temperature scatter
        scatter = axes[1, 0].scatter(weather_data['temperature_celsius'], 
                                   weather_data['humidity_percent'],
                                   c=weather_data['day_of_year'], 
                                   cmap='viridis', alpha=0.6)
        axes[1, 0].set_title('Humidity vs Temperature')
        axes[1, 0].set_xlabel('Temperature (°C)')
        axes[1, 0].set_ylabel('Humidity (%)')
        plt.colorbar(scatter, ax=axes[1, 0], label='Day of Year')
        
        # 4. Monthly precipitation
        monthly_precip = weather_data.groupby('month')['precipitation_mm'].sum()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        axes[1, 1].bar(monthly_precip.index, monthly_precip.values, 
                      color='skyblue', alpha=0.8)
        axes[1, 1].set_title('Monthly Precipitation')
        axes[1, 1].set_xlabel('Month')
        axes[1, 1].set_ylabel('Precipitation (mm)')
        axes[1, 1].set_xticks(range(1, 13))
        axes[1, 1].set_xticklabels(month_names)
        
        plt.tight_layout()
        filepath = self.output_dir / 'weather_analysis.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"[green]✓[/green] Saved weather analysis: {filepath}")
    
    def create_stock_analysis(self, stock_data: pd.DataFrame) -> None:
        """
        Create stock market analysis plots.
        
        Args:
            stock_data: DataFrame with stock data
        """
        print("[yellow]📈 Creating stock analysis plots...[/yellow]")
        
        # Convert date column to datetime
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        
        # Get unique symbols
        symbols = stock_data['symbol'].unique()
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Stock Market Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Stock price trends
        for symbol in symbols:
            symbol_data = stock_data[stock_data['symbol'] == symbol]
            axes[0, 0].plot(symbol_data['date'], symbol_data['close'], 
                          label=symbol, linewidth=2)
        
        axes[0, 0].set_title('Stock Price Trends')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Closing Price ($)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Daily returns distribution
        axes[0, 1].hist(stock_data['daily_return'], bins=50, alpha=0.7, 
                       color='steelblue', edgecolor='black')
        axes[0, 1].set_title('Daily Returns Distribution')
        axes[0, 1].set_xlabel('Daily Return (%)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].axvline(stock_data['daily_return'].mean(), color='red', 
                          linestyle='--', label=f"Mean: {stock_data['daily_return'].mean():.3f}%")
        axes[0, 1].legend()
        
        # 3. Volume by symbol
        volume_by_symbol = stock_data.groupby('symbol')['volume'].mean()
        axes[1, 0].bar(volume_by_symbol.index, volume_by_symbol.values, 
                      color='orange', alpha=0.8)
        axes[1, 0].set_title('Average Trading Volume by Symbol')
        axes[1, 0].set_xlabel('Symbol')
        axes[1, 0].set_ylabel('Average Volume')
        
        # 4. Volatility analysis (rolling standard deviation of returns)
        for symbol in symbols[:3]:  # Show top 3 for clarity
            symbol_data = stock_data[stock_data['symbol'] == symbol].sort_values('date')
            rolling_vol = symbol_data['daily_return'].rolling(window=20).std()
            axes[1, 1].plot(symbol_data['date'], rolling_vol, label=f"{symbol} (20-day)")
        
        axes[1, 1].set_title('Rolling Volatility (20-day)')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Volatility (%)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        filepath = self.output_dir / 'stock_analysis.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"[green]✓[/green] Saved stock analysis: {filepath}")
    
    def create_interactive_dashboard(self, sales_data: pd.DataFrame, 
                                   weather_data: pd.DataFrame, 
                                   stock_data: pd.DataFrame) -> None:
        """
        Create an interactive dashboard using Plotly.
        
        Args:
            sales_data: DataFrame with sales data
            weather_data: DataFrame with weather data
            stock_data: DataFrame with stock data
        """
        print("[yellow]🚀 Creating interactive dashboard...[/yellow]")
        
        # Convert date columns
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        stock_data['date'] = pd.to_datetime(stock_data['date'])
          # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=['Sales Trend', 'Product Performance', 
                          'Temperature & Humidity', 'Stock Prices',
                          'Regional Sales Distribution', 'Trading Volume'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": True}, {"secondary_y": False}],
                   [{"type": "domain"}, {"secondary_y": False}]],
            vertical_spacing=0.08
        )
        
        # 1. Sales trend
        monthly_sales = sales_data.groupby(sales_data['date'].dt.to_period('M'))['total_amount'].sum()
        fig.add_trace(
            go.Scatter(x=monthly_sales.index.astype(str), y=monthly_sales.values,
                      mode='lines+markers', name='Monthly Sales',
                      line=dict(color='blue', width=3)),
            row=1, col=1
        )
        
        # 2. Product performance
        product_sales = sales_data.groupby('product')['total_amount'].sum().sort_values(ascending=False)
        fig.add_trace(
            go.Bar(x=product_sales.index, y=product_sales.values,
                  name='Product Sales', marker_color='lightblue'),
            row=1, col=2
        )
        
        # 3. Temperature and humidity
        fig.add_trace(
            go.Scatter(x=weather_data['date'], y=weather_data['temperature_celsius'],
                      mode='lines', name='Temperature', line=dict(color='red')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=weather_data['date'], y=weather_data['humidity_percent'],
                      mode='lines', name='Humidity', line=dict(color='blue'),
                      yaxis='y2'),
            row=2, col=1, secondary_y=True
        )
        
        # 4. Stock prices
        for symbol in stock_data['symbol'].unique():
            symbol_data = stock_data[stock_data['symbol'] == symbol]
            fig.add_trace(
                go.Scatter(x=symbol_data['date'], y=symbol_data['close'],
                          mode='lines', name=f'{symbol} Close'),
                row=2, col=2
            )
        
        # 5. Regional sales distribution
        region_sales = sales_data.groupby('region')['total_amount'].sum()
        fig.add_trace(
            go.Pie(labels=region_sales.index, values=region_sales.values,
                  name='Regional Sales'),
            row=3, col=1
        )
        
        # 6. Trading volume
        volume_by_date = stock_data.groupby('date')['volume'].sum()
        fig.add_trace(
            go.Bar(x=volume_by_date.index, y=volume_by_date.values,
                  name='Daily Volume', marker_color='orange'),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive Data Analysis Dashboard",
            title_x=0.5,
            title_font_size=20,
            height=1200,
            showlegend=True
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Month", row=1, col=1)
        fig.update_yaxes(title_text="Sales ($)", row=1, col=1)
        
        fig.update_xaxes(title_text="Product", row=1, col=2)
        fig.update_yaxes(title_text="Total Sales ($)", row=1, col=2)
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Temperature (°C)", row=2, col=1)
        fig.update_yaxes(title_text="Humidity (%)", secondary_y=True, row=2, col=1)
        
        fig.update_xaxes(title_text="Date", row=2, col=2)
        fig.update_yaxes(title_text="Stock Price ($)", row=2, col=2)
        
        fig.update_xaxes(title_text="Date", row=3, col=2)
        fig.update_yaxes(title_text="Volume", row=3, col=2)
        
        # Save and show
        filepath = self.output_dir / 'interactive_dashboard.html'
        fig.write_html(filepath)
        fig.show()
        print(f"[green]✓[/green] Saved interactive dashboard: {filepath}")
    
    def _create_sales_heatmap(self, sales_data: pd.DataFrame) -> None:
        """Create a sales heatmap by day of week and month."""
        # Add day of week and month columns
        sales_data['day_of_week'] = sales_data['date'].dt.day_name()
        sales_data['month'] = sales_data['date'].dt.month_name()
        
        # Create pivot table for heatmap
        heatmap_data = sales_data.groupby(['month', 'day_of_week'])['total_amount'].sum().unstack()
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data[day_order]
        
        # Create heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Total Sales ($)'})
        plt.title('Sales Heatmap by Month and Day of Week', fontsize=14, fontweight='bold')
        plt.xlabel('Day of Week')
        plt.ylabel('Month')
        plt.tight_layout()
        
        filepath = self.output_dir / 'sales_heatmap.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"[green]✓[/green] Saved sales heatmap: {filepath}")
