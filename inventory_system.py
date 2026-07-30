import csv
import os
from datetime import datetime


INPUT_FILE = "daily_inventory.csv"
OUTPUT_FILE = "restock_report.csv"
STORE_NAME = "Reliance Smart Bazaar"


SUPPLIER_MAP = {
    "Samsung": "Samsung Distributor",
    "LG": "LG Electronics",
    "Dell": "Dell India",
    "Logitech": "Logitech Supplier",
    "Amul": "Amul Dairy Supplier",
    "Fortune": "Fortune Foods Distributor",
    "HP": "HP India Distributor",
}
DEFAULT_SUPPLIER = "Reliance Vendor"


CRITICAL_RATIO = 0.5

RESTOCK_TARGET_MULTIPLIER = 2.0




def create_sample_inventory(filename=INPUT_FILE):
    """Creates a demo daily_inventory.csv so the project can be run
    immediately without requiring the user to supply their own data."""
    sample_rows = [
        ["Product Name", "Brand", "Current Quantity", "Reorder Threshold", "Price", ],
        ["Milk 1L", "Amul", "18", "40", "58"],
        ["Cooking Oil 1L", "Fortune", "12", "30", "165"],
        ["Basmati Rice 5kg", "Fortune", "60", "25", "480"],
        ["Laptop - Inspiron", "Dell", "3", "10", "45000"],
        ["Printer Ink Cartridge", "HP", "5", "20", "1200"],
        ["LED TV 43inch", "LG", "8", "15", "28000"],
        ["SSD 512GB", "Samsung", "2", "12", "3500"],
        ["Wireless Mouse", "Logitech", "40", "20", "699"],
        ["Refrigerator 300L", "LG", "6", "8", "32000"],
        ["Bread Loaf", "", "22", "35", "45"],
        ["Notebook Pack", "", "150", "50", "120"],
        ["Toothpaste 200g", "", "", "40", "89"],       
        ["", "Samsung", "10", "5", "999"],             
        ["Face Wash 100ml", "", "9", "abc", "199"],     
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_rows)
    print(f"[Setup] No '{filename}' found, so a sample inventory file was created.\n")


def read_inventory(filename=INPUT_FILE):
    """Reads the CSV file and returns a list of clean, validated
    product dictionaries. Bad rows are skipped (with a warning)
    instead of crashing the program."""
    records = []
    skipped = 0

    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_number, row in enumerate(reader, start=2):  # row 1 = header
                try:
                    name = row["Product Name"].strip()
                    brand = row.get("Brand", "").strip()
                    qty = row["Current Quantity"].strip()
                    threshold = row["Reorder Threshold"].strip()
                    price = row["Price"].strip()

                    if not name:
                        raise ValueError("missing product name")
                    if not qty or not threshold or not price:
                        raise ValueError("missing numeric value")
                    qty = int(float(qty))
                    threshold = int(float(threshold))
                    price = float(price)

                    if qty < 0 or threshold <= 0 or price < 0:
                        raise ValueError("invalid numeric value")

                    records.append({
                        "name": name,
                        "brand": brand,
                        "qty": qty,
                        "threshold": threshold,
                        "price": price,
                    })

                except (ValueError, KeyError) as e:
                    skipped += 1
                    print(f"[Warning] Skipped row {row_number}: {e}")

    except FileNotFoundError:
        print(f"[Error] Could not find '{filename}'.")
        return []

    print(f"[Info] Loaded {len(records)} valid products "
          f"({skipped} row(s) skipped due to errors).\n")
    return records



#stocking status

def classify_status(qty, threshold):
    """Returns 'Critical', 'Low Stock', or 'Healthy'."""
    if qty <= threshold * CRITICAL_RATIO:
        return "Critical"
    elif qty <= threshold:
        return "Low Stock"
    else:
        return "Healthy"




def suggested_reorder_qty(qty, threshold):
    """Suggests how many units to order to bring stock back up to
    a healthy target level (2x the threshold, by default)."""
    target_level = threshold * RESTOCK_TARGET_MULTIPLIER
    reorder_qty = max(int(round(target_level - qty)), 0)
    return reorder_qty


def get_supplier(brand):
    return SUPPLIER_MAP.get(brand, DEFAULT_SUPPLIER)

#pp

def analyze_inventory(records):
    """Runs every product through classification, reorder
    calculation, supplier assignment and cost estimation.
    Returns (analyzed_list, summary_dict)."""
    analyzed = []
    counts = {"Healthy": 0, "Low Stock": 0, "Critical": 0}
    total_budget = 0.0

    for item in records:
        status = classify_status(item["qty"], item["threshold"])
        reorder_qty = suggested_reorder_qty(item["qty"], item["threshold"]) \
            if status != "Healthy" else 0
        estimated_cost = round(reorder_qty * item["price"], 2)
        supplier = get_supplier(item["brand"])

        counts[status] += 1
        total_budget += estimated_cost

        analyzed.append({
            **item,
            "status": status,
            "reorder_qty": reorder_qty,
            "estimated_cost": estimated_cost,
            "supplier": supplier,
        })

    total_products = len(records) if records else 1
    health_score = round((counts["Healthy"] / total_products) * 100, 1)

    summary = {
        "total_products": len(records),
        "healthy": counts["Healthy"],
        "low_stock": counts["Low Stock"],
        "critical": counts["Critical"],
        "health_score": health_score,
        "total_budget": round(total_budget, 2),
    }
    return analyzed, summary



#dd dashboard

def print_dashboard(summary, store_name=STORE_NAME):
    status_word = "GOOD" if summary["health_score"] >= 70 else \
                  "NEEDS ATTENTION" if summary["health_score"] >= 40 else "POOR"

    print("=" * 50)
    print("     SMART RETAIL INVENTORY DASHBOARD")
    print(f"          {store_name}")
    print("=" * 50)
    print(f"Date                : {datetime.now().strftime('%d-%b-%Y %I:%M %p')}")
    print(f"Products Scanned    : {summary['total_products']}")
    print(f"Healthy             : {summary['healthy']}")
    print(f"Low Stock           : {summary['low_stock']}")
    print(f"Critical            : {summary['critical']}")
    print(f"Inventory Health    : {summary['health_score']}%  ({status_word})")
    print(f"Estimated Budget    : Rs. {summary['total_budget']:,.2f}")
    print("=" * 50 + "\n")




def generate_email_alert(analyzed, summary, store_name=STORE_NAME):
    
    needs_action = [p for p in analyzed if p["status"] in ("Critical", "Low Stock")]
    critical_products = [p for p in analyzed if p["status"] == "Critical"]
    low_stock_products = [p for p in analyzed if p["status"] == "Low Stock"]

    lines = []
    lines.append("Subject: Daily Inventory Alert - " + store_name)
    lines.append("")
    lines.append("Dear Admin / Store Manager,")
    lines.append("")
    lines.append(
        f"Today's inventory scan has identified {len(needs_action)} "
        f"product(s) that require restocking."
    )
    lines.append("")

    if critical_products:
        lines.append("CRITICAL - Restock Immediately:")
        for p in critical_products:
            lines.append(
                f"  - {p['name']}: {p['qty']} left / threshold {p['threshold']} "
                f"-> order {p['reorder_qty']} units from {p['supplier']} "
                f"(Rs. {p['estimated_cost']:,.2f})"
            )
        lines.append("")

    if low_stock_products:
        lines.append("LOW STOCK - Restock Soon:")
        for p in low_stock_products:
            lines.append(
                f"  - {p['name']}: {p['qty']} left / threshold {p['threshold']} "
                f"-> order {p['reorder_qty']} units from {p['supplier']} "
                f"(Rs. {p['estimated_cost']:,.2f})"
            )
        lines.append("")

    if not needs_action:
        lines.append("No products need restocking today. Inventory is healthy.")
        lines.append("")

    lines.append(f"Estimated Procurement Budget: Rs. {summary['total_budget']:,.2f}")
    lines.append("")
    lines.append("Kindly initiate the purchase process for the above items.")
    lines.append("")
    lines.append("Regards,")
    lines.append("Inventory Automation System")

    return "\n".join(lines)

 #export csv 

def export_report(analyzed, filename=OUTPUT_FILE):
    fieldnames = [
        "Product Name", "Current Quantity", "Threshold", "Priority",
        "Suggested Reorder", "Supplier", "Estimated Cost",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in analyzed:
            writer.writerow({
                "Product Name": p["name"],
                "Current Quantity": p["qty"],
                "Threshold": p["threshold"],
                "Priority": p["status"],
                "Suggested Reorder": p["reorder_qty"],
                "Supplier": p["supplier"],
                "Estimated Cost": p["estimated_cost"],
            })
    print(f"[Info] Restock report saved to '{filename}'.\n")


#main

def main():
    if not os.path.exists(INPUT_FILE):
        create_sample_inventory()

    records = read_inventory()
    if not records:
        print("[Error] No valid inventory data to analyze. Exiting.")
        return

    analyzed, summary = analyze_inventory(records)
    print_dashboard(summary)

    alert = generate_email_alert(analyzed, summary)
    print(alert)
    print()

    export_report(analyzed)


if __name__ == "__main__":
    main()
