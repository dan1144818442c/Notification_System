import { useEffect, useState } from "react";
import "../style/CarPage.css";
import CarDescription from "./CarDescription";
import ContinueButton from "./ContinueButton";

export default function CarPage({
  image,
  description,
  score,
  continueSowCar,
  isDangerous,
}: {
  image: string | undefined;
  description: string;
  score: number;
  continueSowCar: () => void;
  isDangerous: boolean;
}) {
  const [carImageUrl, setCarImage] = useState<string>();

  useEffect(() => {
    const getCarData = async () => {
      try {
        const respons = await fetch(`http://localhost:8001/image/${image}`, {
          method: "GET",
        });
        const blob = await respons.blob();
        const imageUrl = URL.createObjectURL(blob);
        setCarImage(imageUrl);
      } catch (err) {
        console.log(err);
      }
    };
    getCarData();
  }, [image]);
  return (
    <>
      <article id="carPage">
        <img id="image" src={carImageUrl} alt="" />
        <CarDescription description={description} score={score} />
        <ContinueButton ifShow={isDangerous} setRefresh={continueSowCar} />
      </article>
    </>
  );
}
