import React from "react";
import { Grid, TextField, Button } from "@mui/material";
import { useState, useEffect } from "react";
import { useFormik } from "formik";
import axios from "axios";

const EditarCSV = ({ FileCSV, redirect, isAdd, setIsAdd }) => {
    const [initialValues, setInitialValues] = useState({});
    const [isAdding, setIsAdding] = useState(false);
    const [verify, setVerify] = useState(false);

    useEffect(() => {
        if (redirect.length > 0) {
            const editarRow = FileCSV?.find(file => file.id === redirect[0]);
            if (editarRow) {
                setInitialValues(editarRow);
            }
        }
    }, [redirect, FileCSV]);

    useEffect(() => {
        if (isAdd) {
            setInitialValues({});
            // Caso seja uma adição, podemos exibir o formulário sem esperar por initialValues
            setVerify(true);
        } else if (!isAdd && initialValues && Object.keys(initialValues).length > 0) {
            // Caso seja uma edição, só exibir quando initialValues estiver populado
            setVerify(true);
        }
    }, [isAdd, initialValues]);

    const formik = useFormik({
        initialValues: initialValues,
        enableReinitialize: true,
        onSubmit: async (values) => {
            try {
                if (isAdding) {
                    // Adicionar
                    await axios.post(`http://localhost:8150/csv-uploader/api/add-item`, values);
                    console.log("Item adicionado com sucesso");
                } else {
                    // Atualizar
                    const { id, ...payload } = values;
                    await axios.put(`http://localhost:8150/csv-uploader/api/update/id/${id}`, payload);
                    console.log("Item atualizado com sucesso");
                }
                window.location.reload(); // Atualiza a página após sucesso
            } catch (error) {
                console.error("Erro ao enviar dados:", error);
            }
        },
    });

    if (!verify) return null;

    return (
        <form onSubmit={formik.handleSubmit} style={{ padding: "30px" }}>
            <Grid container spacing={3}>
                <Grid item xs={3}>
                    <label className="label_form">Nome</label>
                    <TextField 
                        name="nome"
                        value={formik.values.nome || ""}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={3}>
                    <label className="label_form">Data de Nascimento</label>
                    <TextField 
                        name="data_nascimento"
                        value={formik.values.data_nascimento || ""}
                        placeholder="aaaa/mm/dd"
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={3}>
                    <label className="label_form">Nacionalidade</label>
                    <TextField 
                        name="nacionalidade"
                        value={formik.values.nacionalidade || ""}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={3}>
                    <label className="label_form">Gênero</label>
                    <TextField 
                        name="genero"
                        value={formik.values.genero || ""}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={3}>
                    <label className="label_form">Data de Cadastro</label>
                    <TextField 
                        name="data_criacao"
                        value={formik.values.data_criacao || ""}
                        placeholder="aaaa/mm/dd"
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={3}>
                    <label className="label_form">Data de Atualização</label>
                    <TextField 
                        name="data_atualizacao"
                        value={formik.values.data_atualizacao || ""}
                        placeholder="aaaa/mm/dd"
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                </Grid>
                <Grid item xs={12}>
                    {isAdd ? (
                        <Button 
                        type="button" 
                        variant="contained" 
                        color="secondary" 
                        onClick={() => {
                            setIsAdding(true);
                            setIsAdd(false);
                            formik.handleSubmit();
                        }}
                    >
                        Adicionar
                    </Button>
                    ) : (
                        <Button 
                        type="button" 
                        variant="contained" 
                        color="primary" 
                        onClick={() => {
                            setIsAdding(false);
                            formik.handleSubmit();
                        }}
                    >
                        Atualizar
                    </Button>
                    )}
                </Grid>
            </Grid>
        </form>
    );
};

export default EditarCSV;
