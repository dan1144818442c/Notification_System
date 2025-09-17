import { BrowserRouter, Route, Routes } from "react-router";
import "./App.css";
import Layout from "./components/application-layout/Layout";
import HomePage from "./pages/HomePage";
import About from "./pages/About";

function App() {
  return (
    <>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </>
  );
}

export default App;
