import React, { useState } from "react";
import { Stack } from "@mui/material";
import { Button } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import QrCodeScannerIcon from "@mui/icons-material/QrCodeScanner";
import axios from "axios";
import { Alert } from "@mui/material";
import Box from "@material-ui/core/Box";
import QrCodeIcon from "@mui/icons-material/QrCode";

function ButtonContainer() {
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState(false);
  const [successMessage, setSuccessMessage] = useState(false);
  console.log(file);

  const handleFileChange = (e) => {
    e.preventDefault();
    setFile(e.target.files[0]);
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("csv", file);
    try {
      let res = await axios.post("http://localhost:5000/csv", formData);
      setSuccessMessage(res.data);
      setTimeout(() => {
        setSuccessMessage(false);
      }, 2000);
    } catch {
      setErrorMessage(true);
      setTimeout(() => {
        setErrorMessage(false);
      }, 1500);
    }
  };

  return (
    <>
      {successMessage ? (
        <Box mt={5} mb={5}>
          <Alert severity="success" style={{ fontSize: "40px" }}>
            {successMessage}
          </Alert>
        </Box>
      ) : (
        ""
      )}
      {errorMessage ? (
        <Box mt={5} mb={5}>
          <Alert severity="error" style={{ fontSize: "40px" }}>
            CSV File Upload failed, Please check file 
          </Alert>
        </Box>
      ) : (
        ""
      )}

      <Stack className="button-grp" direction="row" spacing={2}>
        <div>
          <input type="file" onChange={(e) => handleFileChange(e)} />
        </div>

        {
          <Button
            disabled={file ? false : true}
            variant="contained"
            startIcon={<UploadIcon />}
            onClick={(e) => handleFileSubmit(e)}
            type="button"
          >
            Upload
          </Button>
        }
        <Button
          href="/QRScanner"
          variant="contained"
          startIcon={<QrCodeScannerIcon />}
        >
          Scan Tag
        </Button>
        <Button
          href="/create/qr_code"
          variant="contained"
          startIcon={<QrCodeIcon />}
        >
          Create QR Code
        </Button>
      </Stack>
    </>
  );
}
export default ButtonContainer;
