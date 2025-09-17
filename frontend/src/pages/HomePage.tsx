import { useEffect, useState } from "react";
import type ICarInfo from "../interfaces/ICarInfo";
import CarImage from "../components/CarPage";
import Details from "../components/Detalils";
import "../style/HomePage.css";

export default function HomePage() {
  const [carData, setCarData] = useState<ICarInfo>();
  const [shouldRefresh, setShouldRefresh] = useState(true);

  useEffect(() => {
    if (!shouldRefresh) return;

    const getCarData = async () => {
      try {
        const respons = await fetch("http://localhost:8081", {
          method: "GET",
        });
        const result = await respons.json();
        setCarData(result);
      } catch (err) {}
    };
    getCarData();

    const interval = setInterval(() => {
      getCarData();
    }, 3000);

    return () => clearInterval(interval);
  }, [shouldRefresh]);

  useEffect(() => {
    console.log(carData?.score);
    if (carData && carData.score > 40) {
      console.log("fuck");
      setShouldRefresh(false);
    }
  }, [carData]);
  return (
    <>
      <article id="homePage">
        {carData && <Details {...(carData as ICarInfo)} />}
        {carData && (
          <CarImage
            image={carData?.image_id}
            description={carData?.description}
            score={carData.score}
          />
        )}
        {carData && carData.score > 40 && (
          <button id="continu" onClick={() => setShouldRefresh(true)}>{"אישור המשך בדיקה"}</button>
        )}
      </article>
    </>
  );
}
