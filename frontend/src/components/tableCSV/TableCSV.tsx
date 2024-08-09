import React from "react";
import {
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { Navigate } from "react-router-dom"; // Importe o Navigate
import EditarCSV from "../../pages/csvReader/editar";
import axios from "axios";

interface TableCSVProps {
  FileCSV: string[][];
  isEditar: boolean;
}

const TableCSV = (props: TableCSVProps) => {
  const { FileCSV, isEditar, page, pageSize, setPage, setPageSize, totalItems, data, isAdd, setIsAdd } = props;
  const [redirect, setRedirect] = React.useState([])
  const handleDelete = async (item) => {
    // Chame a função setRedirect para definir o item a ser redirecionado
    setRedirect(item);
    
    // Acessa o primeiro item do array e extrai o id
    const [firstItem] = item;
    
    try {
        await axios.delete(`http://localhost:8150/csv-uploader/api/delete/id/${firstItem}`);
        console.log("Item excluído com sucesso");
        // Lógica adicional para exclusão
    } catch (error) {
        console.error("Erro ao excluir item:", error);
    }
    window.location.reload();
};

  if (redirect.redirect) {
    return <Navigate to={`/editar${redirect.id}`}/>; // Redireciona para a página desejada

}
  return (
    FileCSV.length > 0 && (
      <Paper style={{ marginBottom: "40px" }}>
        <Table>
          <TableHead
            style={{ background: "#26a69a" }}
            sx={{ fontWeight: "bold" }}
          >
            <TableRow>
              {!isEditar? (
                FileCSV[0].map((header: string, index: number) => (
                  <TableCell key={index}>{header}</TableCell>
                ))
              ): (
                <>
                  <TableCell>id</TableCell>
                  <TableCell>nome</TableCell>
                  <TableCell>data_nascimento</TableCell>
                  <TableCell>nacionalidade</TableCell>
                  <TableCell>genero</TableCell>
                  <TableCell>data_criacao</TableCell>
                  <TableCell>data_atualizacao</TableCell>
                </>
              )
              }
              {isEditar && <TableCell>Ação</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {FileCSV.slice(0).map((row: any, rowIndex: number) => (
              <TableRow key={rowIndex}>
                {row.map((cell: string, cellIndex: number) => (
                  <TableCell key={cellIndex}>{cell}</TableCell>
                ))}
                {isEditar && (
                  <TableCell>
                    <IconButton onClick={() => {
                      setRedirect(row)
                       setIsAdd(false)
                       }} 
                       style={{ color: "#26a69a" }}
                       >
                      <EditIcon />
                    </IconButton>
                    <IconButton  onClick={() => handleDelete(row)} style={{ color: "#26a69a" }}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
          {isEditar && (
            <TablePagination
              count={totalItems}
              page={page}
              onPageChange={setPage}
              rowsPerPage={pageSize}
              onRowsPerPageChange={setPageSize}
            />
          )}
        </Table>
        <EditarCSV
          FileCSV={data}
          redirect={redirect}
          isAdd={isAdd}
          setIsAdd={setIsAdd}
        />
      </Paper>
    )
  );
};

export default TableCSV;
