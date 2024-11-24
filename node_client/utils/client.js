const axios = require('axios');

async function sendData(data) {
    try {
        const response = await axios.post(
            'http://127.0.0.1:6202/data',
            data,
            {
                headers: { 'Content-Type': 'application/json' },
            }
        );
        console.log('Data sent successfully:', response.data);
    } catch (error) {
        console.error('Error sending data:', error.message);
    }
}

async function createDevice(data) {
    try {
        const response = await axios.post(
            'http://127.0.0.1:6202/dev',
            data,
            {
                headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer admin-token' },
            }
        );
        console.log('Device created successfully:', response.data);
    } catch (error) {
        console.error('Error creating device:', error.message);
    }
}

async function updateDevice(data) {
    try {
        const response = await axios.put(
            'http://127.0.0.1:6202/dev',
            data,
            {
                headers: { 'Content-Type': 'application/json' },
            }
        );
        console.log('Device updated successfully:', response.data);
    } catch (error) {
        console.error('Error updating device:', error.message);
    }
}

async function updateDeviceInfo(devId, data) {
    try {
        const response = await axios.post(
            `http://127.0.0.1:6202/dev/${devId}/dev_info`,
            data,
            {
                headers: { 'Content-Type': 'application/json' },
            }
        );
        console.log('Device info updated successfully:', response.data);
    } catch (error) {
        console.error('Error updating device info:', error.message);
    }
}

module.exports = { sendData, createDevice, updateDevice, updateDeviceInfo };
