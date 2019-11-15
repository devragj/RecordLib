export default function petitionsReducer(state={}, action) {
    switch (action.type) {
        case 'FETCH_PETITIONS_SUCCEEDED':
            return state; 
        default:
            return state;
    }
}