import * as api from "../api"
import { upsertSourceRecords } from "./sourceRecords"
import { updateCRecord } from "./crecord"
/**
 * Actions related to accessing ujs-related api endpoints. 
 * 
 * (UJS is the public website of the PA criminal courts)
 */
export const SEARCH_UJS_BY_NAME_STATUS = "SEARCH_UJS_BY_NAME_STATUS"
export const SEARCH_UJS_BY_NAME_SUCCESS = "SEARCH_UJS_BY_NAME_SUCCESS"
export const UPLOAD_UJS_DOCS_PENDING = "UPLOAD_UJS_DOCS_PENDING"
export const UPLOAD_UJS_DOCS_FINISHED = "UPLOAD_UJS_DOCS_FINISHED"
export const TOGGLE_UJS_SELECTED_SEARCH_CASES = "TOGGLE_UJS_SELECTED_SEARCH_CASES"


function searchUSJByNameStatus(newStatus) {
        return({
                type: SEARCH_UJS_BY_NAME_STATUS,
                payload: newStatus,
        })
}

function searchUSJByNameSuccess({ searchResults }) {
        return({
                type: SEARCH_UJS_BY_NAME_SUCCESS,
                payload: searchResults
        })
}


export function searchUJSByName(first_name, last_name, date_of_birth) {
        return(dispatch => {
                dispatch(searchUSJByNameStatus("Started"))
                api.searchUJSByName(first_name, last_name, date_of_birth).then(response => {
                        const data = response.data
                        console.log("recieved docket search results")
                        if (data.errors) {
                                console.log("error with search")
                                dispatch(searchUSJByNameStatus("error"))
                        } else {
                                dispatch(searchUSJByNameSuccess(data))
                                dispatch(searchUSJByNameStatus("Success"))
                        }
                }).catch(err => {
                        console.log("Searching ujs by name failed.")
                        console.log(err)
                })
        })
}


export function toggleSelectedUJSSearchCases(docType, docNum, newValue=null) {
        /**
         * docType: either summary or docket
         * docNum: the number of the docket.
         */
        return({
                type: TOGGLE_UJS_SELECTED_SEARCH_CASES,
                payload: {docType, docNum, newValue}
        })
}

function uploadUJSDocsPending() {
        return({
                type: UPLOAD_UJS_DOCS_PENDING
        })
}

function uploadUJSDocsFinished() {
        return({
                type: UPLOAD_UJS_DOCS_FINISHED
        })
}



export function uploadUJSDocs() {
        /**
         * send the selected documents to the server, 
         * 
         * We'll receive objects that will get added to the SourceRecords store. 
         * 
         * Then we'll also send the action to update the current crecord with the server and the 
         * current set of sourcerecords. 
         * 
         * cases.result: a list of docket numbers
         * cases.entities: a object. keys are docket numbers, and values are info about 
         *      a case, including docket number, summary and docket urls, and whether those 
         *      things are selected.
         */
        

        return((dispatch, getState) => {
                dispatch(uploadUJSDocsPending())
                const cases = getState().ujsSearchResults.casesFound
                const docketsToSend = cases.result.map(cId => {
                        const c = cases.entities[cId]
                        if (c.docketSelected) {
                                return {
                                        caption: c.caption,
                                        docket_num: c.docket_number,
                                        court: c.court,
                                        url: c.docket_sheet_url,
                                        record_type: "DOCKET_PDF"
                                }
                        } else {
                                return null
                        }
                }).filter(i => i !== null)
                const summariesToSend = cases.result.map(cId => {
                        const c = cases.entities[cId]
                        if (c.summarySelected) {
                                return {
                                        caption: c.caption,
                                        docket_num: c.docket_number,
                                        court: c.court,
                                        url: c.summary_sheet_url,
                                        record_type: "SUMMARY_PDF"
                                }
                        } else {
                                return null
                        }
                }).filter(i => i !== null)
                const recordsToSend = docketsToSend.concat(summariesToSend)
                api.uploadUJSDocs(recordsToSend).then(response => {
                        const data = response.data
                        dispatch(uploadUJSDocsFinished())
                        console.log("server responded with source records:")
                        console.log(data)
                        dispatch(upsertSourceRecords(data))
                        dispatch(updateCRecord())
                }).catch(err => {
                        console.log("error when integrating docs.")
                        console.log(err)
                        dispatch(uploadUJSDocsFinished())
                })
        })
}       

