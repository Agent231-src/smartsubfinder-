import requests
import dns.resolver
import dns.reversename
from tldextract import extract
import threading
from concurrent.futures import ThreadPoolExecutor
import shodan

class Subfinder:
    def __init__(self, domain, shodan_key=None):
        self.domain = self._clean_domain(domain)
        self.shodan_key = shodan_key
        self.results = set()
        
    def _clean_domain(self, domain):
        _, _, suffix = extract(domain)
        return f'*.{suffix}' if '*' in domain else domain
    
    def passive_enum(self):
        """Passive sources: crt.sh, threatcrowd, etc."""
        urls = [
            f"https://crt.sh/?q=%.{self.domain}&output=json",
            f"https://api.threatcrowd.org/v1/domain/report?domain={self.domain}"
        ]
        for url in urls:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    for item in data:
                        if isinstance(item, dict):
                            sub = item.get('name_value', item.get('subdomain'))
                            if sub:
                                self.results.add(sub.lower())
            except:
                pass
    
    def brute_force(self, wordlist_size=1000):
        """Common subdomains brute"""
        common_subs = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api', 'app']
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self._check_sub, sub) for sub in common_subs * 10]
            for future in futures:
                future.result()
    
    def _check_sub(self, sub):
        try:
            answers = dns.resolver.resolve(f'{sub}.{self.domain}', 'A')
            self.results.add(f'{sub}.{self.domain}')
        except:
            pass
    
    def shodan_enum(self):
        if not self.shodan_key:
            return
        try:
            api = shodan.Shodan(self.shodan_key)
            results = api.host_search(f'hostname:{self.domain}')
            for host in results['matches']:
                self.results.add(host['hostnames'][0] if host['hostnames'] else host['ip_str'])
        except:
            pass
    
    def find_all(self):
        threads = []
        funcs = [self.passive_enum, self.brute_force, self.shodan_enum]
        for func in funcs:
            t = threading.Thread(target=func)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        return list(self.results)
