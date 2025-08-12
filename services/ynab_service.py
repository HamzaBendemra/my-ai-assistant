# services/ynab_service.py
# Replace the get_current_month_budget method with this corrected version:

import os
import requests
import streamlit as st
from datetime import datetime
from typing import Dict, Optional

class YNABService:
    def __init__(self, default_budget_name: Optional[str] = None):
        self.access_token = st.secrets["YNAB_ACCESS_TOKEN"]
        self.base_url = "https://api.youneedabudget.com/v1"
        # Use provided name, environment variable, or None
        self.default_budget_name = (
            default_budget_name or 
            st.secrets["YNAB_DEFAULT_BUDGET_NAME"]
        )
        
        if not self.access_token:
            self.is_connected = False
        else:
            self.is_connected = True
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
    
    def list_budget_names(self):
        """Helper method to see all available budget names"""
        budgets = self.get_budgets()
        if budgets:
            return [budget["name"] for budget in budgets]
        return []
    
    def get_budgets(self):
        """Get all budgets"""
        if not self.is_connected:
            return None
            
        try:
            response = requests.get(
                f"{self.base_url}/budgets",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()["data"]["budgets"]
        except Exception as e:
            st.error(f"YNAB Error: {str(e)}")
            return None
    
    def get_current_month_budget(self, budget_name: Optional[str] = None) -> Optional[Dict]:
        """Get current month's budget summary"""
        if not self.is_connected:
            return None
            
        try:
            # Get all budgets
            budgets = self.get_budgets()
            if not budgets:
                return None
            
            # Find budget by name if specified, otherwise use first one
            budget_name_to_use = budget_name or self.default_budget_name
            if budget_name_to_use:
                budget = next((b for b in budgets if b["name"] == budget_name_to_use), None)
                if not budget:
                    st.error(f"Budget '{budget_name_to_use}' not found. Available budgets: {[b['name'] for b in budgets]}")
                    return None
                budget_id = budget["id"]
            else:
                budget_id = budgets[0]["id"]
            
            # Use 'current' for the current month instead of a specific date
            # This ensures we always get valid data
            response = requests.get(
                f"{self.base_url}/budgets/{budget_id}/months/current",
                headers=self.headers
            )
            response.raise_for_status()
            
            month_data = response.json()["data"]["month"]
            
            # Process the data
            summary = {
                "month": month_data["month"],  # This will be the actual month from YNAB
                "budgeted": month_data["budgeted"] / 1000,  # Convert from milliunits
                "spent": abs(month_data["activity"]) / 1000,
                "remaining": (month_data["budgeted"] + month_data["activity"]) / 1000,
                "categories": [],
                "age_of_money": month_data.get("age_of_money", 0)
            }
            
            # Filter out internal categories and get top spending
            valid_categories = [
                cat for cat in month_data["categories"] 
                if not cat["hidden"] and 
                cat["name"] not in ["Inflow: Ready to Assign", "Internal Master Category"] and
                cat["activity"] < 0  # Only categories with spending
            ]
            
            # Sort by spending amount
            categories = sorted(
                valid_categories, 
                key=lambda x: abs(x["activity"]), 
                reverse=True
            )[:5]
            
            for cat in categories:
                summary["categories"].append({
                    "name": cat["name"],
                    "budgeted": cat["budgeted"] / 1000,
                    "spent": abs(cat["activity"]) / 1000,
                    "remaining": cat["balance"] / 1000
                })
            
            return summary
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                st.error("YNAB budget not found. Please check your access token.")
            else:
                st.error(f"YNAB HTTP Error: {e}")
            return None
        except Exception as e:
            st.error(f"YNAB Error: {str(e)}")
            return None
    
    def get_budget_context_for_llm(self, budget_name: Optional[str] = None) -> str:
        """Format budget data for Claude"""
        summary = self.get_current_month_budget(budget_name)
        if not summary:
            return "Budget information not available."
        
        context = f"""Current Month Budget ({summary['month']}):
- Total Budgeted: ${summary['budgeted']:,.2f}
- Total Spent: ${summary['spent']:,.2f}
- Remaining: ${summary['remaining']:,.2f}
- Age of Money: {summary.get('age_of_money', 'N/A')} days

Top Spending Categories:"""
        
        for cat in summary['categories']:
            context += f"\n- {cat['name']}: ${cat['spent']:,.2f} of ${cat['budgeted']:,.2f}"
        
        return context