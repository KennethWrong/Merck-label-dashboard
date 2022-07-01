import React from "react";
import Box from "@material-ui/core/Box";
import '../App.css'; 

function Home() {

  return (
    <Box
    display="flex"
    justifyContent="center"
    alignItems="center"
    minHeight="60vh"
    >
      <Box sx={{display:'flex', flexDirection:'column', justifyContent:'flex-start'}}>
        <h1 style={{color:'#007A73', fontSize:'4em'}}
        className="merckLogo"
        >Merck QR Scanner</h1>
      </Box>
    </Box>
  );
}

export default Home;
