#!/usr/bin/env python3
import argparse, os, json, requests

API_VERSION = "2024-04"

def round_to_tidy(price: float) -> str:
    price_int = int(round(price))
    rem = price_int % 100
    base = price_int - rem
    opts = [base, base + 90, base + 100]
    tidy = min(opts, key=lambda x: abs(price_int - x))
    return f"{tidy:.2f}"

def fetch_all_variants(session, base_url):
    variants, page_info = [], None
    while True:
        params = {"limit": 250}
        if page_info: params["page_info"] = page_info
        resp = session.get(f"{base_url}/products.json", params=params)
        resp.raise_for_status()
        data = resp.json()
        for prod in data["products"]:
            for v in prod["variants"]:
                variants.append({
                    "product_id": prod["id"],
                    "variant_id": v["id"],
                    "original_price": v["price"]
                })
        link = resp.headers.get("Link", "")
        if 'rel="next"' not in link: break
        page_info = link.split("page_info=")[1].split(">")[0]
    return variants

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--token",  required=True)
    p.add_argument("--domain", required=True)
    p.add_argument("--percent", type=float, required=True)
    args = p.parse_args()

    session = requests.Session()
    session.headers.update({
        "X-Shopify-Access-Token": args.token,
        "Content-Type": "application/json"
    })
    base_url = f"https://{args.domain}/admin/api/{API_VERSION}"

    backup_file = os.path.join(os.path.dirname(__file__), "shopify_backup.json")
    if not os.path.exists(backup_file):
        print("🔄 Fetching current variant prices...")
        variants = fetch_all_variants(session, base_url)
        with open(backup_file, "w", encoding="utf-8") as bf:
            json.dump(variants, bf, indent=2)
        print(f"✔️  Backup saved to {backup_file}")
    else:
        variants = json.load(open(backup_file, "r", encoding="utf-8"))

    for v in variants:
        base = float(v["original_price"])
        newp = base * (1 + args.percent/100.0)
        tidy = round_to_tidy(newp)
        url = f"{base_url}/variants/{v['variant_id']}.json"
        payload = {"variant": {"id": v["variant_id"], "price": tidy}}
        resp = session.put(url, json=payload)
        if resp.ok:
            print(f"✅  {v['variant_id']} → {tidy}")
        else:
            print(f"❌  {v['variant_id']} failed: {resp.text}")

    print("🎉 Finished updating!")
if __name__=="__main__":
    main()
