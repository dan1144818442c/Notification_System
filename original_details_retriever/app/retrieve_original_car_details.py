import requests, os, json

from log.logger import Logger


class Retriever:
    def __init__(self):
        self.commercial_vehicles_rid  = os.environ.get("COMMERCIAL_RID", "053cea08-09bc-40ec-8f7a-156f0677aff3")
        self.heavy_vehicles_rid     = os.environ.get("HEAVY_RID", "cd3acc5c-03c3-4c89-9c54-d40f93c0d790")
        self.tew_wheeler_vehicles_rid = os.environ.get("TEW_WHEELER_RID","bf9df4e2-d90d-4c0a-a400-19e15af8e95f")
        self.public_transport_vehicles_rid = os.environ.get("PUBLIC_RID","cf29862d-ca25-4691-84f6-1be60dcb4a1e")
        self.logger = Logger.get_logger()


    def retrieve_cars_data(self, license_plate: str, type: str) -> dict:
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
                raise ValueError("Invalid kind. Must be 'commercial', 'heavy', 'motorcycle', or 'public'.")


    def get_original_vehicle_data(self, license_plate, RID):
         """Retrieve original vehicle data from data.gov.il API."""
         try:
            r = requests.get(
                "https://data.gov.il/api/3/action/datastore_search",
                params={"resource_id": RID, "filters": json.dumps({"mispar_rechev": license_plate}), "limit": 1},
                timeout=20,
            )
            rec = r.json()["result"]["records"]
            if not rec:
                self.logger.warning(f"Vehicle with licence plate {license_plate} not found.")
                color, model = None, None
            else:
                rec = rec[0]

                color = rec.get("tzeva_rechev"),
                model = rec.get("kinuy_mishari") or rec.get("degem_nm"),

            self.logger.info(f"Retrieved original details for vehicle with license plate {license_plate}: color={color}, model={model}")
            return {"color": color,
                    "model": model}

         except requests.RequestException as e:
            raise Exception(f"Error retrieving data from gov.il api: {e}")
         except Exception as e:
            raise Exception(f"Error retrieving original vehicle data: {e}")