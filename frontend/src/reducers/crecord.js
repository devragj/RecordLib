
import { CRECORD_ID } from "../normalize";
import { UPDATE_CRECORD_SUCCEEDED } from "../actions/crecord"

export const initialCrecordState = {
    charges: {},
    cases: {},
    sentences: {},
    cRecord: { [CRECORD_ID]: { cases:[] } }
};

export default function cRecordReducer(state = initialCrecordState, action) {
    switch (action.type) {
        case UPDATE_CRECORD_SUCCEEDED: {
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

