import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import {BrowserRouter} from "react-router-dom";
import AppBar from './components/Appbar'
import QRScanner from "./components/QRScanner";
import CreateQRcode from "./routes/CreateQRcode";
import Home from "./components/Home";
import { FindProduct } from "./components/FindProduct";
import FileUpload from "./components/FileUpload";
import LookUp from "./components/Lookup";
import { Routes, Route} from "react-router";

const font = "'Lato', sans-serif";


const theme = createTheme({
  palette: {
    primary: {
      main: '#007a73',
    },
    secondary: {
      main: '#231f20',
    },
  },
  typography: {
    fontFamily: font,
    h4:{
      fontWeight: 700,
    },
    button:{
      fontWeight: 600,
    },
  },
});

ReactDOM.render(
<ThemeProvider theme={theme}>
    <BrowserRouter>
            <AppBar />
            <Routes>
                <Route path="/QRScanner" element={<QRScanner />} />
                <Route path="/create/qr_code" element={<CreateQRcode />} />
                <Route path="/findProduct" element={<FindProduct />} />
                <Route path="/csv_upload" element={<FileUpload />} />
                <Route path="/lookup" element={<LookUp />} />
                <Route path="/" element={<Home />} />
            </Routes>
    </BrowserRouter>
  </ThemeProvider>,document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
