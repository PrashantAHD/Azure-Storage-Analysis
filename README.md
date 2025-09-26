# Azure Storage Analysis & Dashboard

> **🎯 Unified Single-Command Solution for Azure Storage Cost Intelligence**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure](https://img.shields.io/badge/azure-storage-0078d4.svg)](https://azure.microsoft.com/en-us/services/storage/)
[![Architecture](https://img.shields.io/badge/architecture-unified-success.svg)](#)

**Developed by [Prashant Kumar](https://www.linkedin.com/in/iprashantkr), Cloud & DevOps Engineer @AHEAD**

---

## 📖 Table of Contents

- [What This Project Achieves](#what-this-project-achieves)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Architecture](#project-architecture)
- [What Gets Generated](#what-gets-generated)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 What This Project Achieves

### **Business Value**
This project delivers a **complete Azure FinOps solution** that transforms complex Azure storage cost management into actionable insights through:

- **💰 Cost Optimization**: Identify potential savings opportunities across Azure storage accounts
- **📊 Executive Reporting**: Generate professional CIR (Cost Intelligence Reports) for stakeholders
- **🔍 Real-time Analysis**: Monitor storage usage patterns and cost trends in real-time
- **🏢 Enterprise Scale**: Handle both single-subscription and multi-subscription environments
- **⚡ Operational Efficiency**: Reduce time from hours to minutes for comprehensive Azure analysis

### **Technical Achievement**
- **Single Command Solution**: Eliminates complex multi-step processes
- **Intelligent Auto-Detection**: Automatically adapts to your Azure environment
- **Professional Grade**: Enterprise-ready with comprehensive error handling
- **Modern Interface**: Web-based dashboard with interactive visualizations

---

## ✨ Key Features

### 🚀 **Unified Architecture**
- **One Command Execution**: `python start.py` handles everything
- **Smart Detection**: Auto-detects single vs multi-subscription scenarios
- **Seamless Integration**: Analysis → Excel → Dashboard in one workflow

### 📊 **Professional Reporting**
- **8 Comprehensive Excel Sheets**: Executive summary, detailed analysis, recommendations
- **Real-time Web Dashboard**: Interactive charts and visualizations
- **CIR (Cost Intelligence Reports)**: Professional cost tracking and analysis

### 🔧 **Enterprise Features**
- **Multi-Subscription Support**: Analyze across multiple Azure subscriptions
- **Cost Optimization Engine**: AI-powered savings recommendations
- **Live Data Integration**: Real-time Azure storage account monitoring
- **Scalable Architecture**: Handles large-scale enterprise environments

---

## 📋 Prerequisites

### **System Requirements**
- **Python**: 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large environments)
- **Disk Space**: 1GB free space for reports and analysis data

### **Azure Access Requirements**
- **Azure Subscription**: Active Azure subscription with storage accounts
- **Permissions**: 
  - `Storage Account Reader` role (minimum)
  - `Storage Blob Data Reader` (for detailed container analysis)
  - `Cost Management Reader` (for cost data access)

### **Authentication Setup**
Choose **one** of the following methods:

#### Option 1: Azure CLI (Recommended)
```bash
# Install Azure CLI from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
az login
az account set --subscription "your-subscription-name-or-id"
```

#### Option 2: Service Principal
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

#### Option 3: Managed Identity
```bash
# If running on Azure VM with managed identity
# No additional setup required
```

---

## 🚀 Quick Start

### **1. Clone & Setup**
```bash
git clone https://github.com/PrashantAHD/Azure-Storage-Analysis.git
cd Azure-Storage-Analysis
pip install -r requirements.txt
```

### **2. Authenticate with Azure**
```bash
az login  # Follow the browser authentication
```

### **3. Run Complete Analysis**
```bash
python start.py
```

### **4. Access Results**
- **Dashboard**: http://localhost:5000
- **Excel Reports**: Check current directory for `azure_finops_comprehensive_analysis_*.xlsx`
- **JSON Data**: Analysis results saved as `detailed_analysis_results_*.json`

---

## 🏗️ Project Architecture

### **Unified File Structure**
```
Azure-Storage-Analysis/
├── 🚀 start.py                         # Main Entry Point (START HERE)
├── 🔍 unified_azure_analysis.py        # Complete Analysis Engine  
├── 📊 real_data_dashboard.py           # Universal CIR Dashboard
├── 📋 requirements.txt                 # Python Dependencies
├── 📖 README.md                        # This Documentation
├── 🚫 .gitignore                       # Git Exclusions
└── 📦 azure_storage_analysis/          # Core Framework Modules
    ├── auth.py                         # Authentication & Subscription Management
    ├── core.py                         # Storage Analysis Engine
    ├── cost_management.py              # Cost Analysis APIs
    ├── reservations.py                 # Reserved Instances Analysis
    ├── savings_plans.py                # Savings Plans Optimization
    ├── enhanced_reporting.py           # Advanced Reporting Features
    ├── unified_reporting.py            # Excel CIR Report Generation
    ├── recommendations.py              # Cost Optimization Recommendations
    └── utils.py                        # Utility Functions
```

### **Architecture Benefits**
- ✅ **Single Entry Point**: No confusion about which script to run
- ✅ **Modular Design**: Easy to extend and maintain
- ✅ **Clean Dependencies**: Clear separation of concerns
- ✅ **No Redundancy**: Eliminated duplicate code and separate workflows

---

## 📊 What Gets Generated

### **Excel CIR Reports (8 Comprehensive Sheets)**
1. **Executive Summary** - High-level cost intelligence overview for leadership
2. **Summary** - Detailed subscription and storage account breakdown  
3. **Blob Storage Analysis** - Container-level analysis with size and usage metrics
4. **Azure Files Analysis** - File share usage patterns and optimization opportunities
5. **Storage Analysis** - Combined storage overview with trends and insights
6. **Recommendations** - Actionable cost optimization and management suggestions
7. **Cost Optimization** - Advanced financial recommendations with savings calculations
8. **Detailed Data** - Raw data for custom analysis and further investigation

### **Live Web Dashboard**
- **Real-time Interface**: Professional web dashboard at http://localhost:5000
- **Interactive Charts**: Powered by Chart.js with drill-down capabilities
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Live Data Updates**: Automatic refresh of Azure data

### **Analysis Data Files**
- **Single Subscription**: `detailed_analysis_results_YYYYMMDD_HHMMSS.json`
- **Multi-Subscription**: `multi_subscription_analysis_YYYYMMDD_HHMMSS.json`

---

## 💻 Usage Examples

### **Basic Usage (Most Common)**
```bash
python start.py
```
*Automatically detects your environment and guides you through the process*

### **Direct Analysis Only**
```bash
python unified_azure_analysis.py
```
*Run analysis and generate Excel reports without starting the dashboard*

### **Dashboard Only (After Analysis)**
```bash
python real_data_dashboard.py
```
*Start the web dashboard using previously generated analysis data*

### **Subscription Selection Examples**
When prompted by `start.py`, you can choose:
- **Option 1**: Detailed single-subscription analysis
- **Option 2**: Enterprise multi-subscription view
- **Option 3**: Auto-detect (recommended for most users)

---

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### Authentication Problems
```bash
# Clear and re-authenticate
az logout
az login
az account show  # Verify login
```

#### Permission Errors
- Ensure you have `Storage Account Reader` role
- Check subscription access: `az account list`
- Verify resource group permissions

#### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

#### Dashboard Not Loading
- Check if port 5000 is available
- Verify analysis data exists (JSON files in current directory)
- Try running analysis first: `python unified_azure_analysis.py`

#### Excel Generation Fails
```bash
# Update Excel dependencies
pip install --upgrade openpyxl pandas
```

### **Debug Mode**
For detailed troubleshooting information:
```bash
# Set debug environment variable
export AZURE_STORAGE_DEBUG=1  # Linux/Mac
set AZURE_STORAGE_DEBUG=1     # Windows
python start.py
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Ways to Contribute**
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/PrashantAHD/Azure-Storage-Analysis/issues)
- 💡 **Feature Requests**: Use GitHub Issues with enhancement label
- 🔧 **Code Contributions**: Submit Pull Requests
- 📖 **Documentation**: Improve README, add examples
- 🧪 **Testing**: Test with different Azure environments

### **Development Setup**
```bash
git clone https://github.com/PrashantAHD/Azure-Storage-Analysis.git
cd Azure-Storage-Analysis
pip install -r requirements.txt
# Make your changes
# Test thoroughly
# Submit Pull Request
```

---

## 📞 Support & Resources

### **Getting Help**
- **Issues**: [GitHub Issues](https://github.com/PrashantAHD/Azure-Storage-Analysis/issues)
- **Email**: [prashant271227@gmail.com](mailto:prashant271227@gmail.com)

### **Useful Azure Resources**
- [Azure Storage Pricing](https://azure.microsoft.com/en-us/pricing/details/storage/)
- [Azure Cost Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/)
- [Azure Storage Best Practices](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview)

---

## 👨‍💻 About the Author

**[Prashant Kumar](https://www.linkedin.com/in/iprashantkr)**

Cloud DevOps Engineer @AHEAD with 4+ years of experience specializing in:
- **Cloud Platforms**: AWS, Azure, GCP
- **Expertise**: Cloud Security, DevOps, FinOps, Site Reliability Engineering
- **Specialization**: Managing scalable platforms serving millions of users

### **Certifications**
- [AWS Certified DevOps Engineer - Professional](https://www.credly.com/badges/72e67681-2adc-4eff-8f31-e565b7596838/public_url)
- [AWS Certified Solutions Architect - Professional](https://www.credly.com/badges/410997f9-2d5d-43bb-9660-4bd38fc928b7/public_url)
- [Microsoft Certified: DevOps Engineer Expert](https://learn.microsoft.com/api/credentials/share/en-us/PrashantKumar-1984/2B555C9A9A693129?sharingId=AB54B2AF1407CBA8)
- [Microsoft Certified: Azure Administrator Associate](https://learn.microsoft.com/api/credentials/share/en-us/PrashantKumar-1984/1B89518218F2550A?sharingId=AB54B2AF1407CBA8)


---


## ⭐ Show Your Support

If this project helps you save time and money on Azure costs, please consider:
- ⭐ **Star this repository** on GitHub
- 🐛 **Report issues** to help improve the project
- 💡 **Suggest features** for future releases
- 🔄 **Share** with your team and network

---

**🎯 Azure FinOps Dashboard - Transform Azure Storage Cost Management with a Single Command** 🎯
