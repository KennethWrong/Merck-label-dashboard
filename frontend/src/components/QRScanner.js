
import { TextareaAutosize } from "@mui/base";
import { Box } from "@mui/system";
import axios from "axios";
import React, { useEffect } from "react";
import {useState} from "react";
import QRScan from 'react-qr-reader';
import BasicTable from "./ScanTable";

function QRScanner () {
    const [qrScan, setQrScan] = useState('');
    const [textInfo, setTextInfo] = useState('')

    const [allValues, setAllValues] = useState({
        qr_code_key: '',
        PC: '',
        sampleID: '',
        batchID: '',
        date: ''
     });


    const handleScan = data => {
        if (data) {
            setQrScan(data)
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
                    let res = await axios.post('http://localhost:5000/scan/qr_code',obj)
                    let message = res.data
                    
                    message = message.replace(/'/g, '"')
                    let responseJSON = JSON.parse(message)
                    console.log(responseJSON)

                    setAllValues({
                                qr_code_key : responseJSON.qr_code_key,
                                PC : responseJSON.protein_concentration,
                                sampleID : responseJSON.sample_id,
                                batchID : responseJSON.batch_id,
                                date : responseJSON.date_entered
                    })
                }
                catch(e){
                    console.log(e)
                    setTextInfo('QR code does not match any test samples')
                }
            }
            sendInfoToFlask()
        }
    },[qrScan])

    return (
        <div style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
        <h1>Qr Scanner</h1>
        {console.log(allValues)}
        <div>
            <QRScan
            delay = {300}
            onError={handleError}
            onScan={handleScan}
            style={{height: 240, width: 320, borderRadius:5}}
            />
        </div>
        {/* <TextareaAutosize
        style={{fontSize:18, width:500,height:500, marginTop:100}}
        rowsMax={4}
        defaultValue={textInfo}
        value={textInfo}
        /> */}
        <Box sx={{ mt: 12, }}>
        <BasicTable info={allValues}/>
        </Box>
        </div>
    )
}

export default QRScanner;