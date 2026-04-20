const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();


// Increase the default max listeners to prevent memory leak warnings
require('events').EventEmitter.defaultMaxListeners = 20;
// Load environment variables from .env file
require('dotenv').config();

const API_URL =  process.env.API_URL || "http://api:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    const status = err.response?.status || 500;
    const message = err.response?.data || { error : "something went wrong"};
    res.status(status).json(message);
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    const status = err.response?.status || 500;
    const message = err.response?.data || { error : "something went wrong"};
    res.status(status).json(message);
  }
});

// Health Check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(3000, () => {
  console.log('Frontend running on port 3000');
});
