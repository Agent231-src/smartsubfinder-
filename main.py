#!/usr/bin/env python3
import argparse
import sys
from subfinder import SubdomainFinder
from ml_analyzer import MLAnalyzer
from visualizer import GraphVisualizer
import subprocess

def main():
    parser = argparse.ArgumentParser(description='SmartSubfinder: AI-Powered Subdomain Enumeration')
    parser.add_argument('domain', help='Target domain e.g. example.com')
    parser.add_argument('-o', '--output', help='Output JSON file')
    parser.add_argument('--shodan-key', help='Shodan API key')
    parser.add_argument('--web', action='store_true', help='Start web UI')
    
    args = parser.parse_args()
    
    if not args.domain:
        print("Usage: python3 main.py example.com")
        sys.exit(1)
    
    print(f"[+] Starting recon on {args.domain}")
    
    # 1. Subdomain enum
    finder = SubdomainFinder(args.domain, shodan_key=args.shodan_key)
    subs = finder.find_all()
    
    # 2. ML analysis
    analyzer = MLAnalyzer()
    scored_subs = analyzer.score_subdomains(subs)
    
    # 3. Visualize
    viz = GraphVisualizer(args.domain, scored_subs)
    viz.generate_graph('graph.png')
    
    # Output
    results = {'domain': args.domain, 'subdomains': scored_subs}
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
    
    print(f"[+] Found {len(scored_subs)} subdomains. High-value: {len([s for s in scored_subs if s['score'] > 0.8])}")
    print("[+] Graph saved: graph.png")
    
    if args.web:
        viz.start_web_ui()

if __name__ == '__main__':
    main()
