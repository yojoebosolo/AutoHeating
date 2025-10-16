import datetime
import requests
import os


POSTCODE = os.getenv("POSTCODE")
BASE = "https://api.octopus.energy/v1"


def get_region_letter(postcode: str) -> str:  # outputs the letter for your region ("D")
    r = requests.get(f"{BASE}/industry/grid-supply-points/", params={"postcode": postcode})
    r.raise_for_status()
    return r.json()["results"][0]["group_id"].lstrip("_")


def get_current_agile_product_code() -> str:  # gets the correct product code for the Agile tariff
    r = requests.get(f"{BASE}/products/")
    r.raise_for_status()
    prods = r.json()["results"]
    agile = [p for p in prods
             if p["code"].startswith("AGILE")
             and p.get("direction") == "IMPORT"
             and p.get("available_to") is None]
    if not agile:
        raise RuntimeError("No active AGILE product found")
    agile.sort(key=lambda p: p.get("available_from") or "", reverse=True)
    return agile[0]["code"]


def get_rates(product_code: str, region_letter: str, start_iso: str, end_iso: str):  # outputs the rates for a given period
    tariff_code = f"E-1R-{product_code}-{region_letter}"
    url = f"{BASE}/products/{product_code}/electricity-tariffs/{tariff_code}/standard-unit-rates/"
    r = requests.get(url, params={"period_from": start_iso, "period_to": end_iso, "page_size": 2500})
    r.raise_for_status()
    return r.json()["results"]


def iso_utc(dtobj: datetime.datetime) -> str:  # outputs a readable date format
    if dtobj.tzinfo is None:
        dtobj = dtobj.replace(tzinfo=datetime.UTC)
    return dtobj.isoformat().replace("+00:00", "Z")


def get_current_rate():  # simplified version to just get current rate (no upcoming rates)
    start = datetime.datetime.now(datetime.UTC)
    end = start + datetime.timedelta(hours=3)

    region = get_region_letter(POSTCODE)
    product = get_current_agile_product_code()
    rows = get_rates(product, region, iso_utc(start), iso_utc(end))
    rows.sort(key=lambda r: r["valid_from"])

    current_rate = rows[0]["value_inc_vat"]
    start_time = rows[0]["valid_from"]
    end_time = rows[0]["valid_to"]

    return current_rate, start_time, end_time


def display_rates():  # useful for viewing upcoming rates
    start = datetime.datetime.now(datetime.UTC)
    end = start + datetime.timedelta(hours=6)

    region = get_region_letter(POSTCODE)
    product = get_current_agile_product_code()
    rows = get_rates(product, region, iso_utc(start), iso_utc(end))
    rows.sort(key=lambda r: r["valid_from"])

    print(f"Agile product: {product} | Region: {region} | Window: {iso_utc(start)} → {iso_utc(end)}")
    for x in rows:
        print(f'{x["valid_from"]} → {x["valid_to"]}: {x["value_inc_vat"]} p/kWh')


if __name__ == "__main__":
    display_rates()
    print("Currently:", get_current_rate())