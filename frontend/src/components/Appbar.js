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
            {/* <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton> */}
            {/* make it a button and disable ripple, elevation, etc. */}
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
