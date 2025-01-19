# parses given arguments

class Parser():
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    args: list[str]
    command: str
    action: str
    arg_count: int

    def __init__(self, args: list[str]):
        self.args = args
        self.arg_count = len(args)
        
        # set command and action to first two arguments respectively
        # if they exist.  otherwise set to the falsy empty string
        try:
            self.command = args[1]
            try:
                self.action = args[2]
            except IndexError:
                self.action = ""
        except IndexError:
            self.command = "" 
    
    # rename barcode_index to index_after_barcode
    def parse_add_barcode(self, barcode_index=3):
        # action = -b
        barcode = self.args[barcode_index]
        is_servings = True 
        
        unit_flag = self.args[barcode_index+1]
        if unit_flag == "-s":
           is_servings = True
        elif unit_flag == "-u":
            is_servings = False
        else:
            raise Exception(f"{unit_flag}: is not understood as indicating servings or units.")
        
        count = float(self.args[barcode_index+2])
        return barcode, is_servings, count 

    def parse_add_manual(self, index_after_flag=2):
        values = [float(self.args[index_after_flag]),
                float(self.args[index_after_flag+1]),
                float(self.args[index_after_flag+2]),
                float(self.args[index_after_flag+3])]

        return dict(zip(self.MACROS, values))

    def parse_add_meal(self): 
        meal_name = self.args[3]

        # check if -s or -u were passed.  If so return whether we want to calculate using
        # servings or units.  Return None if neither of those flags were passed, and assume
        # a count representing the amount of the meal that needs tracked was passed instead.
        try:
            if self.args[4] == "-s":
                count = float(self.args[5])
                is_servings = True
                return meal_name, count, is_servings
            elif self.args[4] == "-u":
                count = float(self.args[5])
                is_servings = False
                return meal_name, count, is_servings 
            else:
                count = float(self.args[4])
                return meal_name, count, None
        except IndexError:
            return meal_name, int(1), None

    def parse_meal_create(self):
        FLAGS = ["-b", "-p", "-m"]
        name = self.args[3]

        barcodes = []
        manuals = []
        meals = []
        
        # list of tuples that contain (flag, first index after the flag in self.args) 
        flags = []
        for i in range(0, self.arg_count):
            if self.args[i] in FLAGS:
                # append the flag and the index after it
                flags.append((self.args[i], i+1))
                
        for flag, index_after in flags:
            if flag == "-b":
                barcodes.append(self.parse_add_barcode(barcode_index=index_after))

            if flag == "-p":
                manuals.append(self._parse_create_meal_manual(index_after_flag=index_after))

            elif flag == "-m":
                meals.append([self.args[index_after], float(self.args[index_after+1])])

        return name, barcodes, manuals, meals

    def parse_meal_remove(self):
        # return the name of the meal to remove
        return self.args[3]

    def _parse_create_meal_manual(self, index_after_flag):
        return [str(self.args[index_after_flag]),
                float(self.args[index_after_flag+1]),
                float(self.args[index_after_flag+2]),
                float(self.args[index_after_flag+3]),
                float(self.args[index_after_flag+4]),
                float(self.args[index_after_flag+5])]

