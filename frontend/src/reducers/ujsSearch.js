import { combineReducers } from "redux"
import {
    SEARCH_UJS_BY_NAME_STATUS, SEARCH_UJS_BY_NAME_SUCCESS, UPLOAD_UJS_DOCS_PENDING, UPLOAD_UJS_DOCS_FINISHED, 
    TOGGLE_UJS_SELECTED_SEARCH_CASES,
} from "../actions/ujs"


function ujsSearchStatusReducer(state = null, action) {
    switch (action.type) {
        case SEARCH_UJS_BY_NAME_STATUS:
            return action.payload
            
        default:
            return state
    }
}


function ujsCasesFoundReducer(state={result: [], entities: {}}, action) {
    switch (action.type) {
        case SEARCH_UJS_BY_NAME_SUCCESS:
            const mdjDockets = action.payload.MDJ.dockets.map(d => {
                d["court"] = "MDJ"
                d["docketSelected"] = true
                d["summarySelected"] = false
                return(d)
            })
            const cpDockets = action.payload.CP.dockets.map(d => {
                d["court"] = "CP"
                d["docketSelected"] = true
                d["summarySelected"] = false
                return(d)
            })
            const allDockets = [...mdjDockets, ...cpDockets]
            const newResult = allDockets.map(d => d.docket_number)
            const newEntities = allDockets.reduce((obj, item) => {
                    obj[item.docket_number] = item
                    return(obj)
                }, {})
            return(Object.assign({}, state, {
                result: newResult,
                entities: newEntities
            }))
        case TOGGLE_UJS_SELECTED_SEARCH_CASES:
            const {docType, docNum, newValue } = action.payload
            var keyField = ""
            if (docType.toLowerCase() === "summary") {
                keyField = "summarySelected"
            } else {
                keyField = "docketSelected"
            }
            const newState = Object.assign({}, state, {
                result: state.result,
                entities: Object.assign({}, state.entities, {
                    [docNum]: Object.assign({}, state.entities[docNum], {
                        [keyField] : newValue !== null ? newValue : !state.entities[docNum][keyField]
                    })
                })
            })
            return newState
        default: 
            return state
    }
}

function uploadUJSDocsReducer(state = {pending: false}, action) {
    switch (action.type) {
        case UPLOAD_UJS_DOCS_PENDING:
            return Object.assign({}, state, {
                pending: true
            })
        case UPLOAD_UJS_DOCS_FINISHED:
            return Object.assign({}, state, {
                pending: false
            })
        default:
            return state
    }
}

const ujsSearchReducer = combineReducers({
        status: ujsSearchStatusReducer,
        casesFound: ujsCasesFoundReducer,
        uploadUJSDocs: uploadUJSDocsReducer,
})

export default ujsSearchReducer;


