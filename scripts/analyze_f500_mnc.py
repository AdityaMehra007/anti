import csv
import re
from collections import defaultdict

with open(r'e:\anti\linkedin_export\Connections.csv', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:10]):
    if 'First Name' in line and 'Company' in line:
        start_idx = i
        break

reader = csv.DictReader(lines[start_idx:])
connections = list(reader)

# Canonical F500 & MNC Catalog
# Format: (canonical_name, regex_pattern, is_f500, is_global_mnc, sector)
f500_mnc_defs = [
    # Big Tech & Cloud
    ('Amazon / AWS', r'\b(amazon|aws|amazon web services)\b', True, True, 'Big Tech, Cloud & E-Commerce'),
    ('Microsoft', r'\bmicrosoft\b', True, True, 'Big Tech & Cloud Software'),
    ('Google / Alphabet', r'\b(google|alphabet)\b', True, True, 'Big Tech & AI'),
    ('IBM', r'\b(ibm|international business machines)\b', True, True, 'Enterprise Tech & Hybrid Cloud'),
    ('Cisco Systems', r'\bcisco\b', True, True, 'Networking & Tech Infrastructure'),
    ('Oracle', r'\boracle\b', True, True, 'Enterprise Software & Cloud'),
    ('Dell Technologies', r'\bdell\b', True, True, 'Hardware & Cloud Infrastructure'),
    ('Intel', r'\bintel\b', True, True, 'Semiconductors & Compute'),
    ('HP / HPE', r'\b(hewlett packard|hp inc|hpe)\b', True, True, 'Enterprise Hardware & Tech'),
    ('SAP', r'\b(sap labs|sap se|sap india|sap)\b', True, True, 'Enterprise Software & ERP'),
    ('Salesforce', r'\bsalesforce\b', True, True, 'Enterprise SaaS & CRM'),
    ('Adobe', r'\badobe\b', True, True, 'Creative & Document Cloud'),
    ('Qualcomm', r'\bqualcomm\b', True, True, 'Wireless & Semiconductors'),
    ('Apple', r'\bapple\b', True, True, 'Consumer Hardware & OS'),
    ('Meta', r'\b(meta|facebook)\b', True, True, 'Social Tech & AI'),
    ('ServiceNow', r'\bservicenow\b', True, True, 'Enterprise Cloud Workflow'),
    ('Uber', r'\buber\b', True, True, 'Mobility & Delivery Tech'),
    ('PayPal', r'\bpaypal\b', True, True, 'Digital Payments & FinTech'),

    # Big 4 & Global Strategy Consulting
    ('EY (Ernst & Young)', r'\b(ey|ernst & young|ernst and young)\b', False, True, 'Big 4 / Global Professional Services'),
    ('Deloitte', r'\bdeloitte\b', True, True, 'Big 4 / Consulting & Advisory (Fortune Global 500)'),
    ('PwC (PricewaterhouseCoopers)', r'\b(pwc|pricewaterhousecoopers)\b', False, True, 'Big 4 / Global Professional Services'),
    ('KPMG', r'\bkpmg\b', False, True, 'Big 4 / Global Advisory & Tax'),
    ('Accenture', r'\baccenture\b', True, True, 'Global Strategy & IT Consulting (Fortune 500)'),
    ('McKinsey & Company', r'\bmckinsey\b', False, True, 'Management Consulting (Global MNC)'),
    ('Boston Consulting Group (BCG)', r'\b(boston consulting|bcg)\b', False, True, 'Management Consulting (Global MNC)'),
    ('Bain & Company', r'\b(bain & company|bain & co|bain)\b', False, True, 'Management Consulting (Global MNC)'),

    # Global IT Services & Tech Services Giants
    ('Tata Consultancy Services (TCS)', r'\b(tcs|tata consultancy services)\b', True, True, 'IT Services & Digital Transformation (Fortune India 500)'),
    ('Infosys', r'\b(infosys|infosys bpm)\b', True, True, 'IT Services & Consulting (Fortune India 500)'),
    ('Wipro', r'\b(wipro|wipro enterprise)\b', True, True, 'IT Services & Consulting (Fortune India 500)'),
    ('Capgemini', r'\bcapgemini\b', True, True, 'IT Services & Engineering (Fortune Global 500)'),
    ('Cognizant', r'\bcognizant\b', True, True, 'Digital Transformation & IT Services (Fortune 500)'),
    ('HCLTech', r'\b(hcltech|hcl technologies|hcl)\b', True, True, 'IT Services (Fortune India 500)'),
    ('Tech Mahindra', r'\btech mahindra\b', True, True, 'IT & Telecom Services (Fortune India 500)'),
    ('LTIMindtree / L&T', r'\b(ltimindtree|l&t|larsen & toubro|larsen and toubro)\b', True, True, 'Engineering & Tech Services (Fortune India 500)'),
    ('DXC Technology', r'\b(dxc technology|dxc)\b', True, True, 'IT Services (Fortune 500)'),
    ('Genpact', r'\bgenpact\b', False, True, 'Digital Operations & Analytics (Global MNC)'),
    ('WNS Global Services', r'\bwns\b', False, True, 'BPM & Business Analytics (Global MNC)'),
    ('Concentrix', r'\bconcentrix\b', True, True, 'Customer Experience & Tech (Fortune 500)'),
    ('GlobalLogic', r'\bgloballogic\b', False, True, 'Digital Product Engineering (Hitachi Group Global MNC)'),

    # Global Investment Banking & Financial Services
    ('Goldman Sachs', r'\b(goldman sachs|goldman)\b', True, True, 'Investment Banking & Asset Management (Fortune 500)'),
    ('JPMorganChase', r'(jpmorgan|jp\s*morgan|j\.p\.\s*morgan|jpmc|\bchase\b)', True, True, 'Investment Banking & Financial Services (Fortune 500)'),
    ('Morgan Stanley', r'\bmorgan stanley\b', True, True, 'Investment Banking & Wealth Management (Fortune 500)'),
    ('Citigroup / Citi', r'\b(citigroup|citibank|citi)\b', True, True, 'Global Banking & Financial Services (Fortune 500)'),
    ('Bank of America', r'\b(bank of america|bofa|merrill lynch)\b', True, True, 'Banking & Financial Services (Fortune 500)'),
    ('Wells Fargo', r'\bwells fargo\b', True, True, 'Banking & Financial Services (Fortune 500)'),
    ('Deutsche Bank', r'\bdeutsche bank\b', True, True, 'Investment Banking & Corporate Finance (Fortune Global 500)'),
    ('HSBC', r'\bhsbc\b', True, True, 'Global Banking & Markets (Fortune Global 500)'),
    ('Barclays', r'\bbarclays\b', True, True, 'Global Banking & Financial Services (Global MNC)'),
    ('Standard Chartered Bank', r'\bstandard chartered\b', False, True, 'International Banking & Trade Finance (Global MNC)'),
    ('Commonwealth Bank of Australia', r'\b(commonwealth bank|cba)\b', True, True, 'Global Banking (Fortune Global 500)'),
    ('UBS / Credit Suisse', r'\b(ubs|credit suisse)\b', True, True, 'Wealth Management & IB (Fortune Global 500)'),
    ('BNP Paribas', r'\bbnp paribas\b', True, True, 'Banking & Financial Services (Fortune Global 500)'),
    ('State Street', r'\bstate street\b', True, True, 'Institutional Custody & Asset Management (Fortune 500)'),
    ('BNY Mellon', r'\b(bny mellon|bank of new york mellon)\b', True, True, 'Custody & Investment Services (Fortune 500)'),
    ('American Express', r'\b(american express|amex)\b', True, True, 'Payments & Travel Services (Fortune 500)'),
    ('Mastercard', r'\bmastercard\b', True, True, 'Payment Technology & Processing (Fortune 500)'),
    ('Visa', r'\bvisa\b', True, True, 'Payment Network & FinTech (Fortune 500)'),
    ('Fidelity Investments', r'\bfidelity\b', True, True, 'Asset Management & FinTech (Fortune 500)'),
    ('ICICI Bank', r'\bicici bank|icici\b', True, True, 'Banking & Financial Services (Fortune India 500)'),
    ('HDFC Bank', r'\b(hdfc bank|hdfc)\b', True, True, 'Banking & Financial Services (Fortune Global 500)'),
    ('State Bank of India (SBI)', r'\b(state bank of india|sbi)\b', True, True, 'Banking & Financial Services (Fortune Global 500)'),
    ('Axis Bank', r'\baxis bank\b', True, True, 'Banking & Financial Services (Fortune India 500)'),
    ('Kotak Mahindra Bank', r'\b(kotak mahindra|kotak bank)\b', True, True, 'Banking & Financial Services (Fortune India 500)'),

    # Global Retail, FMCG & Consumer Giants
    ('Walmart / Flipkart', r'\b(walmart|flipkart)\b', True, True, 'Retail & E-Commerce (#1 Fortune 500)'),
    ('Target', r'\btarget\b', True, True, 'Retail & Merchandising (Fortune 500)'),
    ('Procter & Gamble (P&G)', r'\b(procter & gamble|p&g)\b', True, True, 'Consumer Goods / FMCG (Fortune 500)'),
    ('Unilever / HUL', r'\b(unilever|hindustan unilever|hul)\b', True, True, 'Consumer Goods / FMCG (Fortune Global 500)'),
    ('Nestle', r'\b(nestle|nestlé)\b', True, True, 'Food & Beverage FMCG (Fortune Global 500)'),
    ('PepsiCo', r'\bpepsico\b', True, True, 'Food & Beverage FMCG (Fortune 500)'),
    ('Coca-Cola', r'\b(coca-cola|coca cola|hccb)\b', True, True, 'Beverages & Distribution (Fortune 500)'),
    ('ITC Limited', r'\b(itc limited|itc ltd|itc)\b', True, True, 'FMCG, Paper & Agri-Business (Fortune India 500)'),
    ('Johnson & Johnson', r'\b(johnson & johnson|j&j)\b', True, True, 'Healthcare & Consumer Products (Fortune 500)'),
    ('Mondelez International', r'\b(mondelez|cadbury)\b', True, True, 'Snacks & Confectionery (Fortune 500)'),
    ('Colgate-Palmolive', r'\bcolgate\b', True, True, 'Consumer Products (Fortune 500)'),
    ('Puma Global & India', r'\bpuma\b', False, True, 'Global Sportswear & Footwear (Global MNC)'),
    ('Nike', r'\bnike\b', True, True, 'Sportswear & Footwear (Fortune 500)'),
    ('Adidas', r'\badidas\b', False, True, 'Sportswear & Footwear (Global MNC)'),

    # Industrial, Automotive, Aerospace & Engineering
    ('Boeing', r'\bboeing\b', True, True, 'Aerospace & Defense (Fortune 500)'),
    ('Airbus', r'\bairbus\b', True, True, 'Aerospace & Defense (Fortune Global 500)'),
    ('Lockheed Martin', r'\b(lockheed martin|lockheed)\b', True, True, 'Aerospace & Defense (Fortune 500)'),
    ('Siemens', r'\bsiemens\b', True, True, 'Industrial Automation & Energy (Fortune Global 500)'),
    ('Robert Bosch', r'\bbosch\b', True, True, 'Automotive & Industrial Tech (Fortune Global 500)'),
    ('General Electric (GE)', r'\b(ge aerospace|ge healthcare|ge vernova|general electric)\b', True, True, 'Industrial & Aerospace (Fortune 500)'),
    ('Honeywell', r'\bhoneywell\b', True, True, 'Industrial & Aerospace Automation (Fortune 500)'),
    ('Schneider Electric', r'\bschneider electric\b', True, True, 'Energy Management & Automation (Fortune Global 500)'),
    ('ABB', r'\babb\b', True, True, 'Robotics & Electrification (Fortune Global 500)'),
    ('Volvo Group', r'\bvolvo\b', True, True, 'Automotive & Heavy Equipment (Fortune Global 500)'),
    ('Tata Motors', r'\btata motors\b', True, True, 'Automotive & Commercial Vehicles (Fortune India 500)'),
    ('Mahindra Group', r'\bmahindra\b', True, True, 'Automotive, Farm & Aerospace (Fortune India 500)'),
    ('Caterpillar', r'\bcaterpillar\b', True, True, 'Heavy Machinery & Mining (Fortune 500)'),
    ('TE Connectivity', r'\bte connectivity\b', True, True, 'Sensors & Connectors (Fortune 500)'),
    ('Cummins', r'\bcummins\b', True, True, 'Engines & Power Tech (Fortune 500)'),
    ('3M', r'\b3m\b', True, True, 'Industrial & Safety Tech (Fortune 500)'),

    # Healthcare, Pharma & Medical Devices
    ('Pfizer', r'\bpfizer\b', True, True, 'Pharmaceuticals & Biotechnology (Fortune 500)'),
    ('Novartis', r'\bnovartis\b', True, True, 'Healthcare & Pharmaceuticals (Fortune Global 500)'),
    ('AstraZeneca', r'\bastrazeneca\b', True, True, 'Pharmaceuticals (Global MNC)'),
    ('Abbott Laboratories', r'\babbott\b', True, True, 'Medical Devices & Healthcare (Fortune 500)'),
    ('Medtronic', r'\bmedtronic\b', True, True, 'Medical Technology (Fortune 500)'),
    ('Sanofi', r'\bsanofi\b', True, True, 'Pharmaceuticals (Fortune Global 500)'),
    ('GSK (GlaxoSmithKline)', r'\b(gsk|glaxosmithkline)\b', True, True, 'Pharmaceuticals (Global MNC)'),
    ('Dr. Reddy Laboratories', r'\b(dr\. reddy|dr reddy)\b', True, True, 'Pharma (Fortune India 500)'),
    ('Cipla', r'\bcipla\b', True, True, 'Pharma & Biotech (Fortune India 500)'),
    ('Biocon', r'\bbiocon\b', False, True, 'Biopharma (Global MNC)'),

    # Telecom, Media & Hospitality
    ('Bharti Airtel', r'\b(airtel|bharti airtel)\b', True, True, 'Telecommunications (Fortune India 500)'),
    ('Reliance Industries / Jio', r'\b(reliance|jio)\b', True, True, 'Energy, Retail & Telecom (Fortune Global 500)'),
    ('Tata Communications', r'\btata communications\b', True, True, 'Digital Ecosystem / Telecom (Tata Group / Global MNC)'),
    ('Vodafone / Vi', r'\bvodafone\b', True, True, 'Telecommunications (Fortune Global 500)'),
    ('AT&T', r'\bat&t\b', True, True, 'Telecommunications (Fortune 500)'),
    ('Verizon', r'\bverizon\b', True, True, 'Telecommunications (Fortune 500)'),
    ('Thomson Reuters', r'\bthomson reuters\b', False, True, 'Information & Media (Global MNC)'),
    ('Hilton Worldwide', r'\b(hilton|conrad)\b', True, True, 'Hospitality & Luxury Hotels (Fortune 500)'),
    ('Marriott International', r'\b(marriott|jw marriott|ritz-carlton)\b', True, True, 'Hospitality (Fortune 500)'),
    ('Hyatt Hotels', r'\bhyatt\b', True, True, 'Hospitality (Fortune 500)'),
    ('IHG (InterContinental)', r'\b(ihg|intercontinental)\b', False, True, 'Hospitality (Global MNC)')
]

matched_connections = defaultdict(list)
f500_connections = set()
mnc_connections = set()

for c_idx, c in enumerate(connections):
    raw_co = (c.get('Company') or '').strip().lower()
    if not raw_co:
        continue
    
    fn = (c.get('First Name') or '').strip()
    ln = (c.get('Last Name') or '').strip()
    pos = (c.get('Position') or '').strip()
    full_info = (f'{fn} {ln}', pos, c.get('Company', ''))

    for canon, pat, is_f500, is_mnc, sector in f500_mnc_defs:
        if re.search(pat, raw_co):
            matched_connections[canon].append(full_info)
            if is_f500:
                f500_connections.add(c_idx)
            if is_mnc:
                mnc_connections.add(c_idx)
            break

print(f"TOTAL_CONNECTIONS: {len(connections):,}")
print(f"TOTAL_F500_CONNECTIONS: {len(f500_connections):,}")
print(f"TOTAL_MNC_CONNECTIONS: {len(mnc_connections):,}")
print(f"TOTAL_DISTINCT_F500_MNC_COMPANIES: {len(matched_connections)}")

# Sector Aggregations
sector_counts = defaultdict(int)
for canon, conns in matched_connections.items():
    meta = [d for d in f500_mnc_defs if d[0] == canon][0]
    sector = meta[4]
    sector_counts[sector] += len(conns)

print("\n=== TOP EMPLOYERS IN YOUR NETWORK (CONNECTIONS COUNT) ===")
for canon, conns in sorted(matched_connections.items(), key=lambda x: len(x[1]), reverse=True)[:45]:
    meta = [d for d in f500_mnc_defs if d[0] == canon][0]
    badge = "Fortune 500" if meta[2] else "Global MNC"
    print(f"• {canon:36s} : {len(conns):3d} contacts [{badge}]")
