import math
import pandas as pd

def quantity_to_log_cat(quantity):
    if check_nan(quantity):
        return 0
    else:
        if quantity <= 1:
            return 1
        else:
            return math.ceil(math.log(quantity)) + 1

def fiscal_year_to_cat(year):
    if year == '2012-2013':
        return 0
    elif year == '2013-2014':
        return 1
    elif year == '2014-2015':
        return 2
    else:
        raise NotImplemented

def get_date_to_month_buckets(base):
    def date_to_month_buckets(date):
        if type(date) == str:
            print(date)
        if check_nan(date):
            return 0
        try:
            days = (date-base).days
        except:
            print(date, base)
            raise Exception
        months = round(days/30)
        if months < 0:
            return 1
        if months > 72:
            return 74
        return months + 2
    return date_to_month_buckets

def price_to_log_cat(price):
    if check_nan(price):
        return 0
    else:
        price = float(price.replace('$',''))
        if price <= 0:
            return 1
        elif price <= 1:
            return 2
        else:
            return math.ceil(math.log10(price)) + 2

def price_to_float(price):
    if type(price) == float:
        if math.isnan(price):
            return 0
        else:
            return price
    else:
        return float(price.replace('$',''))

def check_nan(item):
    # return type(item) == float and math.isnan(item)
    return pd.isnull(item)

def add_desc(desc, entry, key):
    if check_nan(entry[key]):
        return desc + f'There is no {key}. '
    else:
        return desc + f'The {key} is {entry[key]}. '

def entry_to_desc(entry):
    if check_nan(entry['Creation Date']):
        desc = 'A record of a large purchase by the State of CA created on an unkown date. '
    else:
        desc = f'A record of a large purchase by the State of CA created on {entry["Creation Date"]}. '
    if check_nan(entry['Purchase Date']):
        desc += 'The purchase date is unknown. '
    else:
        desc += f'The purhcase date is {entry["Purchase Date"]}. '
    if check_nan(entry['Fiscal Year']):
        desc += 'The record fiscal year is unknown. '
    else:
        desc += f'The record fiscal year is {entry["Fiscal Year"]}. '
    if check_nan(entry['Item Name']):
        desc += 'The purchase is for an unknown item '
    else:
        desc += f'The purchase was for {entry["Item Name"]} '
    if check_nan(entry['Item Description']):
        desc += 'with unknown description. '
    else:
        desc += f'with the description: {entry["Item Description"]}. '
    if check_nan(entry['Quantity']):
        desc += 'The quantity and price of the purchase is unknown. '
    else:
        desc += f'The purchase is for {entry["Quantity"]} items with unit price of {entry["Unit Price"]} for a total of {entry["Total Price"]}. '
    if check_nan(entry['LPA Number']):
        desc += 'There is no Leveraged Procuement Agreement Number, aka Contract Number. '
    else:
        desc += f'The purchase is contract spend with a Leveraged Procuement Agreement Number, aka Contract Number: {entry["LPA Number"]}. '
    keys = ['Purchase Order Number', 'Requisition Number', 'Acquisition Type', 'Sub-Acquisition Type', 'Acquisition Method', 'Sub-Acquisition Method', 'Department Name', 'Supplier Code', 'Supplier Name', 'Supplier Qualifications', 'Supplier Zip Code', 'CalCard', 'Classification Codes', 'Normalized UNSPSC', 'Commodity Title', 'Class', 'Class Title', 'Family', 'Family Title', 'Segment', 'Segment Title']
    for key in keys:
        desc = add_desc(desc, entry, key)
    if check_nan(entry['Location']):
        desc += 'The purchase location is unknown.'
    else:
        try:
            zipcode, coord = entry['Location'].split('\n')
            desc += f'The purchase zipcode is {zipcode} and longitude and latitude is {coord}.'
        except:
            desc += f'The purchase zipcode is {entry["location"]}, which may not be abroad.'
    return desc