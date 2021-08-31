const path = require('path');
const express = require('express');
const port = 8000;
app = express();

app.use(express.json(), express.urlencoded({extended: true}));

app.use('/', express.static(path.join(__dirname, './public')));


app.listen(port, () => console.log('Mock Server on port', port));