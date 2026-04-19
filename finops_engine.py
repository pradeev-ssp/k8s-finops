import requests
import os
import requests
import datetime

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090/api/v1/query")
COST_PER_CORE_MONTH = 40.00 # Dummy local cost for the sake of the report

def get_prometheus_data(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    return response.json()['data']['result']

def generate_report():
    print("🌍 Aggregating Metrics: Actual vs Requested...")
    
    # 1. DATA COLLECTION
    # (Note: In production, change [5m] to [7d] for the 7-day average)
    actual_query = 'sum by (pod) (rate(container_cpu_usage_seconds_total{namespace="default", container!="POD", container!=""}[5m]))'
    requested_query = 'sum by (pod) (kube_pod_container_resource_requests{namespace="default", resource="cpu"})'
    
    actual_data = get_prometheus_data(actual_query)
    requested_data = get_prometheus_data(requested_query)
    
    # Create a dictionary to easily match Actual to Requested by Pod Name
    pods_usage = {item['metric']['pod']: float(item['value'][1]) for item in actual_data}
    pods_requests = {item['metric']['pod']: float(item['value'][1]) for item in requested_data}

    # 2. ANALYSIS
    html_rows = ""
    total_wasted_money = 0
    
    for pod_name, requested_cpu in pods_requests.items():
        actual_cpu = pods_usage.get(pod_name, 0)
        waste_cores = requested_cpu - actual_cpu
        waste_percent = (waste_cores / requested_cpu) * 100 if requested_cpu > 0 else 0
        
        # Only flag if waste is > 50%
        if waste_percent > 50.0:
            wasted_dollars = waste_cores * COST_PER_CORE_MONTH
            total_wasted_money += wasted_dollars
            
            # 3. REPORTING (HTML Generation)
            html_rows += f"""
            <tr style="background-color: #ffebee;">
                <td>{pod_name}</td>
                <td>{requested_cpu:.2f} Cores</td>
                <td>{actual_cpu:.4f} Cores</td>
                <td style="color: red; font-weight: bold;">{waste_percent:.1f}%</td>
                <td>Reduce YAML request to: {(actual_cpu * 1.2):.2f} (Includes 20% safety buffer)</td>
            </tr>
            """

    # Generate the final HTML file
    html_template = f"""
    <html>
        <head>
            <title>Weekly K8s FinOps Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f4f4f4; }}
                .summary {{ font-size: 1.2em; margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Kubernetes FinOps Audit Report</h1>
            <p>Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="summary">
                <strong>🚨 Total Monthly Waste Identified:</strong> ${total_wasted_money:.2f}
            </div>

            <h2>High Priority: Deployments > 50% Waste</h2>
            <table>
                <tr>
                    <th>Pod Name</th>
                    <th>Requested CPU</th>
                    <th>Actual CPU (Peak)</th>
                    <th>Waste %</th>
                    <th>Developer Recommendation</th>
                </tr>
                {html_rows}
            </table>
        </body>
    </html>
    """
    
    with open("finops_report.html", "w") as file:
        file.write(html_template)
    print("✅ Success! 'finops_report.html' has been generated.")

if __name__ == "__main__":
    generate_report()