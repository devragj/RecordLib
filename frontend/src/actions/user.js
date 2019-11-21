import * as api from "../api"

export const FETCH_USER_PROFILE_SUCCEEDED = "FETCH_USER_PROFILE_SUCCEEDED"

export function fetchUserProfileSucceeded(profileData) {
        return({
                type: 'FETCH_USER_PROFILE_SUCCEEDED',
                payload: profileData
        })
}


export function fetchUserProfile() {
        return(dispatch => {
                api.fetchUserProfileData().then(response => {
                        const data = response.data
                        dispatch(fetchUserProfileSucceeded(data))
                }).catch(err => {
                        console.log("fetching user profile failed because:")
                        console.log(err)
                })
        })
}