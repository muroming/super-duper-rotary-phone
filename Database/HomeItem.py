class HomeItem(object):
    def __init__(self, id, item_name, is_on, item_description, item_photo):
        self.id = id
        self.item_name = item_name
        self.is_item_on = is_on == 1
        self.item_description = item_description
        self.item_photo = item_photo
