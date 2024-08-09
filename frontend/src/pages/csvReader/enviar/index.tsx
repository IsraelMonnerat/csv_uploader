import { Container, Grid } from "@mui/material";
import CSVReader from "../CSVReader";
import { useState } from "react";

export const EnviarCSV = () => {
  const [FileCSV, setFileCSV] = useState<string[][]>([]);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    console.log("", file);
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        const csvData = parseCSV(text);
        setFileCSV(csvData);
      };
      reader.readAsText(file);
    }
  };

  const parseCSV = (text: string): string[][] => {
    const rows = text.split("\n");
    return rows.map((row) => row.split(","));
  };

  return (
    <Container>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <p className="label_form">Selecionar arquivo csv</p>
          <CSVReader FileCSV={FileCSV} handleFileUpload={handleFileUpload} />
        </Grid>
      </Grid>
    </Container>
  );
};

export default EnviarCSV;
