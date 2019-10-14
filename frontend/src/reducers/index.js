/*
        For developing without using the backend server,
        uncomment the code in the comment block below.
        Also, replace the first line of the function below it with

        export default function cRecordReducer(state = normalizedData, action) {
 */


//import { normalizeCRecord } from '../normalize';
//
//const cRecordString = '{"defendant": {"first_name": "Garrett Paul", "last_name": "Gallagher", "date_of_birth": "1981-07-29", "aliases": ["Garrett Gallagher", "Garrett P. Gallagher", "Garrett Paul Gallagher", "Garrett Paul Gallagher", "Paul Gallagher Garrett"]}, "cases": [{"docket_number": "CP-07-MD-0000230-2010", "otn": "S0132834", "dc": "", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "", "sentences": []}], "status": "Active", "county": "Blair", "arrest_date": "2010-02-27", "judge": ""}, {"docket_number": "CP-07-MD-0001421-2013", "otn": "", "dc": "", "charges": [], "status": "Active", "county": "Blair", "judge": ""}, {"docket_number": "CP-07-MD-0000050-2014", "otn": "", "dc": "", "charges": [], "status": "Active", "county": "Blair", "judge": ""}, {"docket_number": "CP-07-CR-0001027-2009", "otn": "K8928065", "dc": "", "charges": [{"offense": "Simple Assault", "grade": "M2", "statute": "18 \u00a7 2701 \u00a7\u00a7 A1", "disposition": "Nolle Prossed", "disposition_date": "2009-09-18", "sentences": []}, {"offense": "Simple Assault", "grade": "M2", "statute": "18 \u00a7 2701 \u00a7\u00a7 A3", "disposition": "Nolle Prossed", "disposition_date": "2009-09-18", "sentences": []}, {"offense": "Harassment - Subject Other to", "grade": "S", "statute": "18 \u00a7 2709 \u00a7\u00a7 A1", "disposition": "Guilty Plea", "disposition_date": "2009-09-18", "sentences": [{"sentence_date": "2009-09-18", "sentence_type": "No Further Penalty", "sentence_period": "", "sentence_length": {"min_time": 0, "min_unit": "days", "max_time": 0, "max_unit": "days"}}]}], "status": "Closed", "county": "Blair", "arrest_date": "2009-04-10", "disposition_date": "2009-09-18", "judge": "Milliron, Daniel J."}, {"docket_number": "CP-07-CR-0001763-2012", "otn": "T2121066", "dc": "", "charges": [{"offense": "Theft By Unlaw Taking-Movable Prop", "grade": "M1", "statute": "18 \u00a7 3921 \u00a7\u00a7 A", "disposition": "Guilty Plea", "disposition_date": "2013-01-07", "sentences": [{"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": 1825, "min_unit": "days", "max_time": 1825, "max_unit": "days"}}, {"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": 1825, "min_unit": "days", "max_time": 1825, "max_unit": "days"}}]}, {"offense": "Receiving Stolen Property", "grade": "F3", "statute": "18 \u00a7 3925 \u00a7\u00a7 A", "disposition": "Nolle Prossed", "disposition_date": "2013-01-07", "sentences": []}, {"offense": "Criminal Mischief - Damage Property", "grade": "M3", "statute": "18 \u00a7 3304 \u00a7\u00a7 A5", "disposition": "Guilty Plea", "disposition_date": "2013-01-07", "sentences": [{"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": 365, "min_unit": "days", "max_time": 365, "max_unit": "days"}}, {"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": 365, "min_unit": "days", "max_time": 365, "max_unit": "days"}}]}, {"offense": "Theft By Unlaw Taking-Movable Prop", "grade": "F3", "statute": "18 \u00a7 3921 \u00a7\u00a7 A", "disposition": "Nolle Prossed", "disposition_date": "2013-01-07", "sentences": []}], "status": "Closed", "county": "Blair", "disposition_date": "2013-01-07", "judge": "Doyle, Elizabeth"}, {"docket_number": "CP-07-CR-0001099-2015", "otn": "T6314722", "dc": "", "charges": [{"offense": "Endangering Welfare of Children -", "grade": "M1", "statute": "18 \u00a7 4304 \u00a7\u00a7 A1", "disposition": "Guilty Plea", "disposition_date": "2015-10-02", "sentences": [{"sentence_date": "2016-01-08", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": 1825, "min_unit": "days", "max_time": 1825, "max_unit": "days"}}]}], "status": "Closed", "county": "Blair", "disposition_date": "2015-10-02", "judge": "Kopriva, Jolene Grubb"}, {"docket_number": "CP-07-MD-0002038-2009", "otn": "", "dc": "", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "Found in Contempt", "disposition_date": "2010-01-14", "sentences": []}], "status": "Closed", "county": "Blair", "disposition_date": "2010-01-14", "judge": "Carpenter, Hiram A. III"}, {"docket_number": "CP-07-MD-0000072-2010", "otn": "", "dc": "", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "", "sentences": []}], "status": "Closed", "county": "Blair", "judge": ""}, {"docket_number": "CP-11-CR-0001031-2000", "otn": "H0954343", "dc": "", "charges": [{"offense": "Resist Arrest/Other Law Enforce", "grade": "M2", "statute": "18 \u00a7 5104", "disposition": "", "sentences": []}, {"offense": "Harassment/Repeatedly Alarm,", "grade": "S", "statute": "18 \u00a7 2709 \u00a7\u00a7 A3", "disposition": "", "sentences": []}], "status": "Closed", "county": "Cambria", "arrest_date": "2000-03-31", "judge": ""}]}';
//const cRecord = JSON.parse(cRecordString);
//const normalizedData = normalizeCRecord(cRecord);


/**
 * Redux reducer
 * @param  {Object} [state={}] holds normalized data from a CRecord
 * @param  {Object} action
 * @param  {string} action.type
 * @param  {Object} action.payload - We're following the convention that
 * all other information in the action is stored in an object
 * named payload.
 * @return {Object}  the new state
 */


import { combineReducers } from 'redux';

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
            return Object.assign({}, state, {path: action.payload.download});
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

function cRecordReducer(state = {}, action) {
    switch (action.type) {
        case 'FETCH_CRECORD_SUCCEEDED': {
                return action.payload;
        }

        // Generic action to edit a field of any of the entities stored in state.
        // This case makes shallow copies so as to edit
        // the field while keeping state immutable.
        // TODO: consider using a library such as immutable.js for this and the next three cases.
        case 'EDIT_ENTITY_VALUE': {
            const { entityName, entityId, field, value } = action.payload;

            const newState = Object.assign({},state, {
                entities: Object.assign({}, state.entities, {
                   [entityName]: Object.assign({}, state.entities[entityName], {
                        [entityId]: Object.assign({}, state.entities[entityName][entityId], {
                            [field]: value
                        })
                    })
                })
            });

            return newState;
        }

        case 'TOGGLE_EDITING': {
            const { caseId } = action.payload;

            const newState = Object.assign({},state, {
                entities: Object.assign({}, state.entities, {
                   cases: Object.assign({}, state.entities['cases'], {
                        [caseId]: Object.assign({}, state.entities['cases'][caseId], {
                            editing: !state.entities['cases'][caseId].editing
                        })
                    })
                })
            });

            return newState;
        }

        case 'EDIT_SENTENCE_LENGTH': {
            const { sentenceId, field, value } = action.payload;

            const newState = Object.assign({},state, {
                entities: Object.assign({}, state.entities, {
                    sentences: Object.assign({}, state.entities['sentences'], {
                        [sentenceId]: Object.assign({}, state.entities['sentences'][sentenceId], {
                            sentence_length: Object.assign({}, state.entities['sentences'][sentenceId]['sentence_length'], {
                                [field]: value
                            })
                        })
                    })
                })
            });

            return newState;
        }

        case 'ADD_ENTITY': {
            const { entityName, entity, parentId, parentEntityName, parentListKey } = action.payload;

            const newState = Object.assign({},state, {
                entities: Object.assign({}, state.entities, {
                    [entityName]: Object.assign({}, state.entities[entityName], {
                        [entity.id]: entity
                    }),
                    [parentEntityName]: Object.assign({}, state.entities[parentEntityName], {
                        [parentId]: Object.assign({}, state.entities[parentEntityName][parentId], {
                            [parentListKey]: [...state.entities[parentEntityName][parentId][parentListKey], entity.id]
                        })
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
    crecord: cRecordReducer,
    analysis: analysisReducer,
    attorney: attorneyReducer,
    petitionPackage: petitionsReducer,
    serviceAgencies: serviceAgencyReducer,
});

export default rootReducer

