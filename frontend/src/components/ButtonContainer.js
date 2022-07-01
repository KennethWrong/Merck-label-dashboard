import React from "react";
import { Stack } from "@mui/material";
import { Button } from "@mui/material";
import QrCodeIcon from "@mui/icons-material/QrCode";
import ImageSearchIcon from "@mui/icons-material/ImageSearch";
import { useNavigate } from "react-router-dom";
import UploadFileIcon from '@mui/icons-material/UploadFile';
import FlipIcon from '@mui/icons-material/Flip';


function ButtonContainer() {
  let history = useNavigate();

  function handleButtonClick(link) {
    history(link);
  }

  return (
    <>
      <Stack className="button-grp" direction="row" spacing={2}>
        <Button
          onClick={() => {handleButtonClick('/QRScanner')}}
          variant="contained"
          startIcon={<FlipIcon />}
        >
          Scan Tag
        </Button>
        <Button
          onClick={() => {handleButtonClick('/create/qr_code')}}
          variant="contained"
          startIcon={<QrCodeIcon />}
        >
          Create QR Code
        </Button>
        <Button
          onClick={() => {handleButtonClick('/csv_upload')}}
          variant="contained"
          startIcon={<UploadFileIcon />}
        >
          Upload CSV
        </Button>
        <Button
          onClick={() => {handleButtonClick('/lookup')}}
          variant="contained"
          startIcon={<ImageSearchIcon />}
        >
          Key Look-up
        </Button>
      </Stack>
    </>
  );
}
export default ButtonContainer;
