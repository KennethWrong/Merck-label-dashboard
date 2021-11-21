import "./App.css";
import Appbar from "./components/Appbar";
import { Routes, Route } from "react-router";
import QRScanner from "./components/QRScanner";
import Home from "./components/Home";

function App() {
  return (
    <>
      <Appbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/QRScanner" element={<QRScanner />} />
      </Routes>
    </>
  );
}

export default App;
