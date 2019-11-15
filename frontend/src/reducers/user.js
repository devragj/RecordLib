import { FETCH_USER_PROFILE_SUCCEEDED } from "../actions/user"

export default function userReducer(state={}, action) {
    switch (action.type) {
        case FETCH_USER_PROFILE_SUCCEEDED: 
            return(Object.assign({}, state, {
                username: action.payload.user.username,
                email: action.payload.user.email,
            }))
        default: {
            return state;
        }
    }
}

