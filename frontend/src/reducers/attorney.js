/**
 * manage changes to the state of the Attorney of this session.
 */
export default function attorneyReducer(state={}, action) {
    switch(action.type) {
        case 'ADD_ATTORNEY': {
            const { attorney } = action.payload;


            const newState = Object.assign({},state, attorney)
            return newState;
        }
        case 'EDIT_ATTORNEY': {
            const { field, value } = action.payload;
            const newState = Object.assign({},state, {
                    [field]: value
                });
            return newState;
        }
        case 'TOGGLE_EDITING_ATTORNEY': {

            const { editing } = state


            const newState = Object.assign({},state, {
                    editing: !editing
                })
            return newState;
        }
        default: {
            return state
        }
    }
}

