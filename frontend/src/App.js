import "./App.css";
import Appbar from "./components/Appbar";
import { Routes, Route } from "react-router";
import QRScanner from "./components/QRScanner";
import Home from "./components/Home";
import CreateQRcode from "./routes/CreateQRcode";
import { FindProduct } from "./components/FindProduct";
import FileUpload from "./components/FileUpload";
import LookUp from "./components/Lookup";

function App() {
  return (
    <>
      <Appbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/QRScanner" element={<QRScanner />} />
        <Route path="/create/qr_code" element={<CreateQRcode />} />
        <Route path="/findProduct" element={<FindProduct />} />
        <Route path="/csv_upload" element={<FileUpload />} />
        <Route path="/lookup" element={<LookUp />} />
      </Routes>
    </>
  );
}

export default App;
