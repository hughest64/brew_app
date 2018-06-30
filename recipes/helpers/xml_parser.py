import xml.etree.ElementTree as ET
"""
The current version of this module will only return the first recipe node
of the elemnt tree. It cannot be used to return muliple recipes from a single
XML file!
"""

class BeerXMLParser(object):
    """ A class for parsing beer xml files
    Initiate an object with the path (full or relative)
    to the file.
    """
    def __init__(self, file):
        # file path to xml doc
        self.file = file


    def parse_file(self):
        """ Sets the root element of the tree
        and calls methods for data colletion.
        """
        self.tree = ET.parse(self.file)
        # we only grab the first recipe node of the XML tree.
        self.recipe = self.tree.getroot()[0]
        self._set_basic_data()
        self._set_hops()
        self._set_mash_steps()
        self._set_fermentables()
        self._set_misc()
        self._set_yeast()


    def _set_basic_data(self):
        """ Set a dict of the various useful elements from the tree. """
        self.recipe_name = self.recipe.find('NAME').text
        self.version = self.recipe.find('VERSION').text
        self.style = self.recipe.find('STYLE').find('NAME').text
        self.boil_time = self.recipe.find('BOIL_TIME').text.split('.')[0]
        self.brew_type = self.recipe.find('TYPE').text

        # volume converted from liters to gallons
        self.batch_volume = (
            "{:.2f}".format(float(self.recipe.find ('BATCH_SIZE').text)
            * .264172)
        )

        self.og = self.recipe.find('EST_OG').text.split()[0]
        self.abv = self.recipe.find('EST_ABV').text.split()[0]

        # converted from liters to gallons
        self.boil_volume = (
            "{:.2f}".format(float(self.recipe.find ('BOIL_SIZE').text)
            * .264172)
        )
        self.efficiency = (
            "{:.2f}".format(float(self.recipe.find('EFFICIENCY').text))
        )

        self.strike = self.recipe.find('MASH').find('MASH_STEPS')[0]
        self.strike_volume = (
            self.strike.find('DISPLAY_INFUSE_AMT').text.split()[0]
        )
        self.strike_temp = self.strike.find('INFUSE_TEMP').text.split()[0]

        self.boil_grav = self._calc_boil_grav()

        # Put all of the elements into a dict.
        self.basic_data = {
            'recipe_name': self.recipe_name,
            'version': self.version,
            'style': self.style,
            'boil_time': self.boil_time,
            'brew_type': self.brew_type,
            'batch_volume': self.batch_volume,
            'og': self.og,
            'abv': self.abv,
            'boil_volume': self.boil_volume,
            'efficiency': self.efficiency,
            'strike_volume': self.strike_volume,
            'strike_temp': self.strike_temp,
            'boil_grav': self.boil_grav
        }


    def _calc_boil_grav(self):
        """ There is no tag for pre-boil volume so it  must calculated. """
        equip = self.recipe.find('EQUIPMENT')
        self.trub_loss = (
            equip.find('DISPLAY_TRUB_CHILLER_LOSS').text.split()[0]
        )
        water_loss = (
            float(self.boil_volume)
            - float(self.batch_volume)
            - float(self.trub_loss)
        )
        post_boil_vol = float(self.batch_volume) + float(self.trub_loss)
        # use the forumula: ((Va x SGa) + (Vb x SGb))/(Va + Vb) = boil_grav
        boil_grav = (
            "{:.3f}".format(
                 (water_loss + (post_boil_vol * float(self.og)))
                 / float(self.boil_volume)
           )
        )
        return boil_grav


    def _set_mash_steps(self):
        ''' Returns a tuple of (name, time, temperature) for each
        mash step into a list. All values are collected as strings.
        '''
        self.mash_steps = []

        # loop through the tee and find our mash steps
        for step in self.tree.iter('MASH_STEP'):
            name = step.find('NAME').text
            # dropping the trailing 0's
            time = step.find('STEP_TIME').text.split('.')[0]
            farenheit = round(float(step.find('STEP_TEMP').text) * 1.8 + 32)
            temp = "{:.0f}".format(farenheit)
            elements = {'name': name, 'time': time, 'temp': temp}
            self.mash_steps.append(elements)

    def _set_hops(self):
        '''Returns a list of 4 tuples for all of the hops in a recipe.
        Tuple structure: (name, amount, time, use).
        '''
        self.hops = []

        for hop in self.tree.iter('HOP'):
            name =  hop.find('NAME').text
            type_of = hop.find('TYPE').text
            # convert the weight from mg to oz
            amount ="{:.2f}".format(float(hop.find('AMOUNT').text) * 35.274)
            # dropping the trailing 0's
            use = hop.find('USE').text
            if use != 'Dry Hop':
                time = hop.find('TIME').text.split('.')[0]
            else:
                # convert dry hop time from minutes to days
                days = int(float(hop.find('TIME').text) / 1440)
                time = str(days)
            hop_data = {
                'name': name,
                'type_of': type_of,
                'amount': amount,
                'use':use,
                'time': time,
            }

            self.hops.append(hop_data)


    def _set_fermentables(self):
        """ The fermentable ingredients like grains, sugars, etc.
        for a recipe.
        """
        self.fermentables = []

        for fermentable in self.tree.iter('FERMENTABLE'):
            name = fermentable.find('NAME').text
            type_of = fermentable.find('TYPE').text
            amount = fermentable.find('DISPLAY_AMOUNT').text.split()[0]
            fermentable_data = {
                'name': name,
                'type_of': type_of,
                'amount': amount}
            self.fermentables.append(fermentable_data)

    def _set_misc(self):
        """ A list of 5 tuples for the additional non-fermentable ingredients
        a recipe such as oak, lactose, cacao nibs, etc.
        """
        self.misc = []

        for misc in self.tree.iter('MISC'):
            name = misc.find('NAME').text
            type_of = misc.find('TYPE').text
            use = misc.find('USE').text
            amount = misc.find('DISPLAY_AMOUNT').text.split(' ')[0]
            time = misc.find('DISPLAY_TIME').text
            # time returns time and unit. Example:
            # '5.0 days' or '10.0 mins'
            misc_data = {
                'name': name,
                'type_of': type_of,
                'use': use,
                'amount': amount,
                'time': time,
            }
            self.misc.append(misc_data)

    def _set_yeast(self):
        """ A list of 5 tuples for the yeast(s) in a reicpe. """
        self.yeast = []

        for yeast in self.tree.iter('YEAST'):
            name = yeast.find('NAME').text
            type_of = yeast.find('TYPE').text
            lab = yeast.find('LABORATORY').text
            product_id = yeast.find('PRODUCT_ID').text
            # product_id returns time and unit. Example:
            # '124.10 ml'
            amount = yeast.find('DISPLAY_AMOUNT').text
            yeast_data = {
                'name': name,
                'type_of': type_of,
                'lab': lab,
                'product_id': product_id,
                'amount': amount,
            }
            self.yeast.append(yeast_data)


    def get_basic_data(self):
        """ returns a dict of the basic recipe elements """
        return self.basic_data


    def get_mash_steps(self):
        ''' returns a list of mash steps '''
        return self.mash_steps


    def get_hops(self):
        ''' returns a list of all hops.
        List elements are dicts of hop data.
        '''
        return self.hops

    def get_fermentables(self):
        ''' returns a list of fermentable ingredients '''
        return self.fermentables


    def get_misc(self):
        ''' returns a list of miscellaneous ingredients '''
        return self.misc


    def get_yeast(self):
        ''' returns a list of yeast(s) for a recipe '''
        return self.yeast


    def get_all_data(self):
        ''' a dict of all useful recipe data '''
        self.all_data = {
            'basic_data': self.basic_data,
            'mash_steps': self.mash_steps,
            'hops': self.hops,
            'fermentables': self.fermentables,
            'misc': self.misc,
            'yeast': self.yeast,
        }

        return self.all_data
