const express = require('express');
const ziti = require('@openziti/ziti-sdk-nodejs');
const { sendData, createDevice, updateDevice, updateDeviceInfo } = require('./utils/client.js');

// OpenZiti Configuration
const zitiConfig = {
    controller: 'http://localhost:1280',
    identity: 'nodeapp.jwt',        
};

const app = express();
const PORT = 3000;

app.use(express.json());

app.post('/data', async (req, res) => {
    try {
        const response = await sendData(req.body);
        res.status(200).json({ message: 'Data sent successfully', response });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/dev', async (req, res) => {
    try {
        const response = await createDevice(req.body);
        res.status(200).json({ message: 'Device created successfully', response });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/update-dev', async (req, res) => {
    try {
        const response = await updateDevice(req.body);
        res.status(200).json({ message: 'Device updated successfully', response });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.put('/dev/dev_info/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const response = await updateDeviceInfo(id, req.body);
        res.status(200).json({ message: 'Device info updated successfully', response });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.listen(PORT, async () => {
    console.log(`Server running on http://localhost:${PORT}`);

    // Openziti configuration to be added
    try {
        console.log('Initializing OpenZiti...');
        await ziti.init(zitiConfig.identity);
        console.log('OpenZiti initialized successfully');
    } catch (error) {
        console.error('Error initializing OpenZiti:', error.message);
    }
});
