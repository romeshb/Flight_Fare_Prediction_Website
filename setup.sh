mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"email@domain\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor='#3a70ec'
backgroundColor='#FFD600'
textColor='#0e1862'
secondaryBackgroundColor=’#F0F2F6’
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml


