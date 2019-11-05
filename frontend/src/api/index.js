import axios from 'axios';

// Without declaring a BASE_URL, axios just calls to its own domain.
//const API_BASE_URL = 'http://localhost';

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const client = axios.create({
        //baseURL: API_BASE_URL,
        headers: {
                'Content-Type': 'application/json',
        },
        maxRedirects: 5,
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
        return client.post(
                "/record/analyze/",
                data
        )
}


export function fetchPetitions(petitions, attorney) {
        // Send a POST to transform a set of petitions into 
        // rendered petition files, and return the generated files 
        // in a zip file.
        petitions.forEach(p => p.attorney = attorney)
        
        const config = {
                responseType: 'blob',
        }

        return client.post(
                "/record/petitions/",
                {petitions: petitions},
                config,
        )
}

export function login(username, password) {
        const data = new FormData()
        data.append('username', username)
        data.append('password', password)
        client.post(
                "/accounts/login/",
                data,
                {headers: {'Content-Type': 'multipart/form-data'}},
        ).then(response => {
                if (response.data.username) {
                    let date = new Date();
                    date.setTime(date.getTime() + (14 * 24 * 60 * 60 * 1000));
                    document.cookie = "username = " + response.data.username + "; expires = " + date.toGMTString() + "; path=/";
                }

                window.location = "/"
                console.log(response)
        })
}

export function logout() {
        client.get("/accounts/logout/");
        window.location = '/accounts/login';
        document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
}


export function fetchUserProfileData() {
        return client.get("/record/profile/") // TODO thats a bad api endpoint for a user profile.
}