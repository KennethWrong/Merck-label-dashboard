
import { TextareaAutosize } from "@mui/base";
import React from "react";
import {useState} from "react";
import QRScan from 'react-qr-reader';

function QRScanner () {

    const [qrScan, setQrScan] = useState('No result');
    const handleScan = data => {
        if (data) {
            setQrScan(data)
        }
    }

    const handleError = e => {
        console.error(e);
    }

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
        <TextareaAutosize
        style={{fontSize:18, width:320,height:100, marginTop:100}}
        rowsMax={4}
        defaultValue={qrScan}
        value={qrScan}
        />
        </div>
    )
}

export default QRScanner;