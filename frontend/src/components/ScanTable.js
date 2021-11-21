import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function BasicTable(props) {
    let values = props.info

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>QR Code Key</TableCell>
            <TableCell align="right">Sample ID</TableCell>
            <TableCell align="right">Batch ID</TableCell>
            <TableCell align="right">Protein Conc.</TableCell>
            <TableCell align="right">Date Entered</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
            <TableRow
                key={1}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                <TableCell component="th" scope="row">
                    {values.qr_code_key}
                </TableCell>
                <TableCell align="right">{values.sampleID}</TableCell>
                <TableCell align="right">{values.batchID}</TableCell>
                <TableCell align="right">{values.PC}</TableCell>
                <TableCell align="right">{values.date}</TableCell>
            </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default BasicTable