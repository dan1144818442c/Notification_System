import type ICarInfo from "../interfaces/ICarInfo";
import "../style/Details.css";

export default function Details({
  model,
  color,
  number,
  original_details,
  is_off_road,
  score,
}: ICarInfo) {
  return (
    <>
      <article id="detailsComp">
        <ul id="ulDetails">
          <li className="liInfo">{model} : דגם נוכחי</li>
          <li className="liInfo">{color} : צבע נוכחי</li>
          <li className="liInfo">{number} : לוחית רישוי</li>
          <li className="liInfo">
            האם ירד מהכביש : {is_off_road === "True" ? "כן" : "לא"}
          </li>
          <li className="liInfo">{score} : ציון מסוכנות</li>
          <li className="liInfo">{original_details.model} : דגם מקורי</li>
          <li className="liInfo">צבע מקורי : {original_details.color}</li>
        </ul>
      </article>
    </>
  );
}
