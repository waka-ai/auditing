import sys
import os
import json
import re

def load_json(filename):
    # Always loads from the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_vulnerabilities(filepath, cve_mapping, mitigations):
    findings = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, start=1):
        if re.search(r'password\s*=\s*["\'].*["\']', line, re.I):
            findings.append({
                "file": os.path.basename(filepath),
                "line": idx,
                "severity": "High",
                "vulnerability": "Hardcoded Password",
                "cve": cve_mapping.get("Hardcoded Password", "N/A"),
                "mitigation": mitigations.get("Hardcoded Password", "N/A")
            })
        if 'eval(' in line:
            findings.append({
                "file": os.path.basename(filepath),
                "line": idx,
                "severity": "High",
                "vulnerability": "Use of eval()",
                "cve": cve_mapping.get("Use of eval()", "N/A"),
                "mitigation": mitigations.get("Use of eval()", "N/A")
            })
        if 'import pickle' in line:
            findings.append({
                "file": os.path.basename(filepath),
                "line": idx,
                "severity": "Medium",
                "vulnerability": "Insecure Deserialization (pickle)",
                "cve": cve_mapping.get("Insecure Deserialization (pickle)", "N/A"),
                "mitigation": mitigations.get("Insecure Deserialization (pickle)", "N/A")
            })
    return findings

def generate_html_report(findings):
    html = """
    <html><head>
    <title>Audit Report</title>
    <style>
    body { font-family: Arial; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #aaa; padding: 8px; text-align: left; }
    th { background: #f0f0f0; }
    </style>
    </head><body>
    <h2>Code Audit Report</h2>
    """
    if findings:
        html += "<table><tr><th>File</th><th>Line</th><th>Severity</th><th>Vulnerability</th><th>CVE</th><th>Mitigation</th></tr>"
        for f in findings:
            html += f"<tr><td>{f['file']}</td><td>{f['line']}</td><td>{f['severity']}</td><td>{f['vulnerability']}</td><td>{f['cve']}</td><td>{f['mitigation']}</td></tr>"
        html += "</table>"
    else:
        html += "<p>No vulnerabilities found!</p>"
    html += "</body></html>"
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python code_auditing_tool_with_reporting.py <file-to-audit>")
        sys.exit(1)
    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print("Target file does not exist.")
        sys.exit(1)

    cve_mapping = load_json("vuln_to_cve_mapping.json")
    mitigations = load_json("vuln_mitigations.json")

    findings = detect_vulnerabilities(target_file, cve_mapping, mitigations)
    html_report = generate_html_report(findings)

    # Save report to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, "audit_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"HTML report saved as '{report_path}'.")

if __name__ == "__main__":
    main()