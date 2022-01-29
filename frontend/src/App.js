import "./App.css";
import Appbar from "./components/Appbar";
import { Routes, Route } from "react-router";
import QRScanner from "./components/QRScanner";
import Home from "./components/Home";
import CreateQRcode from "./routes/CreateQRcode";
import { FindProduct } from "./components/FindProduct";

function App() {
  return (
    <>
      <Appbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/QRScanner" element={<QRScanner />} />
        <Route path="/create/qr_code" element={<CreateQRcode />} />
        <Route path="/findProduct" element={<FindProduct />} />
      </Routes>
    </>
  );
}

export default App;
