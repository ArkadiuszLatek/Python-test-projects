# Importing the required libraries
import xml.etree.ElementTree as ET
import pandas as pd


namespace = '{http://base.google.com/ns/1.0}'


cols = ["id", "title", "image_link", "condition", "price", "sale_price", "gtin", "brand", "mpn", "item_group_id", "custom_label_0",
        "custom_label_2", "applink", "description", "android_app_name", "mobile_link"]
rows = []

# Parsing the XML file
tree = ET.parse('org.xml')
root = tree.getroot()
for channel in root.iter('channel'):
    for i in channel.iter('item'):
        try:
            id = i.find('{}id'.format(namespace)).text
            title = i.find('{}title'.format(namespace)).text
            image_link = i.find('{}image_link'.format(namespace)).text
            condition = i.find('{}condition'.format(namespace)).text
            availability = i.find('{}availability'.format(namespace)).text
            price = i.find('{}price'.format(namespace)).text
            sale_price = i.find('{}sale_price'.format(namespace)).text
            gtin = i.find('{}gtin'.format(namespace)).text
            brand = i.find('{}brand'.format(namespace)).text
            mpn = i.find('{}mpn'.format(namespace)).text
            item_group_id = i.find('{}item_group_id'.format(namespace)).text
            custom_label_0 = i.find('{}custom_label_0'.format(namespace)).text
            custom_label_2 = i.find('{}custom_label_2'.format(namespace)).text
            applink = i.find('applink').text
            description = i.find('{}description'.format(namespace)).text
            android_app_name = i.find('android_app_name').text
            android_app_package = i.find('android_app_package').text
            mobile_link = i.find("mobile_link").text

            rows.append({"id": id,
                         "title": title,
                         "image_link": image_link,
                         "condition": condition,
                         "price": price,
                         "sale_price": sale_price,
                         "gtin": gtin,
                         "brand": brand,
                         "mpn": mpn,
                         "item_group_id": item_group_id,
                         "custom_label_0": custom_label_0,
                         "custom_label_2": custom_label_2,
                         "applink": applink,
                         "description": description,
                         "android_app_name": android_app_name,
                         "android_app_package": android_app_package,
                         "mobile_link": mobile_link
                         })
        except(AttributeError):
            pass

df = pd.DataFrame(rows, columns=cols)

# Writing dataframe to csv
df.to_csv('output.csv')
