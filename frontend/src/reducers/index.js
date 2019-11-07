import { combineReducers } from 'redux';

import { CRECORD_ID } from "../normalize";


function userReducer(state={}, action) {
    switch (action.type) {
        case 'FETCH_USER_PROFILE_SUCCEEDED': 
            return(Object.assign({}, state, {
                username: action.payload.user.username,
                email: action.payload.user.email,
            }))
        default: {
            return state;
        }
    }
}

const initialApplicant = {
    first_name: '',
    last_name: '',
    date_of_birth: '',
    date_of_death: '',
    ssn: '',
    address: { line_one: '', city_state_zip: '' },
    aliases: [],
    editing: true
 };

const initialApplicantState = { applicant: initialApplicant, aliases: {} };

function applicantReducer(state=initialApplicantState, action) {
    switch (action.type) {
        case 'EDIT_APPLICANT': {
            const { field, value } = action.payload;

            let newState;
            if (field.substring(0, 7) == 'address') {
                const subfield = field.substring(8);
                newState = Object.assign({}, state, {
                    applicant: Object.assign({}, state.applicant, {
                        address: Object.assign({}, state.applicant.address, {
                            [subfield]: value
                        })
                    })
                });
            }

            else {
                newState = Object.assign({}, state, {
                    applicant: Object.assign({}, state.applicant, {
                        [field]: value
                    })
                });
            }

            return newState;
        }
        case 'EDIT_ALIAS': {
            const { id, value } = action.payload;

            const newState = Object.assign({}, state, {
                aliases: Object.assign({}, state.aliases, {
                    [id]: value
                })
            });

            return newState;
        }
        case 'ADD_ALIAS': {
            const { id, value } = action.payload;

            const newState = Object.assign({}, state, {
                applicant: Object.assign({}, state.applicant, {
                    aliases: state.applicant.aliases.concat([id])
                }),
                aliases: Object.assign({}, state.aliases, {
                    [id]: value
                })
            });

            return newState;
        }
        case 'ADD_DEFENDANT': {
            const defendant = action.payload;
            const aliasObject = defendant.aliases;
            const oldAliasNames = Object.values(state.aliases);
            const newAliases = {};
            const newKeys = [];
            for (const [key, value] of Object.entries(aliasObject)) {
                if (!oldAliasNames.includes(value)) {
                    newKeys.push(key);
                    newAliases[key] = value;
                }
            }

            const newState = Object.assign({}, state, {
                applicant: Object.assign({}, state.applicant, {
                    aliases: state.applicant.aliases.concat(newKeys)
                }),
                aliases: Object.assign({}, state.aliases, newAliases)
            });

            if (newState.applicant.first_name === '' && newState.applicant.last_name === '') {
                newState.applicant.first_name = defendant.first_name;
                newState.applicant.last_name = defendant.last_name;
            }

            if (newState.applicant.date_of_birth === '') {
                newState.applicant.date_of_birth = defendant.date_of_birth;
            }

            return newState;
        }
        default:
            return state;
    }
}



/**
 * Add an Analysis returned from the server to the state.
 * 
 * @param {*} state 
 * @param {*} action 
 */
function analysisReducer(state={}, action) {
    switch (action.type) {
        case 'ANALYZE_CRECORD_SUCCEEDED':
            return action.payload;
        default:
            return state;
    }
}


function petitionsReducer(state={}, action) {
    switch (action.type) {
        case 'FETCH_PETITIONS_SUCCEEDED':
            return state; 
        default:
            return state;
    }
}

/**
 * manage changes to the state of the Attorney of this session.
 */
function attorneyReducer(state={}, action) {
    switch(action.type) {
        case 'ADD_ATTORNEY': {
            const { attorney } = action.payload;


            const newState = Object.assign({},state, attorney)
            return newState;
        }
        case 'EDIT_ATTORNEY': {
            const { field, value } = action.payload;
            let newState;
            if (field.substring(0, 7) == 'address') {
                const subfield = field.substring(8);
                newState = Object.assign({}, state, {
                    organization_address: Object.assign({}, state.organization_address, {
                        [subfield]: value
                    })
                });
            }

            else {
                newState = Object.assign({}, state, {
                    [field]: value
                });
            }

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


const initialCrecordState = {
    charges: {},
    cases: {},
    sentences: {},
    cRecord: { [CRECORD_ID]: { cases:[] } }
};

function cRecordReducer(state = initialCrecordState, action) {
    switch (action.type) {
        case 'FETCH_CRECORD_SUCCEEDED': {
            const newInfo = action.payload.entities;

            const newState = {
                cRecord: {
                    [CRECORD_ID]: Object.assign({}, state.cRecord[CRECORD_ID], {
                        cases: state.cRecord[CRECORD_ID].cases.concat(newInfo.cRecord[CRECORD_ID].cases)
                    })
                },
                cases: Object.assign({}, state.cases, newInfo.cases),
                charges: Object.assign({}, state.charges, newInfo.charges),
                sentences: Object.assign({}, state.sentences, newInfo.sentences)
            };

            return newState;
        }

        // Generic action to edit a field of any of the entities stored in state.
        // This case makes shallow copies so as to edit
        // the field while keeping state immutable.
        // TODO: consider using a library such as immutable.js for this and the next three cases.
        case 'EDIT_ENTITY_VALUE': {
            const { entityName, entityId, field, value } = action.payload;

            const newState = Object.assign({}, state, {
                [entityName]: Object.assign({}, state[entityName], {
                    [entityId]: Object.assign({}, state[entityName][entityId], {
                        [field]: value
                    })
                })
            });

            return newState;
        }

        case 'TOGGLE_EDITING': {
            const { caseId } = action.payload;

            const newState = Object.assign({}, state, {
                cases: Object.assign({}, state['cases'], {
                    [caseId]: Object.assign({}, state['cases'][caseId], {
                        editing: !state['cases'][caseId].editing
                    })
                })
            });

            return newState;
        }

        case 'EDIT_SENTENCE_LENGTH': {
            const { sentenceId, field, value } = action.payload;

            const newState = Object.assign({}, state, {
                sentences: Object.assign({}, state['sentences'], {
                    [sentenceId]: Object.assign({}, state['sentences'][sentenceId], {
                        sentence_length: Object.assign({}, state['sentences'][sentenceId]['sentence_length'], {
                            [field]: value
                        })
                    })
                })
            });

            return newState;
        }

        case 'ADD_ENTITY': {
            const { entityName, entity, parentId, parentEntityName, parentListKey } = action.payload;

            const newState = Object.assign({}, state, {
                [entityName]: Object.assign({}, state[entityName], {
                    [entity.id]: entity
                }),
                [parentEntityName]: Object.assign({}, state[parentEntityName], {
                    [parentId]: Object.assign({}, state[parentEntityName][parentId], {
                        [parentListKey]: [...state[parentEntityName][parentId][parentListKey], entity.id]
                    })
                })
            });
            return newState;
        }

        default: {
            return state;
        }
    }
}

function serviceAgencyReducer(state={result: [], entities: {}}, action) {
    switch (action.type) {
        case 'NEW_SERVICE_AGENCY': 
            return(
                Object.assign(
                    {}, 
                    state, 
                    {
                        result: [...state.result, action.payload.id],
                        entities: Object.assign({}, state.entities, 
                            {
                                [action.payload.id]: {
                                    id: action.payload.id,
                                    name: action.payload.name,
                                }
                            })
                    })
            )

        case 'EDIT_SERVICE_AGENCY':
            return(
                Object.assign(
                    {},
                    state,
                    {
                        entities:  Object.assign({}, state.entities, 
                            {
                                [action.payload.id]: {
                                    id: action.payload.id,
                                    name: action.payload.name,
                                }
                            })

                    }
                )
            )

        case "DELETE_SERVICE_AGENCY":
            const callback = (acc, [k, v]) => Object.assign(acc, {[k]:v})
            const newEntities = Object.entries(state.entities)
                                .filter(([key]) => key !== action.payload.id)
                                .reduce(callback, {})
            
            return(
                Object.assign(
                    {},
                    state,
                    {
                        result: state.result.filter(s => s !== action.payload.id),
                        entities: newEntities,
                    }
                )
            )
        default:
            return(state)
    }
}


const rootReducer = combineReducers({
    user: userReducer,
    applicantInfo: applicantReducer,
    crecord: cRecordReducer,
    analysis: analysisReducer,
    attorney: attorneyReducer,
    petitionPackage: petitionsReducer,
    serviceAgencies: serviceAgencyReducer,
});

export default rootReducer

