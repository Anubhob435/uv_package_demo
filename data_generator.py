"""
Data Generator Module

This module provides functionality to generate various types of sample data
for demonstration purposes including sales, weather, stock, and customer data.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

class DataGenerator:
    """Generates various types of sample datasets for analysis and visualization."""
    
    def __init__(self, seed: int = 42):
        """Initialize the data generator with a random seed for reproducibility."""
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_sales_data(self, num_records: int = 1000) -> pd.DataFrame:
        """
        Generate synthetic sales data.
        
        Args:
            num_records: Number of sales records to generate
            
        Returns:
            DataFrame with sales data including date, product, sales amount, etc.
        """
        products = [
            'Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor', 
            'Keyboard', 'Mouse', 'Speaker', 'Webcam', 'Charger'
        ]
        
        regions = ['North', 'South', 'East', 'West', 'Central']
        salespersons = [
            'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince',
            'Eva Martinez', 'Frank Wilson', 'Grace Lee', 'Henry Davis'
        ]
        
        # Generate date range for the last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        data = []
        for _ in range(num_records):
            # Random date within the year
            random_days = random.randint(0, 365)
            sale_date = start_date + timedelta(days=random_days)
            
            product = random.choice(products)
            
            # Price based on product type with some variation
            base_prices = {
                'Laptop': 800, 'Smartphone': 600, 'Tablet': 400, 'Monitor': 300,
                'Headphones': 150, 'Keyboard': 80, 'Mouse': 50, 'Speaker': 120,
                'Webcam': 90, 'Charger': 30
            }
            
            base_price = base_prices[product]
            # Add variation (±20%)
            price = base_price * (0.8 + 0.4 * random.random())
            
            # Quantity (most sales are 1-3 items)
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
            
            total_amount = price * quantity
            
            # Add seasonal trends for certain products
            month = sale_date.month
            if product in ['Laptop', 'Tablet'] and month in [11, 12, 1]:  # Holiday season
                total_amount *= 1.2
            elif product in ['Smartphone'] and month in [9, 10]:  # New release season
                total_amount *= 1.15
            
            data.append({
                'date': sale_date.strftime('%Y-%m-%d'),
                'product': product,
                'quantity': quantity,
                'unit_price': round(price, 2),
                'total_amount': round(total_amount, 2),
                'region': random.choice(regions),
                'salesperson': random.choice(salespersons),
                'customer_id': f"CUST{random.randint(1000, 9999)}"
            })
        
        return pd.DataFrame(data)
    
    def generate_weather_data(self, num_days: int = 365) -> pd.DataFrame:
        """
        Generate synthetic weather data.
        
        Args:
            num_days: Number of days of weather data to generate
            
        Returns:
            DataFrame with weather data including temperature, humidity, pressure, etc.
        """
        start_date = datetime.now() - timedelta(days=num_days)
        
        data = []
        for i in range(num_days):
            current_date = start_date + timedelta(days=i)
            
            # Seasonal temperature variation
            day_of_year = current_date.timetuple().tm_yday
            seasonal_temp = 20 + 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
            
            # Add daily variation and noise
            temp = seasonal_temp + 5 * np.sin(2 * np.pi * i / 7) + np.random.normal(0, 3)
            
            # Humidity (higher in summer, correlated with temperature)
            humidity = 60 + 20 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + np.random.normal(0, 10)
            humidity = max(20, min(100, humidity))  # Clamp between 20-100%
            
            # Atmospheric pressure
            pressure = 1013 + np.random.normal(0, 15)
            
            # Wind speed (higher in winter)
            wind_speed = 10 + 5 * np.sin(2 * np.pi * (day_of_year - 260) / 365) + np.random.exponential(3)
            
            # Precipitation (random, but more likely in certain seasons)
            precipitation_prob = 0.1 + 0.1 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
            precipitation = np.random.exponential(5) if random.random() < precipitation_prob else 0
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'temperature_celsius': round(temp, 1),
                'humidity_percent': round(humidity, 1),
                'pressure_hpa': round(pressure, 1),
                'wind_speed_kmh': round(wind_speed, 1),
                'precipitation_mm': round(precipitation, 1),
                'day_of_year': day_of_year,
                'month': current_date.month,
                'season': self._get_season(current_date.month)
            })
        
        return pd.DataFrame(data)
    
    def generate_stock_data(self, num_days: int = 252) -> pd.DataFrame:
        """
        Generate synthetic stock market data.
        
        Args:
            num_days: Number of trading days to generate
            
        Returns:
            DataFrame with stock data including OHLCV data
        """
        companies = [
            {'symbol': 'TECH', 'name': 'TechCorp Inc.', 'base_price': 150},
            {'symbol': 'BANK', 'name': 'Banking Solutions', 'base_price': 80},
            {'symbol': 'RETAIL', 'name': 'Retail Giant', 'base_price': 120},
            {'symbol': 'ENERGY', 'name': 'Energy Systems', 'base_price': 60},
            {'symbol': 'HEALTH', 'name': 'HealthTech Ltd.', 'base_price': 200}
        ]
        
        start_date = datetime.now() - timedelta(days=num_days)
        
        all_data = []
        
        for company in companies:
            symbol = company['symbol']
            current_price = company['base_price']
            
            for i in range(num_days):
                current_date = start_date + timedelta(days=i)
                
                # Skip weekends
                if current_date.weekday() >= 5:
                    continue
                
                # Random walk with trend
                daily_return = np.random.normal(0.001, 0.02)  # Slight positive trend with volatility
                current_price *= (1 + daily_return)
                
                # Generate OHLC data
                open_price = current_price
                close_price = current_price * (1 + np.random.normal(0, 0.015))
                
                high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.01)))
                low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.01)))
                
                # Volume (higher volume on volatile days)
                volatility = abs(close_price - open_price) / open_price
                base_volume = 1000000
                volume = int(base_volume * (1 + volatility * 5) * np.random.lognormal(0, 0.5))
                
                current_price = close_price  # Update for next day
                
                all_data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'symbol': symbol,
                    'company_name': company['name'],
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': volume,
                    'daily_return': round(daily_return * 100, 3)  # Percentage
                })
        
        return pd.DataFrame(all_data)
    
    def generate_customer_data(self, num_customers: int = 500) -> pd.DataFrame:
        """
        Generate synthetic customer data.
        
        Args:
            num_customers: Number of customer records to generate
            
        Returns:
            DataFrame with customer demographics and behavior data
        """
        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson'
        ]
        
        cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
            'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
            'San Francisco', 'Columbus', 'Indianapolis', 'Fort Worth', 'Charlotte', 'Seattle'
        ]
        
        occupations = [
            'Engineer', 'Teacher', 'Manager', 'Analyst', 'Developer', 'Designer',
            'Consultant', 'Salesperson', 'Accountant', 'Nurse', 'Doctor', 'Lawyer',
            'Marketing Specialist', 'Project Manager', 'Data Scientist', 'Writer'
        ]
        
        data = []
        for i in range(num_customers):
            customer_id = f"CUST{1000 + i}"
            
            # Demographics
            age = np.random.choice(range(18, 80), p=self._age_distribution())
            
            # Income correlated with age and occupation
            base_income = 40000 + (age - 18) * 1000 + np.random.normal(0, 15000)
            income = max(25000, base_income)
            
            # Spending behavior
            monthly_spending = income * 0.1 * (0.5 + random.random())  # 5-15% of income
            
            # Loyalty score (0-100)
            loyalty_score = np.random.beta(2, 5) * 100  # Skewed towards lower scores
            
            # Registration date (within last 3 years)
            reg_date = datetime.now() - timedelta(days=random.randint(1, 1095))
            
            data.append({
                'customer_id': customer_id,
                'first_name': random.choice(first_names),
                'last_name': random.choice(last_names),
                'age': age,
                'city': random.choice(cities),
                'occupation': random.choice(occupations),
                'annual_income': round(income),
                'monthly_spending': round(monthly_spending, 2),
                'loyalty_score': round(loyalty_score, 1),
                'registration_date': reg_date.strftime('%Y-%m-%d'),
                'preferred_category': random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books']),
                'email_subscribed': random.choice([True, False]),
                'total_orders': np.random.poisson(12),  # Average 12 orders
                'last_purchase_days_ago': random.randint(1, 180)
            })
        
        return pd.DataFrame(data)
    
    def _get_season(self, month: int) -> str:
        """Get season based on month."""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    def _age_distribution(self) -> List[float]:
        """Get realistic age distribution for customer data."""
        # Create age distribution that roughly matches real demographics
        ages = range(18, 80)
        # Younger adults have higher probability, with peak around 25-35
        probs = []
        for age in ages:
            if 25 <= age <= 35:
                prob = 0.025
            elif 18 <= age <= 24 or 36 <= age <= 45:
                prob = 0.02
            elif 46 <= age <= 55:
                prob = 0.015
            elif 56 <= age <= 65:
                prob = 0.01
            else:
                prob = 0.005
            probs.append(prob)
        
        # Normalize probabilities
        total = sum(probs)
        return [p / total for p in probs]
