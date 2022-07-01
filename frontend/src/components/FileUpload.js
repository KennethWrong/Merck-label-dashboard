import React, { useState} from "react";
import axios from "axios";
import { Alert, Button, Box } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import PrintCard from "./PrintCard";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState(false);
    const [labelData, setLabelData] = useState([])
    const [severity, setSeverity] = useState("success")
    const handleFileChange = (e) => {
        e.preventDefault();
        setFile(e.target.files[0]);
    };

    const changeDisplayMessage = (message, severity) => {
            setMessage(message);
            setSeverity(severity)
            setTimeout(() => {
                setSeverity("success");
                setMessage("");
            }, 1000);
    }

    const handleFileSubmit = async (e) => {
        e.preventDefault();
        let formData = new FormData();
        formData.append("csv", file);
        try {
            let res = await axios.post("http://localhost:5000/csv", formData);
            let data = res.data
            setMessage(data["message"]);
            delete data["message"]
            setLabelData(data)
            setTimeout(() => {
              setMessage("");
          }, 2000);
        } catch {
            changeDisplayMessage("An error has occured. Please try again.", "error")
            console.log(e);
        }
    };

    return (
    <Box>
        <Box mt={5} mb={5} sx={{visibility: message?'visible':'hidden'}}>
            <Alert severity={severity} style={{ fontSize: "20px", minHeight:"2.2em"}}>
                {message}
            </Alert>
        </Box>

        <Box sx={{display: 'flex', flexDirection:'row', alignItems:'flex-start', justifyContent:'center',
    mt:'1.5em', mb:'1.5em'}}>
            <input type="file" onChange={(e) => handleFileChange(e)} />
            <Button
            disabled={file ? false : true}
            variant="contained"
            startIcon={<UploadIcon />}
            onClick={(e) => handleFileSubmit(e)}
            >
            Upload
            </Button>
        </Box>
        <div style={{flex:true, flexDirection:"row"}}>
            {labelData? Object.entries(labelData).map(([key, value]) => {
                return <PrintCard base64Encoding={value} qr_key={key} key={key} labelData={labelData} 
                setLabelData={setLabelData} changeDisplayMessage={changeDisplayMessage}/>
            }
            ):''}
        </div>
    </Box>
    )
}

export default FileUpload
