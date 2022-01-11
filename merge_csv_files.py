import csv

shared_field = "id"
all_fields = [shared_field]


def get_offers_csv(feed_name: str, shared_field, fields, prefix="empty_prefix"):
    offers = []
    prefix = feed_name.split('.')[0] + "_" if prefix == "empty_prefix" else prefix
    for field in fields:
        if field != shared_field:
            all_fields.append(prefix+field)
    with open(feed_name, "r") as file:
        csv_reader = csv.DictReader(file, delimiter=",")
        for offer in csv_reader:
            new_offer = {}
            for key in fields:
                if key == shared_field:
                    new_offer.update({key: offer[key]})
                else:
                    new_offer.update({prefix+key: offer[key]})
            offers.append(new_offer)
    return offers


ars_offers = get_offers_csv("ARS.csv", shared_field, ["id", "price", "category", "offer_URL"])
mxn_offers = get_offers_csv("MXN.csv", shared_field, ["id", "price", "category", "offer_URL"])
base_offers = get_offers_csv("base.csv", shared_field, ["id", "title", "price", "category", "offer_URL", "image_URL"], "")

with open("feed.csv", "w") as file:
    csv_writer = csv.DictWriter(file, fieldnames=all_fields)
    csv_writer.writeheader()
    for offer in base_offers:
        full_offer = offer
        id= offer["id"]
        for ars_offer in ars_offers:
            if ars_offer["id"] == id:
                full_offer.update(ars_offer)
        for mxn_offer in mxn_offers:
            if mxn_offer["id"] == id:
                full_offer.update(mxn_offer)
        csv_writer.writerow(offer)

