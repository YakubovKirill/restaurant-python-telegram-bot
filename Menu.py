class Menu:
    def __init__(self):
        self.current_menu_level = 0
        self.current_category = ''
    
    def getLevel(self):
        return self.current_menu_level
    
    def getCategory(self):
        return self.current_category

    def incLevel(self):
        self.current_menu_level += 1
    
    def decLevel(self):
        if self.current_menu_level > 0:
            self.current_menu_level -= 1
    
    def setCategory(self, category):
        self.current_category = category
    
    def clear(self):
        self.current_menu_level = 0
        self.current_category = ''