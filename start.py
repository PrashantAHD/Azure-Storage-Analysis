#!/usr/bin/env python3
"""
Unified Azure FinOps CIR Dashboard + Excel Report Generator
Single command for analysis, dashboard, and Excel reports
"""

import subprocess
import sys
import os
import threading
import time

def run_analysis_with_excel():
    """Run analysis and generate Excel reports"""
    print("\n🔍 STEP 1: Running Azure Analysis + Excel Generation")
    print("=" * 60)
    
    # Ask user for subscription preference
    print("\n📋 SUBSCRIPTION SELECTION:")
    print("1. Single Subscription Analysis (detailed)")
    print("2. Multi-Subscription Analysis (enterprise view)")
    
    while True:
        choice = input("\nChoose analysis mode (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("❌ Please enter 1 or 2")
    
    try:
        if choice == '1':
            print("\n� Running single-subscription analysis with Excel generation...")
            subprocess.run([sys.executable, "show_detailed_data.py"], check=True)
        else:
            print("\n🔍 Running multi-subscription analysis with Excel generation...")
            subprocess.run([sys.executable, "show_multi_subscription_data.py"], check=True)
        
        print("✅ Analysis completed with Excel CIR reports generated!")
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def start_dashboard():
    """Start the CIR dashboard"""
    print("\n📊 STEP 2: Starting CIR Dashboard")
    print("=" * 60)
    print("🌐 Dashboard URL: http://localhost:5000")
    print("💡 Features: Cost Intelligence Reports (CIR), Multi/Single Subscription support")
    print("📋 Excel CIR Reports: Generated automatically during analysis")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, "real_data_dashboard.py"], check=True)
    except KeyboardInterrupt:
        print("\n✅ Dashboard stopped")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def main():
    """Unified Azure FinOps CIR platform launcher"""
    print("🚀 UNIFIED AZURE FINOPS CIR PLATFORM")
    print("=" * 60)
    print("🎯 Features:")
    print("  • Single & Multi-Subscription Support")
    print("  • Cost Intelligence Reports (CIR)")
    print("  • Automatic Excel Report Generation")
    print("  • Professional Dashboard with Charts")
    print("=" * 60)
    
    # Step 1: Run analysis with Excel generation
    if not run_analysis_with_excel():
        print("❌ Cannot continue without analysis data")
        return
    
    print("\n⏳ Starting dashboard in 3 seconds...")
    time.sleep(3)
    
    # Step 2: Start dashboard
    start_dashboard()

if __name__ == "__main__":
    main()