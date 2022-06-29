import { useState } from "react";
import { Stack, TextField } from "@mui/material";
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
  // const [selectedDate, handleDateChange] = useState(new Date());

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

  const printImg = () => {
    const url = `http://localhost:5000/assets/qr_code/${qr}_${size}?${experimentId}`;

    const win = window.open("");
    win.document.write("<html><head>");
    win.document.write("</head><body>");
    win.document.write('<img id="print-image-element" src="' + url + '"/>');
    win.document.write(
      '<script>var img = document.getElementById("print-image-element"); img.addEventListener("load",function(){ window.focus(); window.print(); window.document.close(); window.close(); }); </script>'
    );
    win.document.write("</body></html>");
    win.window.print();
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
      console.log(res);
      setQR(res.data["qr_code_key"]);
      setTrueSize(size);
      // setExperimentId("");
      // setAnalyst("");
      // setExpiry(new Date());
      setDateEntered(new Date());
      setDateModified(new Date());
      // setContents("");
      // setStorageCondition("");
      setBase64Encoding(res.data["image_string"])
    } catch (e) {
      console.log(e);
    }
  };

  return (
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
      <Stack alignItems={"center"} width={"45vw"} justifyContent={"center"}>
        {/* <h1>{qr}</h1> */}
        {qr ? (
          <div>
            <h1>QR code has Key {qr}</h1>
            <img
              alt="Generated QR Code"
              src={base64Encoding?`data:image/png;base64,${base64Encoding}`:''}
            />
          </div>
        ) : (
          ""
        )}
        {qr ? (
          <Button
            onClick={() => {
              printImg();
            }}
          >
            Print
          </Button>
        ) : (
          ""
        )}
      </Stack>
    </Stack>
  );
}

export default CreateQRcode;
