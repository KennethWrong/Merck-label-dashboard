import {
  Stack,
  Paper,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  IconButton,
} from "@mui/material";
import Webcam from "react-webcam";
import PhotoCameraIcon from "@mui/icons-material/PhotoCamera";
import { useCallback, useRef, useState } from "react";
import axios from "axios";

export const FindProduct = () => {
  const camRef = useRef(null);
  const [image, setImage] = useState(null);
  const capture = useCallback(() => {
    if (camRef) {
      const imgSrc = camRef.current.getScreenshot();
      setImage(imgSrc);
    }
  }, [camRef]);

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("img", image);
    try {
      const res = await axios.post("http://localhost:5000/csv", formData);
      console.log(res.data);
    } catch {
      console.log("error in submission");
    }
  };

  return (
    <Stack
      justifyContent={"center"}
      alignItems={"center"}
      height={"60vh"}
      spacing={2}
    >
      <Stack direction={"row"} justifyContent={"space-around"} width={"100vw"}>
        <Stack alignItems="center" spacing={2}>
          <Webcam
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={{ width: { max: 500 }, aspectRatio: 2 }}
            ref={camRef}
          />
          <IconButton
            color="primary"
            onClick={(e) => {
              e.preventDefault();
              capture();
              handleFileSubmit(e);
            }}
          >
            <PhotoCameraIcon />
          </IconButton>
        </Stack>
        <h4>Hello From the other side</h4>
      </Stack>
      <TableContainer sx={{ width: "20vw" }} component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Product Name</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow
              key={1}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                Ibuprofen
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
};
