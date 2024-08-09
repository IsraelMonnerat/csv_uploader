import React, { useState, useEffect } from "react";
import { Container, Grid, Button, TextField } from "@mui/material";
import CSVReader from "../CSVReader";
import axios from "axios";

export const ConsultarCSV = () => {
  const [fileCSV, setFileCSV] = useState<string[][]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(0);
  const [pageSize, setPageSize] = useState<number>(10);
  const [totalItems, setTotalItems] = useState<number>(0);
  const [data, setData] = useState<any[]>([]);

  // Campos de pesquisa
  const [searchColumn, setSearchColumn] = useState<string>("");
  const [searchValue, setSearchValue] = useState<string>("");
  const [isAdd, setIsAdd] = useState<boolean>(false);

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setPageSize(parseInt(event.target.value, 10));
    setPage(0);
  };

  useEffect(() => {
    const fetchCSVData = async () => {
      try {
        const response = await fetch("http://localhost:8150/csv-uploader/api/all", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "page": page + 1,
            "page_size": pageSize
          },
        });

        if (response.ok) {
          let data = await response.json();
          let totalItems = data.shift();
          setData(data);
          setTotalItems(totalItems);
          // Processar a lista de objetos em JSON para uma matriz bidimensional, se necessário
          const processedData = data.map((item: any) => Object.values(item));
          setFileCSV(processedData);
        } else {
          throw new Error("Falha ao buscar dados");
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
        setError("Não foi possível carregar os dados.");
      } finally {
        setLoading(false);
      }
    };

    fetchCSVData();
  }, [page, pageSize]);

  const onSubmit = async (values) => {
    try {
        // Adicionar
        await axios.post(`http://localhost:8150/csv-uploader/api/add-item`, values);
        console.log("Item adicionado com sucesso");
        window.location.reload(); // Atualiza a página após sucesso
    } catch (error) {
        console.error("Erro ao enviar dados:", error);
    }
}
  const handleDownload = async () => {
    try {
      const response = await fetch("http://localhost:8150/csv-uploader/api/csv-file", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "planilha.csv"); // Nome do arquivo para o download
        document.body.appendChild(link);
        link.click();
        link.remove();
      } else {
        throw new Error("Falha ao baixar o arquivo");
      }
    } catch (error) {
      console.error("Erro ao baixar o arquivo:", error);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://localhost:8150/csv-uploader/api/filter/field/${encodeURIComponent(searchColumn)}/value/${encodeURIComponent(searchValue)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        // Processar os dados para atualizar o estado
        const processedData = data.map((item: any) => Object.values(item));
        setFileCSV(processedData);
        setData(data);
        setTotalItems(data.length);
      } else {
        throw new Error("Falha ao buscar dados");
      }
    } catch (error) {
      console.error("Erro ao buscar dados:", error);
      setError("Não foi possível carregar os dados.");
    }
  };

  if (loading) {
    return <p>Carregando...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <Container>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleDownload}>
            Download Documento
          </Button>
          {/* Campos de pesquisa */}
          <TextField
            label="Coluna"
            value={searchColumn}
            onChange={(e) => setSearchColumn(e.target.value)}
            style={{ marginLeft: '10px' }}
          />
          <TextField
            label="Valor"
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            style={{ marginLeft: '10px' }}
          />
          <Button
            variant="contained"
            color="secondary"
            onClick={handleSearch}
            style={{ marginLeft: '10px' }}
          >
            Pesquisar
          </Button>
          {!isAdd && (
            <Button
            variant="contained"
            color="secondary"
            onClick={() => setIsAdd(true)}
            style={{ marginLeft: '10px' }}
          >
            Adicionar Novo Item
          </Button>
          )}
          <p className="label_form">Selecionar arquivo csv</p>
          <CSVReader isAdd={isAdd} setIsAdd={setIsAdd} FileCSV={fileCSV} page={page} pageSize={pageSize} setPage={handleChangePage} setPageSize={handleChangeRowsPerPage} totalItems={totalItems} data={data} isEditar={true} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default ConsultarCSV;
