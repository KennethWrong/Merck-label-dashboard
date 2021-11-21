import react, { useState } from 'react'
import { TextField } from '@mui/material'
import { Button } from "@mui/material";
import axios from 'axios';

function CreateQRcode(){
    const [sampleID, setSampleID] = useState('')
    const [BatchID, setBatchID] = useState('')
    const [PC, setPC] = useState('')
    const [qr, setQR] = useState('')

    const handleChangeSample = (e) => {
        setSampleID(e.target.value)
    }

    const handleChangePC = (e) => {
        setPC(e.target.value)
    }

    const handleChangeBatch = (e) => {
        setBatchID(e.target.value)
    }

    const sendQRCode = async() =>{
        try{
            let obj = {
                sample_id : sampleID,
                batch_id : BatchID,
                protein_concentration : PC
            }
            let res = await axios.post('http://localhost:5000/create/qr_code', obj)
            setQR(res.data)

        }catch(e){
            console.log(e)
        }
    }
    
    return(
        <div>
            <TextField fullWidth label="Sample ID" value={sampleID} onChange={handleChangeSample}
            id="fullWidth" variant="filled" margin="dense" />
            <TextField fullWidth label="Batch ID" value={BatchID} onChange={handleChangeBatch}
            id="fullWidth" variant="filled" margin="dense"/>
            <TextField fullWidth label="Protein Concentration" value={PC} onChange={handleChangePC}
            id="fullWidth" variant="filled" margin="dense"/>
            <Button variant="contained" color="success" size='large' onClick={sendQRCode}>
                Success
            </Button>
            <h1>{qr}</h1>
            {qr?
            <div>
                <h1>QR code has Key {qr}</h1>
                <img src={`http://localhost:5000/assets/qr_code/${qr}`} />
            </div>:''}
        </div>
    )
}

export default CreateQRcode