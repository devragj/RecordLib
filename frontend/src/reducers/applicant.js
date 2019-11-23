import { ADD_OR_REPLACE_APPLICANT, EDIT_APPLICANT, EDIT_ALIAS, ADD_ALIAS } from "../actions/applicant"
import { combineReducers } from "redux";

const initialApplicant = {
    first_name: '',
    last_name: '',
    date_of_birth: '',
    date_of_death: '',
    ssn: '',
    address: '',
    aliases: [],
    editing: true
 };



const applicantInfoReducer = combineReducers({
    applicant: applicantReducer,
    aliases: aliasReducer,
})

export default applicantInfoReducer

function aliasReducer(state = {}, action) {
    switch(action.type) {
        case ADD_OR_REPLACE_APPLICANT: {
            console.log("ADD OR REPLACE APPLICANT payload")
            console.log(action.payload) 
            const callback = (acc, curr) => {
                return(Object.assign(acc, curr))
            }
            const { aliases } = action.payload
            return Object.assign({}, state, 
                aliases.map(alias => {
                    return({[alias]: alias})
                }).reduce(callback, {})
            )
        }
        case EDIT_ALIAS:
        case ADD_ALIAS:
        {
            const { id, value } = action.payload;
            
            const newState = Object.assign({}, state, {
                [id]: value
            });
            
            return newState;
        }
        default:
            return state
    }
}
    
function applicantReducer(state = initialApplicant, action) {
    switch (action.type) {
        case EDIT_APPLICANT: {
            const { field, value } = action.payload;

            const newState = Object.assign({}, state, {
                [field]: value
            });

            return newState;
        }
        case ADD_OR_REPLACE_APPLICANT: {
            var applicant = action.payload;

            // Some values are null when sent from the server.
            // Delete these null values, so that state remains with 
            // previous values.
            Object.keys(applicant).forEach(key => {
                if (!applicant[key]) {
                    delete applicant[key]
                }
            })

            const newState = Object.assign({}, state, {
                ...applicant,
                aliases: Array.from(new Set([...state.aliases, ...applicant.aliases]))
            })
            
            // If state already has a name for the applicant, don't overwrite it.
            // (for example, user may have entered it manually)
            if (state.first_name !== '') {
                newState.first_name = state.first_name
            }
            if (state.last_name !== '') {
                newState.last_name = state.last_name
            }
            
            // Similarly if state already has a date of birth for the applicant, 
            // don't overwrite it with the new one.
            if (state.date_of_birth ) {
                newState.date_of_birth = state.date_of_birth;
            }

            return newState;
        }
        case ADD_ALIAS: {
            const { id, value } = action.payload;

            const newState = Object.assign({}, state, {
                aliases: state.aliases.concat(id)
            });

            return newState;
        }
        default:
            return state
    }
}

/**
 * deprecated, no longer called, here for reference.
 */
// function originalapplicantReducer(state=initialApplicantState, action) {
//     switch (action.type) {
//         case EDIT_APPLICANT: {
//             const { field, value } = action.payload;

//             const newState = Object.assign({}, state, {
//                 applicant: Object.assign({}, state.applicant, {
//                     [field]: value
//                 })
//             });

//             return newState;
//         }
//         case EDIT_ALIAS: {
//             const { id, value } = action.payload;

//             const newState = Object.assign({}, state, {
//                 aliases: Object.assign({}, state.aliases, {
//                     [id]: value
//                 })
//             });

//             return newState;
//         }
//         case ADD_ALIAS: {
//             const { id, value } = action.payload;

//             const newState = Object.assign({}, state, {
//                 applicant: Object.assign({}, state.applicant, {
//                     aliases: state.applicant.aliases.concat([id])
//                 }),
//                 aliases: Object.assign({}, state.aliases, {
//                     [id]: value
//                 })
//             });

//             return newState;
//         }
//         case ADD_APPLICANT: {
//             const applicant = action.payload;
//             const aliasObject = applicant.aliases;
//             const oldAliasNames = Object.values(state.aliases);
//             const newAliases = {};
//             const newKeys = [];
//             for (const [key, value] of Object.entries(aliasObject)) {
//                 if (!oldAliasNames.includes(value)) {
//                     newKeys.push(key);
//                     newAliases[key] = value;
//                 }
//             }

//             const newState = Object.assign({}, state, {
//                 applicant: Object.assign({}, state.applicant, {
//                     aliases: state.applicant.aliases.concat(newKeys)
//                 }),
//                 aliases: Object.assign({}, state.aliases, newAliases)
//             });

//             if (newState.applicant.first_name === '' && newState.applicant.last_name === '') {
//                 newState.applicant.first_name = applicant.first_name;
//                 newState.applicant.last_name = applicant.last_name;
//             }

//             if (newState.applicant.date_of_birth === '') {
//                 newState.applicant.date_of_birth = applicant.date_of_birth;
//             }

//             return newState;
//         }
//         default:
//             return state;
//     }
// }
