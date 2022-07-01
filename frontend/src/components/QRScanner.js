import { Box } from "@mui/system";
import axios from "axios";
import React, { useEffect, useState } from "react";
import QRScan from "react-qr-reader";
import BasicTable from "./ScanTable";
import { Alert } from "@mui/material";

function QRScanner() {
  const [qrScan, setQrScan] = useState("");
  const [total_scans, setTotal_scans] = useState([]);
  const [message, setMessage] = useState(false);
  const [severity, setSeverity] = useState("success")
  

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

  const changeDisplayMessage = (message, severity) => {
    setMessage(message);
    setSeverity(severity)
    setTimeout(() => {
        setSeverity("success");
        setMessage("");
    }, 1000);
  }

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
          
          changeDisplayMessage(`Successfully printed QRCode label: ${qrScan}`, "success")
          
        } catch (e) {
          changeDisplayMessage("An error has occured. Please try again.", "error")
          console.log(e);
        }
      }
      sendInfoToFlask();
    }
  }, [qrScan, total_scans]);

  return (
    <>
      <Box mt={5} mb={5} sx={{visibility: message?'visible':'hidden'}}>
        <Alert severity={severity} style={{ fontSize: "20px", minHeight:"2.2em"}}>
            {message}
        </Alert>
      </Box>
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
      </div>
    </>
  );
}

const modifyToJSON = (message) => {
  message = message.replace(/'/g, '"');
  let responseJSON = JSON.parse(message);
  return responseJSON;
};

export default QRScanner;
