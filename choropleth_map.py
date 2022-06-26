from choropleth_map_utility import Illness, parameters
import pandas as pd
import folium
import os
import json

# 
#  a class that, given the option, will generate a map 
# for a certain outbreak data set
class mapper():
    def __init__(self, illness):
        # parameters needed based on 
        # the currrent illness being displayed
        self.parameters  = parameters[illness]

        # for later
        self.state_col = 'usa_state'
        self.state_code_col = 'usa_state_code'

    # being given a name, saves the c map into that template
    # use map.html will save to map.html
    def save_map(self, name = "map.html"):
        map = self.get_choropleth_map()
        map.save(os.path.join('./templates', name))

    def save_to_different_maps(self):
        if self.parameters.illness_type == Illness.Covid_19:
            name = "map1.html"
        elif self.parameters.illness_type == Illness.PB_Salmonella:
            name = "map2.html"
        elif self.parameters.illness_type == Illness.BP_Salmonella:
            name = "map3.html"
        elif self.parameters.illness_type == Illness.Monkey_Pox:
            name = "map4.html"
        map.save(os.path.join('./templates', name))

    def get_choropleth_map(self):
        # create the map with a starting coordinate in usa
        (LATITUDE, LONGITUDE) = (37.127476, -99.277467)
        START = [LATITUDE, LONGITUDE]
        ZOOM = 4
        MAX_ZOOM = 15
        folium_map = folium.folium.Map(location=START, zoom_start=ZOOM, max_zoom=MAX_ZOOM)

        # get the data needed for the c map
        geojson = self.get_geo_json()
        data = self.get_full_data()

        # add the cloropeth to the folium map
        self.add_choropeth_to_map(data, geojson, folium_map)

        return folium_map

    def add_choropeth_to_map(self, data, geojson, folium_map):
        cp = folium.Choropleth(
            geo_data=geojson,
            data=data,
            columns=[self.state_col, self.parameters.column_mainvalue],
            key_on='feature.properties.NAME',
            fill_color='YlGn', 
            fill_opacity=0.7, 
            line_opacity=0.2,
            legend_name=self.parameters.legend_name
        ).add_to(folium_map)
        
        self.get_click_popup(data, folium_map, cp)

    def get_click_popup(self, data, folium_map, cp):
        # does not work for the covid 19 data
        if self.parameters.illness_type == Illness.Covid_19:
            return

        # creating a state indexed version of the dataframe so we can lookup values
        indexed = data.set_index(self.state_col)
  
        # looping thru the geojson object and adding a new property
        # and assigning a value from our dataframe
        for s in cp.geojson.data['features']:
            state_name = s['properties']['NAME']
            if len(indexed[indexed.index == state_name]) != 0:
                s['properties']['Number of Cases'] = indexed.loc[state_name, self.parameters.column_mainvalue]
            else:
                s['properties']['Number of Cases'] = 0
            s['properties']['Illness'] = self.parameters.illness_type.value
        
        # and finally adding a tooltip/hover to the choropleth's geojson
        folium.GeoJsonTooltip(['NAME', 'Illness', 'Number of Cases']).add_to(cp.geojson)
        folium.LayerControl().add_to(folium_map)

    def get_geo_json(self, geo_path=r'geojson_states.json'):
        with open(geo_path) as geo_file:
            geo_json = json.load(geo_file)
    
        return geo_json

    # the data is lacking the full names of the state
    # instead, it has initials of the state
    # function will add it 
    def get_full_data(self):
        names_df = self.get_names_df()
        data = self.get_illness_df()
        
        # ensure it is a float
        data[self.parameters.column_mainvalue] = data[self.parameters.column_mainvalue].astype(float)

        # add a name column
        result = data.merge(
            names_df[[self.state_col, self.state_code_col]], 
            left_on=self.parameters.column_state, right_on=self.state_code_col
        )

        return result

    def get_names_df(self, path=r'state_information.csv'):
        data = pd.read_csv(path)
        return data

    def get_illness_df(self):
        filename = self.parameters.file_name
        filetype = self.parameters.file_type
        if filetype == 'CSV':
            data  = pd.read_csv(filename)
        else: # filetype == 'XLSX':
            data = pd.read_excel(filename)

        return data

def main():
    map = mapper(Illness.Covid_19)
    print("hello")
    # map.save_map()
    z = map.get_full_data()
    print(z.info())
    print("world")


# call main whenever you want to update the map to a different illness
main()