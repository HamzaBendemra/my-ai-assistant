# services/ynab_service.py
import os
import requests
import streamlit as st
from datetime import datetime
from typing import Dict, Optional

class YNABService:
    def __init__(self):
        self.access_token = os.getenv("YNAB_ACCESS_TOKEN") or st.secrets.get("YNAB_ACCESS_TOKEN")
        self.base_url = "https://api.youneedabudget.com/v1"
        
        if not self.access_token:
            self.is_connected = False
        else:
            self.is_connected = True
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
    
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
    
    def get_current_month_budget(self) -> Optional[Dict]:
        """Get current month's budget summary"""
        if not self.is_connected:
            return None
            
        try:
            # Get first budget (usually the main one)
            budgets = self.get_budgets()
            if not budgets:
                return None
                
            budget_id = budgets[0]["id"]
            current_month = datetime.now().strftime("%Y-%m-01")
            
            # Get month data
            response = requests.get(
                f"{self.base_url}/budgets/{budget_id}/months/{current_month}",
                headers=self.headers
            )
            response.raise_for_status()
            
            month_data = response.json()["data"]["month"]
            
            # Process the data
            summary = {
                "month": current_month,
                "budgeted": month_data["budgeted"] / 1000,  # Convert from milliunits
                "spent": abs(month_data["activity"]) / 1000,
                "remaining": (month_data["budgeted"] + month_data["activity"]) / 1000,
                "categories": []
            }
            
            # Get top 5 categories by spending
            categories = sorted(
                month_data["categories"], 
                key=lambda x: abs(x["activity"]), 
                reverse=True
            )[:5]
            
            for cat in categories:
                if cat["name"] != "Inflow: Ready to Assign":
                    summary["categories"].append({
                        "name": cat["name"],
                        "budgeted": cat["budgeted"] / 1000,
                        "spent": abs(cat["activity"]) / 1000,
                        "remaining": cat["balance"] / 1000
                    })
            
            return summary
            
        except Exception as e:
            st.error(f"YNAB Error: {str(e)}")
            return None
    
    def get_budget_context_for_llm(self) -> str:
        """Format budget data for Claude"""
        summary = self.get_current_month_budget()
        if not summary:
            return "Budget information not available."
        
        context = f"""Current Month Budget:
- Total Budgeted: ${summary['budgeted']:,.2f}
- Total Spent: ${summary['spent']:,.2f}
- Remaining: ${summary['remaining']:,.2f}

Top Spending Categories:"""
        
        for cat in summary['categories']:
            context += f"\n- {cat['name']}: ${cat['spent']:,.2f} of ${cat['budgeted']:,.2f}"
        
        return context