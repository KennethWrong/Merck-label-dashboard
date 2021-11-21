import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import {BrowserRouter} from "react-router-dom";

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
  <App />
  </BrowserRouter>
  </ThemeProvider>,document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
