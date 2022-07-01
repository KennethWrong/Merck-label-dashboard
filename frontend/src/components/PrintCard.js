import React, {useState} from "react";
import {Button, Box } from "@mui/material";
import axios from 'axios'
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export const PrintCard = (props) => {
    const [size, setSize] = useState('2ml');

    const handleChange = (event) => {
        setSize(event.target.value);
    };


    const printImg = async () => {
        try{
            await axios.get(`http://localhost:5000/print/${props.qr_key}?size=${size}`);
        }catch(e){
            props.changeDisplayMessage(`Error occured when priting QRCode Label: ${props.qr_key}`, "error")
        }
      };

    const removePrintCard = () => {
        let newLableData = Object.keys(props.labelData).filter(key =>
            key !== props.qr_key).reduce((obj, key) =>
            {
                obj[key] = props.labelData[key];
                return obj;
            }, {}
        );
        props.changeDisplayMessage(`Successfully removed QRCode Label: ${props.qr_key}`, "success")
        props.setLabelData(newLableData)
    }


return (
    <Box sx={{ display: 'flex', flexDirection:'column', 
    justifyContent: 'space-evenly', backgroundColor:'#D9EAF7', padding:'1.0em',mb:'1.5em' }}>
        <h1>QRCode Key is: <span style={{color:'#007A73'}}>{props.qr_key}</span></h1>
        <Box sx={{ display: 'flex', flexDirection:'row', alignItems: 'center',
        justifyContent: 'space-evenly'}}>
            <img
            alt="Generated QR Code"
            src={`data:image/png;base64,${props.base64Encoding}`}
            />
            <Box sx={{ display: 'flex', flexDirection:'column', alignItems: 'center',
        justifyItems: 'space-between'}}>
                <Button variant="contained" sx={{mb:'1.0em'}} size="large"
                onClick={() => {printImg()}}>
                        Print
                </Button>
                <FormControl sx={{mb:'1.0em'}}>
                    <InputLabel id="demo-simple-select-label">Size</InputLabel>
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
                <Button variant="contained" sx={{mb:'1.0em', backgroundColor:"red"}} size="large"
                onClick={() => {removePrintCard()}}>
                        Remove
                </Button>
            </Box>
        </Box>
    </Box>
);
}

export default PrintCard