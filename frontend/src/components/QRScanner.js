
import { Box } from "@mui/system";
import axios from "axios";
import React, { useEffect } from "react";
import {useState} from "react";
import QRScan from 'react-qr-reader';
import BasicTable from "./ScanTable";
import { Alert } from '@mui/material';

function QRScanner () {
    const [qrScan, setQrScan] = useState('');
    const [errorMessage, setErrorMessage] = useState(false)
    const [successMessage, setSuccessMessage] = useState(false)

    const [allValues, setAllValues] = useState({
        qr_code_key: '',
        PC: '',
        sampleID: '',
        batchID: '',
        date: ''
     });


    const handleScan = data => {
        if (data) {
            console.log(data)
            let responseJSON = modifyToJSON(data)
            setQrScan(responseJSON['qr_code_key'])
        }
    }
    const handleError = e => {
        console.error(e);
    }

    useEffect(()=>{
        if(qrScan){
            async function sendInfoToFlask(){
                let obj = {
                    'qr_code_key':qrScan
                }
                try{
                    //post request to our backend
                    let res = await axios.post('http://localhost:5000/scan/qr_code',obj)
                    let responseJSON = res.data

                    setAllValues({
                                qr_code_key : responseJSON.qr_code_key,
                                PC : responseJSON.protein_concentration,
                                sampleID : responseJSON.sample_id,
                                batchID : responseJSON.batch_id,
                                date : responseJSON.date_entered
                    })
                    setSuccessMessage(true)
                    setTimeout(() => {
                      setSuccessMessage(false)
                    },1500)
                }
                catch(e){
                    console.log(e)
                    setErrorMessage(true)
                    setTimeout(() => {
                      setErrorMessage(false)
                    },1500)
                }
            }
            sendInfoToFlask()
        }
    },[qrScan])

    return (
        <div style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>

        <h1>Qr Scanner</h1>
        <div>
            <QRScan
            delay = {300}
            onError={handleError}
            onScan={handleScan}
            style={{height: 240, width: 320, borderRadius:5}}
            />
        </div>
        <Box sx={{ mt: 12, }}>
        <BasicTable info={allValues}/>
        </Box>

        {successMessage?
        <Box mt={5} mb={5}>
            <Alert severity="success" style={{ fontSize: '40px' }}>Successfully Scanned Item</Alert>
        </Box>:''
        }
        {errorMessage?
        <Box mt={5} mb={5}>
            <Alert severity="error" style={{ fontSize: '40px' }}>Scan was unsuccessful, try again please</Alert>
        </Box>:''
        }
        </div>
    )
}

const modifyToJSON = (message) => {
    message = message.replace(/'/g, '"')
    let responseJSON = JSON.parse(message)
    return responseJSON
}

export default QRScanner;