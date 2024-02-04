import json


def convert_to_days(time, metric):
    if metric == 'Days':
        return time
    elif metric == 'Weeks':
        return time * 7
    elif metric == 'Months':
        return time * 30  # Approximation
    elif metric == 'Hours':
        return time / 24
    else:
        return None  # For unsupported metrics

def get_min_fridge_expiration_time_in_days(product_name, name_subtitle=None, file_path="./FoodData.json"):
    # Load the JSON data
    with open(file_path) as file:
        data = json.load(file)

    # Search for the product
    for product in data['sheets'][2]['data']:
        name = product[2].get('Name')
        subtitle = product[3].get('Name_subtitle')
        if name == product_name:
            #print(name + " " + subtitle)
            pass
        if name == product_name and (subtitle == name_subtitle or subtitle == None):
            min_time = product[20].get('DOP_Refrigerate_Min')
            metric = product[22].get('DOP_Refrigerate_Metric')
            return convert_to_days(min_time, metric)
    
    return None



