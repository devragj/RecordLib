import axios from 'axios';

// Without declaring a BASE_URL, axios just calls to its own domain.
//const API_BASE_URL = 'http://localhost';

const client = axios.create({
        //baseURL: API_BASE_URL,
        headers: {
                'Content-Type': 'application/json',
        },
});

/**
 * function to post record files (currently only pdfs) to the server
 * @param  {Object} files - uploaded Summary and docket pdf files
 * @return {Object} a promise
 */
export function uploadRecords(files) {
        const data = new FormData();
        files.forEach((file) => data.append('files', file))

        return client.post(
                "/record/upload/", data, 
                {headers: {'Content-Type': 'multipart/form-data'}});
}

/**
 * POST a CRecord to the server and retrieve an analysis.
 */
export function analyzeCRecord(data) {
        data.person = data.defendant
        delete data.defendant
        return client.post(
                "/record/analyze/",
                data
        )
}


export function fetchPetitions(petitions) {
        return client.post(
                "/record/petitions/",
                {petitions: petitions}
        )
}