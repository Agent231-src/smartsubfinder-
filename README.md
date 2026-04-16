# SmartSubfinder 🚀

Advanced subdomain enumeration tool with priority scoring and interactive visualization. It combines multiple discovery methods into a single, high-performance workflow.

## Features
- Passive Recon: Aggregates data from crt.sh, ThreatCrowd, and other public sources.
- Active Discovery: High-speed brute-force engine with intelligent permutation logic.
- External Intelligence: Full Shodan and Censys API support.
- Priority Scoring: Algorithmic identification of high-value targets based on open ports and services.
- Visual Mapping: Built-in interactive graph-based dashboard for network analysis.

## Installation
git clone https://github.com/Agent231-src/smartsubfinder-
cd smartsubfinder-
pip3 install -r requirements.txt

## External API Setup (Optional)
To enhance your results with Shodan data:
1. Register at account.shodan.io
2. Go to your Dashboard and copy the API Key (Free tier: 100 queries/day)

## Usage Examples

1. Basic Scan
Quick passive and active enumeration for a target domain:
python3 main.py google.com

2. Full Intelligence Scan
Use Shodan to identify services and save results to a JSON file:
python3 main.py hackerone.com --shodan-key YOUR_KEY_HERE --output results.json

3. Web Dashboard
Launch the interactive web interface to visualize the subdomain infrastructure:
python3 main.py tesla.com --web

---
*Disclaimer: This tool is for educational and ethical security testing purposes only.*
