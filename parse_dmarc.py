import sys
import pandas as pd
import xml.etree.ElementTree as ET


def parse_dmarc(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    records = []
    for record in root.findall('.//record'):
        ip = record.findtext('row/source_ip')
        count = record.findtext('row/count')
        policy = record.find('row/policy_evaluated')
        disposition = policy.findtext('disposition') if policy is not None else None
        dkim = policy.findtext('dkim') if policy is not None else None
        spf = policy.findtext('spf') if policy is not None else None
        domain = record.findtext('identifiers/header_from')
        records.append({
            'source_ip': ip,
            'count': count,
            'disposition': disposition,
            'dkim': dkim,
            'spf': spf,
            'domain': domain
        })
    return pd.DataFrame(records)


def main(xml_path):
    df = parse_dmarc(xml_path)
    base = xml_path.rsplit('.', 1)[0]
    html_path = f"{base}.html"
    xlsx_path = f"{base}.xlsx"
    df.to_html(html_path, index=False)
    df.to_excel(xlsx_path, index=False)
    print(f"Generated {html_path} and {xlsx_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parse_dmarc.py <report.xml>')
        sys.exit(1)
    main(sys.argv[1])
