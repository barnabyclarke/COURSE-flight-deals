from data_manager import DataManager


class FlightData(DataManager):
    # This class is responsible for structuring the flight data.
    def __init__(self):
        super().__init__()
        self.count = 0
        self.cheaper_list = []

        if len(self.flight_list) > 0:
            for destination in self.flight_list:
                for travel_info in destination:
                    index = {
                        "price": f"{travel_info['price']}",
                        "airport_from": f"{travel_info['cityFrom']}-{travel_info['flyFrom']}",
                        "airport_to": f"{travel_info['cityTo']}-{travel_info['flyTo']}",
                        "via_city": "",
                        "date_from": f"{((travel_info['route'][0]['local_departure']).split('T'))[0]}",
                        "date_to": f"{((travel_info['route'][-1]['local_arrival']).split('T'))[0]}",
                        "link": travel_info["deep_link"],
                    }
                    if len(travel_info['route']) == 3:
                        if travel_info['route'][1]['cityTo'] == travel_info['cityTo']:
                            index["via_city"] = f", via {travel_info['route'][1]['cityFrom']}-" \
                                                f"{travel_info['route'][1]['flyFrom']} outwards"
                        else:
                            index["via_city"] = f"{travel_info['route'][1]['cityTo']}-" \
                                                f"{travel_info['route'][1]['flyTo']} return"
                    elif len(travel_info['route']) == 4:
                        index["via_city"] = f", via {travel_info['route'][0]['cityTo']}-" \
                                            f"{travel_info['route'][0]['flyTo']} outwards and " \
                                            f"{travel_info['route'][2]['cityTo']}-{travel_info['route'][2]['flyTo']} " \
                                            f"return"

                    if travel_info["price"] < self.travel_table["prices"][self.count]["lowestPrice"]:
                        self.cheaper_list.append(index)
                self.count += 1
