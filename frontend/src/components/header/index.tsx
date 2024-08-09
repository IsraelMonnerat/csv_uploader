import { AppBar, Container, Toolbar, Typography } from "@mui/material";
import ArticleIcon from '@mui/icons-material/Article';

const Header = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: "#26a69a" }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <ArticleIcon sx={{ display: "block", mr: 1 }} />
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="/"
            sx={{
              flexGrow: 1,
              display: "block", // Garante que o texto esteja sempre visível
              overflow: "hidden", // Evita que o texto transborde em telas muito pequenas
              textOverflow: "ellipsis", // Adiciona reticências se o texto não couber
              whiteSpace: "nowrap", // Impede que o texto quebre para a próxima linha
              color: "inherit",
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              textDecoration: "none",
              transition: "color 0.3s ease-in-out", // Adiciona transição suave
              "&:hover": {
                color: "#80cbc4", // Define a cor do texto quando o mouse está sobre ele
              },
            }}
          >
            CSV UPLOADER
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
