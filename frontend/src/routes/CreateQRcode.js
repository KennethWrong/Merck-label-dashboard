import { useState } from "react";
import { Stack, TextField } from "@mui/material";
import { Button } from "@mui/material";
import axios from "axios";

// analyst, expiry, contents, experimentId, storageCondition, size

function CreateQRcode() {
  const [analyst, setAnalyst] = useState("");
  //TODO: do we need this to be a date picker or a text field is fine?
  const [expiry, setExpiry] = useState("");
  const [contents, setContents] = useState("");
  const [experimentId, setExperimentId] = useState("");
  const [storageCondition, setStorageCondition] = useState("");
  const [size, setSize] = useState("s");
  const [qr, setQR] = useState("");

  const handleChangeAnalyst = (e) => {
    setAnalyst(e.target.value);
  };

  const handleChangeExpiry = (e) => {
    setExpiry(e.target.value);
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

  const sendQRCode = async () => {
    try {
      let obj = {
        experiment_id: experimentId,
        analyst: analyst,
        expiry: expiry,
        contents: contents,
        storage_condition: storageCondition,
      };
      let res = await axios.post("http://localhost:5000/create/qr_code", obj);
      setQR(res.data);
      setExperimentId("");
      setAnalyst("");
      setExpiry("");
      setContents("");
      setStorageCondition("");
      console.log(qr);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <Stack width={"100vw"} mx={2} spacing={2} mt={2} direction="row">
      <Stack width={"45vw"} spacing={2}>
        <TextField
          required
          id="outlined-required"
          label="Analyst"
          value={analyst}
          onChange={handleChangeAnalyst}
          margin="dense"
          variant="filled"
        />

        <TextField
          required
          id="outlined-required"
          label="Expiry"
          value={expiry}
          onChange={handleChangeExpiry}
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
        <Stack spacing={2} direction={"row"}>
          <Button
            variant={size === "s" ? "contained" : "outlined"}
            onClick={() => {
              setSize("s");
            }}
          >
            S
          </Button>
          <Button
            variant={size === "m" ? "contained" : "outlined"}
            onClick={() => {
              setSize("m");
            }}
          >
            M
          </Button>
          <Button
            variant={size === "l" ? "contained" : "outlined"}
            onClick={() => {
              setSize("l");
            }}
          >
            L
          </Button>
        </Stack>
        <Button
          variant="contained"
          color="success"
          size="large"
          onClick={sendQRCode}
        >
          Create
        </Button>
      </Stack>
      <Stack alignItems={"center"} width={"45vw"} justifyContent={"center"}>
        <h1>{qr}</h1>
        {qr ? (
          <div>
            <h1>QR code has Key {qr}</h1>
            <img
              alt="Generated QR Code"
              src={`http://localhost:5000/assets/qr_code/${qr}`}
            />
          </div>
        ) : (
          ""
        )}
      </Stack>
    </Stack>
  );
}

export default CreateQRcode;
