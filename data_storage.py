"""
Data Storage Module

This module provides functionality to save and load data in various formats
including CSV, JSON, and other common data formats.
"""

import pandas as pd
import json
import os
from pathlib import Path
from typing import Dict, Any, Union
from rich import print

class DataStorage:
    """Handles saving and loading data in various formats."""
    
    def __init__(self, base_path: str = "Data"):
        """
        Initialize the data storage handler.
        
        Args:
            base_path: Base directory for storing data files
        """
        self.base_path = Path(base_path)
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create the data directory if it doesn't exist."""
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
            print(f"[green]✓[/green] Created directory: {self.base_path}")
    
    def save_to_csv(self, data: pd.DataFrame, filename: str, index: bool = False) -> str:
        """
        Save DataFrame to CSV format.
        
        Args:
            data: DataFrame to save
            filename: Name of the CSV file
            index: Whether to include row indices
            
        Returns:
            Full path of the saved file
        """
        filepath = self.base_path / filename
        data.to_csv(filepath, index=index)
        print(f"[green]✓[/green] Saved CSV: {filepath} ({len(data)} records)")
        return str(filepath)
    
    def save_to_json(self, data: pd.DataFrame, filename: str, orient: str = 'records') -> str:
        """
        Save DataFrame to JSON format.
        
        Args:
            data: DataFrame to save
            filename: Name of the JSON file
            orient: JSON orientation ('records', 'index', 'values', etc.)
            
        Returns:
            Full path of the saved file
        """
        filepath = self.base_path / filename
        
        # Convert DataFrame to JSON
        if orient == 'records':
            json_data = data.to_dict('records')
        else:
            json_data = data.to_dict(orient)
        
        # Save with pretty formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"[green]✓[/green] Saved JSON: {filepath} ({len(data)} records)")
        return str(filepath)
    
    def save_to_excel(self, data: Union[pd.DataFrame, Dict[str, pd.DataFrame]], filename: str) -> str:
        """
        Save DataFrame(s) to Excel format.
        
        Args:
            data: DataFrame or dictionary of DataFrames for multiple sheets
            filename: Name of the Excel file
            
        Returns:
            Full path of the saved file
        """
        filepath = self.base_path / filename
        
        if isinstance(data, pd.DataFrame):
            data.to_excel(filepath, index=False)
            print(f"[green]✓[/green] Saved Excel: {filepath} ({len(data)} records)")
        else:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"[green]✓[/green] Saved Excel: {filepath} ({len(data)} sheets)")
        
        return str(filepath)
    
    def load_from_csv(self, filename: str) -> pd.DataFrame:
        """
        Load DataFrame from CSV format.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            Loaded DataFrame
        """
        filepath = self.base_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        data = pd.read_csv(filepath)
        print(f"[blue]📖[/blue] Loaded CSV: {filepath} ({len(data)} records)")
        return data
    
    def load_from_json(self, filename: str) -> pd.DataFrame:
        """
        Load DataFrame from JSON format.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Loaded DataFrame
        """
        filepath = self.base_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        data = pd.DataFrame(json_data)
        print(f"[blue]📖[/blue] Loaded JSON: {filepath} ({len(data)} records)")
        return data
    
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """
        Get information about a data file.
        
        Args:
            filename: Name of the file
            
        Returns:
            Dictionary with file information
        """
        filepath = self.base_path / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = filepath.stat()
        return {
            'filename': filename,
            'full_path': str(filepath),
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'extension': filepath.suffix
        }
    
    def list_files(self, extension: str = None) -> list:
        """
        List all files in the data directory.
        
        Args:
            extension: Filter by file extension (e.g., '.csv', '.json')
            
        Returns:
            List of filenames
        """
        if not self.base_path.exists():
            return []
        
        files = []
        for file in self.base_path.iterdir():
            if file.is_file():
                if extension is None or file.suffix.lower() == extension.lower():
                    files.append(file.name)
        
        return sorted(files)
    
    def create_data_summary(self) -> Dict[str, Any]:
        """
        Create a summary of all data files in the directory.
        
        Returns:
            Dictionary with summary information
        """
        summary = {
            'total_files': 0,
            'total_size_mb': 0,
            'file_types': {},
            'files': []
        }
        
        if not self.base_path.exists():
            return summary
        
        for file in self.base_path.iterdir():
            if file.is_file():
                stat = file.stat()
                size_mb = stat.st_size / (1024 * 1024)
                
                summary['total_files'] += 1
                summary['total_size_mb'] += size_mb
                
                ext = file.suffix.lower()
                summary['file_types'][ext] = summary['file_types'].get(ext, 0) + 1
                
                summary['files'].append({
                    'name': file.name,
                    'size_mb': round(size_mb, 2),
                    'type': ext
                })
        
        summary['total_size_mb'] = round(summary['total_size_mb'], 2)
        return summary
    
    def backup_data(self, backup_dir: str = "Backup") -> str:
        """
        Create a backup of all data files.
        
        Args:
            backup_dir: Directory name for backup
            
        Returns:
            Path to backup directory
        """
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        if self.base_path.exists():
            for file in self.base_path.iterdir():
                if file.is_file():
                    shutil.copy2(file, backup_path / file.name)
        
        print(f"[green]✓[/green] Created backup: {backup_path}")
        return str(backup_path)
