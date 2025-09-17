import type IOrginalInfo from "./IOrginalInfo";

export default interface ICarInfo {
  model: string;
  color: string;
  number: number;
  type: string;
  image_id: string;
  original_details: IOrginalInfo;
  is_off_road: string;
  score: number;
  description: string;
}
