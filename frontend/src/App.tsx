import React from "react";
import "./App.css";
import { Navigate, Route, Routes } from "react-router-dom";
import Header from "./components/header";
import EnviarCSV from "./pages/csvReader/enviar";
import { ConsultarCSV } from "./pages/csvReader/consultar";
import EditarCSV from "./pages/csvReader/editar/index";
import { useGetPokemonByNameQuery } from "./services/csv";

const App = () => {

  const { data, error, isLoading } = useGetPokemonByNameQuery('bulbasaur');
  console.log("data", data)

  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Navigate to="/upload" />} />
        <Route path="/upload" element={<EnviarCSV />} />
        <Route path="/consultar" element={<ConsultarCSV />} />
        <Route path="/editar/:id" element={<EditarCSV />} />
      </Routes>
    </>
  );
};

export default App;
