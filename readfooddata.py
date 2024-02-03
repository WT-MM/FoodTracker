import json

def main():
    print("hmmmm")

class FoodItem:
    def __init__(self, name, name_subtitle=None, keywords=None,
                 pantry_min=None, pantry_max=None, pantry_metric=None, pantry_tips=None,
                 dop_pantry_min=None, dop_pantry_max=None, dop_pantry_metric=None, dop_pantry_tips=None,
                 pantry_after_opening_min=None, pantry_after_opening_max=None, pantry_after_opening_metric=None,
                 refrigerate_min=None, refrigerate_max=None, refrigerate_metric=None, refrigerate_tips=None,
                 dop_refrigerate_min=None, dop_refrigerate_max=None, dop_refrigerate_metric=None, dop_refrigerate_tips=None,
                 refrigerate_after_opening_min=None, refrigerate_after_opening_max=None,
                 refrigerate_after_opening_metric=None, refrigerate_after_thawing_min=None,
                 refrigerate_after_thawing_max=None, refrigerate_after_thawing_metric=None,
                 freeze_min=None, freeze_max=None, freeze_metric=None, freeze_tips=None,
                 dop_freeze_min=None, dop_freeze_max=None, dop_freeze_metric=None, dop_freeze_tips=None,
                 id=None, category_id=None):
        self.name = name
        self.name_subtitle = name_subtitle
        self.keywords = keywords
        self.pantry_min = pantry_min
        self.pantry_max = pantry_max
        self.pantry_metric = pantry_metric
        self.pantry_tips = pantry_tips
        self.dop_pantry_min = dop_pantry_min
        self.dop_pantry_max = dop_pantry_max
        self.dop_pantry_metric = dop_pantry_metric
        self.dop_pantry_tips = dop_pantry_tips
        self.pantry_after_opening_min = pantry_after_opening_min
        self.pantry_after_opening_max = pantry_after_opening_max
        self.pantry_after_opening_metric = pantry_after_opening_metric
        self.refrigerate_min = refrigerate_min
        self.refrigerate_max = refrigerate_max
        self.refrigerate_metric = refrigerate_metric
        self.refrigerate_tips = refrigerate_tips
        self.dop_refrigerate_min = dop_refrigerate_min
        self.dop_refrigerate_max = dop_refrigerate_max
        self.dop_refrigerate_metric = dop_refrigerate_metric
        self.dop_refrigerate_tips = dop_refrigerate_tips
        self.refrigerate_after_opening_min = refrigerate_after_opening_min
        self.refrigerate_after_opening_max = refrigerate_after_opening_max
        self.refrigerate_after_opening_metric = refrigerate_after_opening_metric
        self.refrigerate_after_thawing_min = refrigerate_after_thawing_min
        self.refrigerate_after_thawing_max = refrigerate_after_thawing_max
        self.refrigerate_after_thawing_metric = refrigerate_after_thawing_metric
        self.freeze_min = freeze_min
        self.freeze_max = freeze_max
        self.freeze_metric = freeze_metric
        self.freeze_tips = freeze_tips
        self.dop_freeze_min = dop_freeze_min
        self.dop_freeze_max = dop_freeze_max
        self.dop_freeze_metric = dop_freeze_metric
        self.dop_freeze_tips = dop_freeze_tips
        self.id = id
        self.category_id = category_id
    def name(self):
        print(self.name)
def find_food(food_name, sub_type = None):
    with open('FoodData.json', 'r') as file:
        data = json.load(file)
    for x in data['sheets'][2]['data']:
        if(x[2]['Name'] == food_name and (sub_type == None or x[3]['Name_subtitle'] == sub_type) ):
            if(sub_type == None and x[3]['Name_subtitle'] != None):
                print('Chose subtitle of \"{}\" arbitrarily'.format(x[3]['Name_subtitle']))
                #set_reminder(x[2]['name'], get_time(x[])) 
                #21, 22
                return;
def names_of_everything():
    with open('FoodData.json', 'r') as file:
        data = json.load(file)
    with open('AllNames.txt', 'w') as txt_file:
        for x in data['sheets'][2]['data']:
            if(x[3]['Name_subtitle'] == None):
                txt_file.write('{} \n'.format(x[2]['Name']))
            else:
                txt_file.write('{} - {} \n'.format(x[2]['Name'], x[3]['Name_subtitle']))
def set_reminder(name, time):
    print('I will remind you about {} in {} seconds'.format(name, time))       
    
    #17,18.19

#find_food("Ham")
names_of_everything()