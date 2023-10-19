from .wrapper import GoogleMaps


class MapsBot:
    def __init__(self):
        for try_ in range(5):
            try:
                self.maps_wrapper = GoogleMaps()
                self.maps_wrapper.login()
                break
            except Exception as e:
                self.error_manager(e, try_)

    def search(self, search_text: str):
        for try_ in range(5):
            try:
                self.maps_wrapper.search(search_text)
                print("searched")
                results = self.maps_wrapper.get_search_results()
                results = self.maps_wrapper.search_in_landing(results)
                self.maps_wrapper.close_session()
                return {"results": results, "number_of_results": len(results)}
            except Exception as e:
                self.error_manager(e, try_)

    def error_manager(self, e, try_):
        print(e)
        print("Failed. Trying again.")
        if try_ == 4:
            print("Failed. Max tries reached.")
            raise e
        self.maps_wrapper.close_session()
