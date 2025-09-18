import { useEffect, useState } from "react";
import "../style/CarDescription.css";

export default function CarDescription({
  description,
  score,
}: {
  description: string;
  score: number;
}) {
  const [className, setClassName] = useState("regular");
  useEffect(() => {
    if (score > 40) {
      setClassName("dangerous");
    } else if (score > 20) {
      setClassName("unsafe");
    } else {
      setClassName("regular");
    }
  }, [score]);
  return (
    <section id="description" className={className}>
      <p id="descriptionText">תיאור : {description}</p>
    </section>
  );
}
