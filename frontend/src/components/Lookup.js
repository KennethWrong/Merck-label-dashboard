import {Box, TextField, Button} from "@material-ui/core";
import { Alert } from "@mui/material";
import { useState } from "react";
import axios from "axios";
import DisplayCard from "./DisplayCard";

const LookUp = () => {
    const [qrCode, setQrCode] = useState("");
    const [message, setMessage] = useState(false);
    const [severity, setSeverity] = useState("success")
    const [label, setLabel] = useState("")


    const handleQrCodeChange = (e) => {
        setQrCode(e.target.value)
    }

    const changeDisplayMessage = (message, severity) => {
        setMessage(message);
        setSeverity(severity)
        setTimeout(() => {
            setSeverity("success");
            setMessage("");
        }, 1000);
      }

    const handleButtonClick = async () => {
        try{
            let res = await axios.get(`http://localhost:5000/asset/${qrCode}`)
            console.log(res.data['image'])
            setLabel(res.data['image'])
            changeDisplayMessage(`Successfully looked up label of: ${qrCode}`, "success")
        }catch(e){
            changeDisplayMessage("Error: Non-existing QRCODE Key. Please try again", "error")
            console.log(e)
        }
    }

    return (
        <Box>
            <Box mt={5} mb={5} sx={{visibility: message?'visible':'hidden'}}>
                <Alert severity={severity} style={{ fontSize: "20px", minHeight:"2.2em"}}>
                    {message}
                </Alert>
            </Box>
            <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            >
        <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        width="40vw"
        >
            <TextField  variant="outlined" label="QR Code" focused fullWidth size="medium"
            value={qrCode} placeholder="Enter QR Code"
            onChange={handleQrCodeChange}/>
        </Box>
        <Button sx={{ml:"10px"}}
        onClick={() => {handleButtonClick()}}>
            Search
        </Button>
    </Box>
        {label? 
        <DisplayCard qr_key={qrCode} base64Encoding={label} changeDisplayMessage={changeDisplayMessage}/>:""}
</Box>
    )
}

export default LookUp