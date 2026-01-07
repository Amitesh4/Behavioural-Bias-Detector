const express = require('express');
const { MongoClient } = require('mongodb');
const cors = require('cors');

const app = express();
app.use(cors());

const uri = "mongodb+srv://Pawan_Yadav_084:Pawan123@pawan.wy2hqmv.mongodb.net/?appName=Pawan";
const client = new MongoClient(uri);

app.get('/api/risk-data', async (req, res) => {
    try {
        await client.connect();
        const database = client.db('WealthTech');
        const collection = database.collection('RiskMetrics');
        
        // Sabse latest data nikaalo
        const latestData = await collection.find().sort({ timestamp: -1 }).limit(1).toArray();
        res.json(latestData[0]);
    } catch (error) {
        res.status(500).send(error.message);
    }
});

app.listen(5001, () => console.log('Server running on port 5001'));