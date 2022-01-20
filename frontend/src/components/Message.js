import {Box, Alert} from "@mui/material";

export const Message = ({success, error}) => {
    const severity = () => {
        
    }
  <Box mt={5} mb={5}>
    <Alert severity="success" style={{ fontSize: "40px" }}>
      {success}
    </Alert>
  </Box>;
};
