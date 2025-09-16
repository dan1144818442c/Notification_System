import requests, os, json

from log.logger import Logger


class Retriever:
    def __init__(self):
        self.commercial_vehicles_rid  = os.environ.get("COMMERCIAL_RID", "053cea08-09bc-40ec-8f7a-156f0677aff3")
        self.heavy_vehicles_rid = os.environ.get("HEAVY_RID", "cd3acc5c-03c3-4c89-9c54-d40f93c0d790")
        self.tew_wheeler_vehicles_rid = os.environ.get("TEW_WHEELER_RID","bf9df4e2-d90d-4c0a-a400-19e15af8e95f")
        self.public_transport_vehicles_rid = os.environ.get("PUBLIC_RID","cf29862d-ca25-4691-84f6-1be60dcb4a1e")
        self.off_the_road_vehicles_rid = os.environ.get("OFF_ROAD_RID","851ecab1-0622-4dbe-a6c7-f950cf82abf9")
        self.logger = Logger.get_logger()


    def retrieve_cars_data(self, license_plate: str, type: str) -> tuple[dict, str]:
        """Retrieve vehicle color and model based on license plate and type."""
        match type:
            case "commercial":
                return self.get_original_vehicle_data(license_plate, self.commercial_vehicles_rid)
            case "heavy":
                return self.get_original_vehicle_data(license_plate, self.heavy_vehicles_rid)
            case "motorcycle":
                return self.get_original_vehicle_data(license_plate, self.heavy_vehicles_rid)
            case "public":
                return self.get_original_vehicle_data(license_plate, self.heavy_vehicles_rid)
            case _:
                self.logger.error("Invalid type. Must be 'commercial', 'heavy', 'motorcycle', or 'public'.")
                return {"color": None, "model": None}, "false"


    def get_original_vehicle_data(self, license_plate, RID):
         """Retrieve original vehicle data from data.gov.il API."""
         try:
            res_off_road = self.check_if_off_road(license_plate)
            if res_off_road:
                return res_off_road, "true"

            r = requests.get(
                "https://data.gov.il/api/3/action/datastore_search",
                params={"resource_id": RID, "filters": json.dumps({"mispar_rechev": license_plate}), "limit": 1},
                timeout=20,
            )
            rec = r.json().get("result")["records"]
            if not rec:
                self.logger.warning(f"Vehicle with licence plate {license_plate} not found.")
                color, model = None, None
            else:
                rec = rec[0]

                color_value = rec.get("tzeva_rechev")
                color = str(color_value) if color_value is not None else None

                model_value = rec.get("kinuy_mishari") or rec.get("degem_nm")
                model = str(model_value) if model_value is not None else None

            self.logger.info(f"Retrieved original details for vehicle with license plate {license_plate}: color={color}, model={model}")
            return {"color": color, "model": model}, "false"

         except requests.RequestException as e:
            self.logger.error(f"Error retrieving data from gov.il api: {e}")
            return {"color": None, "model": None}, "false"

         except Exception as e:
            self.logger.error(f"Error retrieving original vehicle data: {e}")
            return {"color": None, "model": None}, "false"


    def check_if_off_road(self, license_plate: str) -> dict | None:
        """Check if a vehicle is off the road based on its license plate."""
        try:
            r = requests.get(
                "https://data.gov.il/api/3/action/datastore_search",
                params={"resource_id": self.off_the_road_vehicles_rid, "filters": json.dumps({"mispar_rechev": license_plate}), "limit": 1},
                timeout=15,
            )
            rec = r.json().get("result")["records"]
            if not rec:
                self.logger.info(f"Vehicle with licence plate {license_plate} is not off the road.")
                return None

            self.logger.info(f"Vehicle with licence plate {license_plate} is off the road.")
            rec = rec[0]

            color = rec.get("tzeva_rechev")
            model = rec.get("kinuy_mishari") or rec.get("degem_nm")

            return {"color": str(color), "model": str(model)}


        except requests.RequestException as e:
            self.logger.error(f"Error retrieving data from gov.il api: {e}")
            return None

        except Exception as e:
            self.logger.error(f"Error checking if vehicle is off the road: {e}")
            return None