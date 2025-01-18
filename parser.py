# parses given arguments

class Parser():
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
       
        if self.command == "add":
            self._parse_add_command(args[2:]) 
        elif self.command == "meal":
            self._parse_meal_command(args[2:])
        elif self.command == "list":
            self._parse_list_command(args)
        
    def parse_add_barcode(self, barcode_index=3):
        # action = -b
        barcode = self.args[barcode_index]
        is_servings = True 
        
        unit_flag = self.args[barcode_index]
        if unit_flag == "-s":
           pass
        elif unit_flag == "-u":
            is_servings = False
        else:
            raise Exception(f"{self.args[4]}: is not understood as indicating servings or units.")
        
        count = float(self.args[5])

        return barcode, is_servings, count 

    def parse_add_manual(self):
        return [float(self.args[3]), float(self.args[4]), float(self.args[5]), float(self.args[6])]

    def parse_add_meal(self):
        meal_name = self.action

        try:
            count = float(self.args[3])
            return meal_name, count
        except IndexError:
            return meal_name, int(1)

    def parse_meal_create(self):
        FLAGS = ["-b", "-m", "-meal"]
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
                flags.append(i+1)

        for flag, index_after in flags:
            if flag == "-b":
                barcodes.append(self.parse_add_barcode(barcode_index=index_after))

            if flag == "-m":
                manual = [self.args[index_after],
                                self.args[index_after+1],
                                self.args[index_after+2],
                                self.args[index_after+3],
                                self.args[index_after+4]]

                manual = [float(i) for i in manual]
                manuals.append(manual)

            elif flag == "-meal":
                meals.append([self.args[index_after], float(self.args[index_after+1])])

    def parse_meal_remove(self):
        None

    def parse_list(self):
        None
