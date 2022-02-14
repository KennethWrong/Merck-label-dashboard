import { Box } from "@mui/system";
import axios from "axios";
import React, { useEffect } from "react";
import { useState } from "react";
import QRScan from "react-qr-reader";
import BasicTable from "./ScanTable";
import { Alert } from "@mui/material";

function QRScanner() {
  const [qrScan, setQrScan] = useState("");
  const [total_scans, setTotal_scans] = useState([]);
  const [errorMessage, setErrorMessage] = useState(false);
  const [successMessage, setSuccessMessage] = useState(false);

  

  const handleScan = (data) => {
    if (data) {
      console.log(data);
      let responseJSON = modifyToJSON(data);
      setQrScan(responseJSON["qr_code_key"]);
    }
  };
  const handleError = (e) => {
    console.error(e);
  };

  useEffect(() => {
    if (qrScan) {
      async function sendInfoToFlask() {
        let obj = {
          qr_code_key: qrScan,
        };
        try {
          //post request to our backend
          let mes = await axios.post("http://localhost:5000/scan/qr_code", obj);
          console.log(mes.data)
          let resJSON= mes.data;
          
          const new_scanned_item = {
            qr_code_key: resJSON.qr_code_key,
            experiment_id: resJSON.experiment_id,
            contents: resJSON.contents,
            analyst: resJSON.analyst,
            storage_condition: resJSON.storage_condition,
            date_entered: resJSON.date_entered,
            expiration_date: resJSON.expiration_date,
          }
          total_scans.splice(0, 0, new_scanned_item)
          setTotal_scans(total_scans)
          
          setSuccessMessage(true);
          setTimeout(() => {
            setSuccessMessage(false);
          }, 1500);
          
        } catch (e) {
          console.log(e);
          setErrorMessage(true);
          setTimeout(() => {
            setErrorMessage(false);
          }, 1500);
        }
      }
      sendInfoToFlask();
    }
  }, [qrScan, total_scans]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1>Qr Scanner</h1>
      <div>
        <QRScan
          delay={300}
          onError={handleError}
          onScan={handleScan}
          style={{ height: 240, width: 320, borderRadius: 5 }}
        />
      </div>
      <Box sx={{ mt: 12 }}>
        <BasicTable total_scans={total_scans}/>
      </Box>

      {successMessage ? (
        <Box mt={5} mb={5}>
          <Alert severity="success" style={{ fontSize: "40px" }}>
            Successfully Scanned Item
          </Alert>
        </Box>
      ) : (
        ""
      )}
      {errorMessage ? (
        <Box mt={5} mb={5}>
          <Alert severity="error" style={{ fontSize: "40px" }}>
            Scan was unsuccessful, try again please
          </Alert>
        </Box>
      ) : (
        ""
      )}
    </div>
  );
}

const modifyToJSON = (message) => {
  message = message.replace(/'/g, '"');
  let responseJSON = JSON.parse(message);
  return responseJSON;
};

export default QRScanner;
