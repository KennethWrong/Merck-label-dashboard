import React, { useState } from "react";
import { Stack } from "@mui/material";
import { Button } from "@mui/material";
import UploadIcon from '@mui/icons-material/Upload';
import QrCodeScannerIcon from '@mui/icons-material/QrCodeScanner';
import axios from 'axios'

function ButtonContainer() {
  const [file, setFile] = useState(null)


  const handleFileChange = (e) => {
    e.preventDefault()
    setFile(e.target.files[0])
  }

  const handleFileSubmit = async (e) => {
    e.preventDefault()
    let formData = new FormData()
    formData.append('csv',file)

    let res = await axios.post('http://localhost:5000/csv', formData)
  }

  return (
    <>
      <Stack className='button-grp' direction="row" spacing={2}>
        <div>
          <input type="file" onChange={(e) => handleFileChange(e)}/>
        </div>

          <Button variant="contained" startIcon={<UploadIcon/>} onClick={(e) => handleFileSubmit(e)} type='button'>
            Upload 
            </Button>
          <Button href='/QRScanner' variant="contained" startIcon={<QrCodeScannerIcon/>}>Scan Tag</Button>
          <Button href='/create/qr_code' variant="contained" startIcon={<QrCodeScannerIcon/>}>Create QR Code</Button>
      </Stack>
    </>
  );
}
export default ButtonContainer;
