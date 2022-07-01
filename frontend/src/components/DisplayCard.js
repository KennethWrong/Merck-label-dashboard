import React, {useState} from "react";
import {Button, Box } from "@mui/material";
import axios from 'axios'
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export const DisplayCard = (props) => {
    const [size, setSize] = useState('2ml');

    const handleChange = (event) => {
        setSize(event.target.value);
    };


    const printImg = async () => {
        try{
            let res = await axios.get(`http://localhost:5000/print/${props.qr_key}?size=${size}`);
        console.log(res)
        }catch(e){
            props.changeDisplayMessage(`Error occured when priting QRCode Label: ${props.qr_key}`, "error")
        }
      };

return (
    <Box sx={{ display: 'flex', flexDirection:'column', 
    justifyContent: 'space-evenly', backgroundColor:'#D9EAF7', padding:'1.0em',mb:'1.5em', mt:'2em' }}>
        <h1>QRCode Key is: <span style={{color:'#007A73'}}>{props.qr_key}</span></h1>
        <Box sx={{ display: 'flex', flexDirection:'row', alignItems: 'center',
        justifyContent: 'space-evenly'}}>
            <img
            alt="Generated QR Code"
            src={`data:image/png;base64,${props.base64Encoding}`}
            />
            <Box sx={{ display: 'flex', flexDirection:'column', alignItems: 'center',
        justifyItems: 'space-between'}}>
                <Button variant="contained" sx={{mb:'10px'}} size="large"
                onClick={() => {printImg()}}>
                        Print
                </Button>
                <FormControl sx={{mt:'10px'}}>
                    <InputLabel>Size</InputLabel>
                    <Select
                    value={size}
                    onChange={handleChange}
                    >
                        <MenuItem value={"2ml"}>2ml</MenuItem>
                        <MenuItem value={"2.5ml"}>2.5ml</MenuItem>
                        <MenuItem value={"4ml"}>4ml</MenuItem>
                        <MenuItem value={"20ml"}>20ml</MenuItem>
                    </Select>
                </FormControl>
            </Box>
        </Box>
    </Box>
);
}

export default DisplayCard