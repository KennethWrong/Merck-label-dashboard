import React from "react";
import { Alert, Stack, Button, Box } from "@mui/material";
import axios from 'axios'


export const PrintCard = (props) => {

    const printImg = async () => {
        console.log(`http://localhost:5000/print/${props.qr_key}`)
        let res = await axios.get(`http://localhost:5000/print/${props.qr_key}`);
        console.log(res)
      };


return (
    <Box sx={{ display: 'flex', flexDirection:'column', 
    justifyContent: 'space-evenly', backgroundColor:'#D9EAF7', padding:'1.0em',mb:'1.5em' }}>
        <h1>QRCode Key is: {props.qr_key}</h1>
        <Box sx={{ display: 'flex', flexDirection:'row', alignItems: 'center',
        justifyContent: 'space-evenly'}}>
            <img
            alt="Generated QR Code"
            src={`data:image/png;base64,${props.base64Encoding}`}
            />
            <Button variant="contained"
            onClick={() => {printImg()}}>
                    Print
            </Button>
        </Box>
    </Box>
);
}

export default PrintCard