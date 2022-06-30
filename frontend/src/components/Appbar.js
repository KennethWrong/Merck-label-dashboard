import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";


import Button from "@mui/material/Button";
import ButtonContainer from "./ButtonContainer";

export default function ButtonAppBar() {
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Button
              href="/"
              color="inherit"
              disableRipple
              disableElevation
              sx={{ flexGrow: 1 }}
              style={{ backgroundColor: "transparent",fontSize: 20 }}
            >
              MERCK QR
            </Button>

            <Button
              href="/"
              color="inherit"
              disableRipple
              disableElevation
              style={{ backgroundColor: "transparent" }}
            >
              Home
            </Button>
          </Toolbar>
        </AppBar>
      </Box>
      <br />
      <ButtonContainer />
    </>
  );
}
