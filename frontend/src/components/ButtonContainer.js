import React from "react";
import { Stack } from "@mui/material";
import { Button } from "@mui/material";
import UploadIcon from '@mui/icons-material/Upload';
import QrCodeScannerIcon from '@mui/icons-material/QrCodeScanner';

function ButtonContainer() {
  return (
    <>
      <Stack className='button-grp' direction="row" spacing={2}>
          <Button href='/' variant="contained" startIcon={<UploadIcon/>}>Upload</Button>
          <Button href='/QRScanner' variant="contained" startIcon={<QrCodeScannerIcon/>}>Scan Tag</Button>

      </Stack>
    </>
  );
}
export default ButtonContainer;
