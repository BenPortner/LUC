import brightway2 as bw
from Helpers import *

bw.projects.set_current("ecoinvent-import")

def remove_no_amount(db):
    for ds in db:
        ds["exchanges"] = [exc for exc in ds["exchanges"] if exc.get("amount")]
    return db

def normalize_amounts(db):
    for ds in db:
        dProduct = [exc for exc in ds.get("exchanges",[]) if exc.get("type") == "production"][0]
        if dProduct.get("amount") > 1:
            scale = dProduct.get("amount")
            for i,exc in enumerate(ds.get("exchanges",[])):
                exc["amount"] = exc["amount"]/scale
    return db

def biosphere_location_to_category(db):
    for ds in db:
        ldBiosphere = [exc for exc in ds.get("exchanges",[]) if exc.get("type") == "biosphere"]
        for exc in ldBiosphere:
            exc["categories"] = exc["location"]
            if "(" in exc["categories"]:
                exc["categories"] = "::".join(eval(exc["categories"]))
            else:
                exc["categories"] = exc["categories"].replace(":","::")
            exc["location"] = ""
    return db


# import custom datasets
sFile = "PV_land_use_change_db.xlsx"
db = bw.ExcelImporter(sFile)
db.apply_strategy(remove_no_amount)
db.apply_strategy(normalize_amounts)
db.apply_strategy(biosphere_location_to_category)
db.apply_strategies()
db.match_database(fields=["name","location","unit"])
db.match_database("ecoinvent 3.5 APOS", fields=["name","location","unit"])
db.match_database("biosphere3", fields=["name","categories","unit"])

# check again in excel
#db.write_excel()
#bw2io.export.DatabaseToGEXF("P2G foreground localized").export()

db.write_database()

pass