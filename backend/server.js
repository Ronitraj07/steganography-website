const express = require('express');
const cors = require('cors');
const path = require('path');
const { exit } = require('process');

const app = express();
const PORT = 3000;

app.use(cors());

// Serve the frontend static files
app.use(express.static(path.join(__dirname, '../frontend')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

app.listen(PORT, () => {
    console.log(`Node.js server is running on http://localhost:${3000}`);
});