import "../../style/Header.css";
import imageLogo from "../../logosImages/image.png";
import NavBar from "../NavBar";
import { NavLink } from "react-router";

export default function Header() {
  return (
    <>
      <header id="header">
        <section id="nainHeader">
          <img id="policeLogo" src={imageLogo} alt="Linkodkod logo" />
          <NavBar />
          <div>
            <NavLink id="nameApp" to="about" end>
              About
            </NavLink>
          </div>
        </section>
      </header>
    </>
  );
}
