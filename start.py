#!/usr/bin/env python3
"""
Unified Azure FinOps CIR Dashboard Launcher
Single command for analysis, dashboard, and Excel reports
"""

import subprocess
import sys
import os
import threading
import time

def run_analysis_with_excel():
    """Run unified analysis and generate Excel reports"""
    print("\n🔍 STEP 1: Running Unified Azure Analysis + Excel Generation")
    print("=" * 60)
    
    try:
        print("🚀 Launching unified analysis engine with intelligent subscription detection...")
        subprocess.run([sys.executable, "unified_azure_analysis.py"], check=True)
        
        print("✅ Unified analysis completed with Excel CIR reports generated!")
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def start_dashboard():
    """Start the unified CIR dashboard"""
    print("\n📊 STEP 2: Starting Unified CIR Dashboard")
    print("=" * 60)
    print("🌐 Dashboard URL: http://localhost:5000")
    print("💡 Features: Intelligent Single/Multi-Subscription Detection")
    print("📋 Excel CIR Reports: Generated automatically during analysis")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        # Start dashboard in background
        dashboard_process = subprocess.Popen([sys.executable, "real_data_dashboard.py"])
        return dashboard_process
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        return None

def main():
    """Main unified launcher"""
    print("🚀 UNIFIED AZURE FINOPS CIR SYSTEM")
    print("=" * 80)
    print("📊 Complete solution: Analysis + Excel Reports + Dashboard")
    print("🤖 Intelligent single/multi-subscription detection")
    print("🎯 One command - Full CIR solution")
    print("=" * 80)
    
    # Step 1: Run analysis
    if not run_analysis_with_excel():
        print("\n❌ Exiting due to analysis failure")
        return
    
    # Step 2: Start dashboard
    dashboard_process = start_dashboard()
    if not dashboard_process:
        print("\n❌ Dashboard failed to start")
        return
    
    print("\n✅ UNIFIED CIR SYSTEM ACTIVE!")
    print("=" * 80)
    print("📊 Dashboard: http://localhost:5000")
    print("📋 Excel Reports: Check current directory for latest CIR files")
    print("🔄 Analysis: Completed with intelligent subscription detection")
    
    try:
        # Keep main process alive
        print("\n⏳ System running... Press Ctrl+C to stop everything")
        dashboard_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down unified system...")
        dashboard_process.terminate()
        dashboard_process.wait()
        print("✅ Clean shutdown complete")

if __name__ == "__main__":
    main()