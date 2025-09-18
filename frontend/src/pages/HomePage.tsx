import { useEffect, useState } from "react";
import type ICarInfo from "../interfaces/ICarInfo";
import Details from "../components/Detalils";
import "../style/HomePage.css";
import CarPage from "../components/CarPage";

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
      setShouldRefresh(false);
    }
  }, [carData]);

  const continueSowCar = (): void => {
    setShouldRefresh(true);
  };
  return (
    <>
      <article id="homePage">
        {carData && <Details {...(carData as ICarInfo)} />}
        {carData && (
          <CarPage
            image={carData?.image_id}
            description={carData?.description}
            score={carData.score}
            continueSowCar={continueSowCar}
            isDangerous={carData.score > 40}
          />
        )}
      </article>
    </>
  );
}
