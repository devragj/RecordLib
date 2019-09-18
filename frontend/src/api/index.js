import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
        baseURL: API_BASE_URL,
        headers: {
                'Content-Type': 'application/json',
        },
});

/**
 * function to post a Summary pdf file to the server
 * @param  {Object} file - uploaded Summary pdf file
 * @return {Object} a promise
 */
export function fetchCRecord(file) {
        const data = new FormData();
        data.append('file', file);
        return client.post("/upload/", data, {});
}