/**
 * Add an Analysis returned from the server to the state.
 * 
 * @param {*} state 
 * @param {*} action 
 */
export default function analysisReducer(state={}, action) {
    switch (action.type) {
        case 'ANALYZE_CRECORD_SUCCEEDED':
            return action.payload;
        default:
            return state;
    }
}

