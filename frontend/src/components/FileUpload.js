import React, { useState, useRef, forwardRef } from "react";
import axios from "axios";
import { Alert, Stack, Button, Box } from "@mui/material";
import UploadIcon from "@mui/icons-material/Upload";
import ReactToPrint from "react-to-print";
import PrintCard from "./PrintCard";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState(false);
    const [successMessage, setSuccessMessage] = useState(false);
    const [labelData, setLabelData] = useState([])

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
            let data = res.data
            console.log(res.data)
            setSuccessMessage(data["message"]);
            delete data["message"]
            setLabelData(data)
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
    <Box>
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

        <Box sx={{display: 'flex', flexDirection:'row', alignItems:'flex-start', justifyContent:'center',
    mt:'1.5em', mb:'1.5em'}}>
            <input type="file" onChange={(e) => handleFileChange(e)} />
            <Button
            // sx={{mt:5}}
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
                return <PrintCard base64Encoding={value} qr_key={key} key={key}/>
            }
            ):''}
        </div>
    </Box>
    )
}

export default FileUpload
