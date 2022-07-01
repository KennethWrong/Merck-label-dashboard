import { useState} from "react";
import { Stack, TextField, Alert, Box, Hidden } from "@mui/material";
import { Button } from "@mui/material";
import axios from "axios";
import DatePicker from "@mui/lab/DatePicker";

import AdapterDateFns from "@mui/lab/AdapterDateFns";
import LocalizationProvider from "@mui/lab/LocalizationProvider";
// analyst, expiry, contents, experimentId, storageCondition, size

const sizes = ["2mL", "2.5mL", "4mL", "20mL"];

function CreateQRcode() {
  const [analyst, setAnalyst] = useState("");
  const [expiry, setExpiry] = useState(new Date());
  const [contents, setContents] = useState("");
  const [experimentId, setExperimentId] = useState("");
  const [storageCondition, setStorageCondition] = useState("");
  const [size, setSize] = useState(sizes[0]);
  const [trueSize, setTrueSize] = useState(size);
  const [qr, setQR] = useState("");
  const [dateEntered, setDateEntered] = useState(new Date());
  const [dateModified, setDateModified] = useState(new Date());
  const [base64Encoding, setBase64Encoding] = useState("");
  const [message, setMessage] = useState(false);
  const [severity, setSeverity] = useState("success")

  const dateToString = (dateObj) =>
    `${String(dateObj.getMonth() + 1).padStart(2, "0")}/${String(
      dateObj.getDate()
    ).padStart(2, "0")}/${dateObj.getFullYear()}`;

  const handleChangeAnalyst = (e) => {
    setAnalyst(e.target.value);
  };

  const handleChangeDateEntered = (e) => {
    setDateEntered(e);
  };

  const handleChangeDateModified = (e) => {
    setDateModified(e);
  };

  const handleChangeExpiry = (e) => {
    setExpiry(e);
  };

  const handleChangeContents = (e) => {
    setContents(e.target.value);
  };
  const handleChangeStorageCondition = (e) => {
    setStorageCondition(e.target.value);
  };

  const handleChangeExperiment = (e) => {
    setExperimentId(e.target.value);
  };

  const changeDisplayMessage = (message, severity) => {
    setMessage(message);
    setSeverity(severity)
    setTimeout(() => {
        setSeverity("success");
        setMessage("");
    }, 1000);
}

  const printImg = async () => {
    let size_string = size.substring(0, size.length - 2)
    try{
      let res = await axios.get(`http://localhost:5000/print/${qr}?size=${size_string}`);
      changeDisplayMessage("Successfully printed QRCode", "success")
    } catch(e){
        changeDisplayMessage("An error has occured. Please try again.", "error")
        console.log(e);
    }
  };

  const sendQRCode = async () => {
    try {
      let obj = {
        experiment_id: experimentId,
        analyst: analyst,
        expiration_date: dateToString(expiry),
        date_modified: dateToString(dateModified),
        date_entered: dateToString(dateEntered),
        contents: contents,
        storage_condition: storageCondition,
        size: size,
      };
      let res = await axios.post("http://localhost:5000/create/qr_code", obj);
      setQR(res.data["qr_code_key"]);
      setTrueSize(size);
      setExperimentId("");
      setAnalyst("");
      setExpiry(new Date());
      setDateEntered(new Date());
      setDateModified(new Date());
      setContents("");
      setStorageCondition("");
      setBase64Encoding(res.data["image_string"])
      setMessage("Successfully created QRCode");
      setTimeout(() => {
        setMessage("");
    },1000);
    } catch (e) {
          setSeverity("error");
          setMessage("An error has occured. Please try again.");
            setTimeout(() => {
                setSeverity("success");
                setMessage("");
            }, 1000);
      console.log(e);
    }
  };

  return (
    <>
      <Box mt={5} mb={5} sx={{visibility: message?'visible':'hidden'}}>
        <Alert severity={severity} style={{ fontSize: "20px", minHeight:"2.2em"}}>
            {message}
        </Alert>
      </Box>

      <Stack width={"100vw"} mx={2} spacing={2} mt={2} direction="row">
        <Stack width={"45vw"} spacing={2}>
          <TextField
            required
            label="Experiment ID"
            value={experimentId}
            onChange={handleChangeExperiment}
            id="outline-required"
            variant="filled"
            margin="dense"
          />
          <TextField
            required
            id="outlined-required"
            label="Storage Condition"
            value={storageCondition}
            onChange={handleChangeStorageCondition}
            margin="dense"
            variant="filled"
          />
          <TextField
            required
            id="outlined-required"
            label="Contents"
            value={contents}
            onChange={handleChangeContents}
            margin="dense"
            variant="filled"
          />
          <TextField
            required
            id="outlined-required"
            label="Analyst"
            value={analyst}
            onChange={handleChangeAnalyst}
            margin="dense"
            variant="filled"
          />

          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              label="Date Entered"
              value={dateEntered}
              onChange={handleChangeDateEntered}
              renderInput={(params) => (
                <TextField
                  id="outlined-required"
                  margin="dense"
                  variant="filled"
                  required
                  {...params}
                />
              )}
            />
            <DatePicker
              label="Expiry"
              value={expiry}
              onChange={handleChangeExpiry}
              renderInput={(params) => (
                <TextField
                  id="outlined-required"
                  margin="dense"
                  variant="filled"
                  required
                  {...params}
                />
              )}
            />

            <DatePicker
              label="Date Modified"
              value={dateModified}
              onChange={handleChangeDateModified}
              renderInput={(params) => (
                <TextField
                  id="outlined-required"
                  margin="dense"
                  variant="filled"
                  required
                  {...params}
                />
              )}
            />
          </LocalizationProvider>

          <Stack spacing={2} direction={"row"}>
            {sizes.map((d, i) => {
              return (
                <Button
                  variant={size === d ? "contained" : "outlined"}
                  onClick={() => {
                    setSize(d);
                  }}
                  sx={{ textTransform: "none" }}
                  key={i}
                >
                  {d}
                </Button>
              );
            })}
          </Stack>
          <Button
            variant="contained"
            color="primary"
            size="large"
            disabled={
              experimentId &&
              analyst &&
              expiry &&
              dateModified &&
              dateEntered &&
              contents &&
              storageCondition
                ? false
                : true
            }
            onClick={() => {
              sendQRCode();
            }}
          >
            Create
          </Button>
        </Stack>
        <Stack alignItems={"center"} width={"45vw"} justifyContent={"center"}
        sx={{backgroundColor:'#D9EAF7'}}>
          {qr ? (
            <div>
              <h1>QR code Key: <span style={{color:'#007A73'}}>{qr}</span></h1>
              <img
                alt="Generated QR Code"
                src={base64Encoding?`data:image/png;base64,${base64Encoding}`:''}
              />
            </div>
          ) : (
            ""
          )}
          {qr ? <Button
              size="large"
              sx={{mt:'1.0em'}}
              variant="contained"
              onClick={() => {
                printImg();
              }}
            >
              Print
            </Button>: (
            ""
          )}
        </Stack>
      </Stack>
    </>
  );
}

export default CreateQRcode;
