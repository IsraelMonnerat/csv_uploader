import React, { useState } from "react";
import { Navigate } from "react-router-dom"; // Importe o Navigate
import { Grid, Button } from "@mui/material";
import TableCSV from "../../components/tableCSV/TableCSV";

interface CSVReaderProps {
  FileCSV: string[][];
  isEditar?: boolean;
  handleFileUpload?: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const CSVReader = (props: CSVReaderProps) => {
  const { FileCSV, handleFileUpload, isEditar = false, page, pageSize, setPage, setPageSize, totalItems, data, isAdd, setIsAdd } = props;
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [redirect, setRedirect] = useState<boolean>(false); // Adiciona o estado de redirecionamento

  const handleFileUploadInternal = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (handleFileUpload) {
      handleFileUpload(event);
    }
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleSend = () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://localhost:8150/csv-uploader/api/upload-csv-file", {
      method: "POST",
      body: formData,
    })
      .then(response => {
        if (response.ok) {
          setRedirect(true); // Atualiza o estado para redirecionar
        } else {
          return response.json().then((error) => {
            console.error("Error:", error);
            // Tratar outros status ou exibir mensagens de erro aqui
          });
        }
      })
      .catch(error => {
        console.error("Error:", error);
      });
  };

  if (redirect) {
    return <Navigate to="/consultar" />; // Redireciona para a página desejada
  }

  return (
    <>
      <TableCSV isAdd={isAdd} setIsAdd={setIsAdd} FileCSV={FileCSV} isEditar={isEditar} page={page} data={data} pageSize={pageSize} setPage={setPage} totalItems={totalItems} setPageSize={setPageSize} />
      <Grid item xs={12}>
        <input
          accept=".csv"
          id="contained-button-file"
          type="file"
          style={{ display: "none" }}
          onChange={handleFileUploadInternal}
        />
        <label htmlFor="contained-button-file">
          <Button className="button-upload" variant="contained" component="span">
            Selecionar
          </Button>
        </label>
        {FileCSV.length > 0 && !isEditar && (
          <Button
            className="button-upload"
            variant="contained"
            component="span"
            onClick={handleSend}
          >
            Enviar
          </Button>
        )}
      </Grid>
    </>
  );
};

export default CSVReader;
