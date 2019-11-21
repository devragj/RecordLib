import * as api from "../api"
import { normalizeCRecord, denormalizeCRecord, CRECORD_ID, normalizeAnalysis, denormalizeSourceRecords } from "../normalize"
import { addOrReplaceApplicant } from "./applicant"

export const UPDATE_CRECORD = "UPDATE_CRECORD"
export const UPDATE_CRECORD_SUCCEEDED = "UPDATE_CRECORD_SUCCEEDED"
export const FETCH_CRECORD_SUCCEEDED = "FETCH_CRECORD_SUCCEEDED"
export const ANALYZE_CRECORD_SUCCEDED = "ANALYZE_CRECORD_SUCCEDED"





function analyzeRecordsSucceeded(data) {
        // TODO - do we need to normalize 'data' here? Its an analysis from the server, so its pretty deeply 
        // nested. But we won't edit it, I think.
        const normalizedAnalysis = normalizeAnalysis(data)
        return {
                type: 'ANALYZE_CRECORD_SUCCEEDED',
                payload: normalizedAnalysis 
        }
}

/**
 * Create an action to send the CRecord to the server and receive an analysis of petitions that can be generated from this analysis, 
 */
export function analyzeCRecord() {
        return (dispatch, getState) => {
                const crecord = getState().crecord;
                const normalizedData = { entities: crecord, result: CRECORD_ID };
                const denormalizedCRecord = denormalizeCRecord(normalizedData);
                const applicantInfo = getState().applicantInfo;
                const person = Object.assign({}, applicantInfo.applicant, {
                    aliases: applicantInfo.applicant.aliases.map(aliasId => applicantInfo.aliases[aliasId])
                });
                delete person.editing;
                if (person.date_of_death === '') {
                    delete person.date_of_death;
                }
                denormalizedCRecord['person'] = person;
                api.analyzeCRecord(denormalizedCRecord).then(
                        response => {
                                const data = response.data;
                                console.log("fetched data successfully")
                                console.log(data)
                                const action = analyzeRecordsSucceeded(data);
                                dispatch(action);
                        }).catch(err => { 
                                console.log("error analyzing record:"); 
                                console.log(err)
                        })
        }
}



/**
 * 
 * N.B. this action will trigger two reducers - one to update the crecord object that stores cases and charges, and one to update the 'applicant' slice.
 * @param {*} newCRecord 
 */

function updateCRecordSucceeded(newCRecord) {
    console.log("in updateCREcordSucceeded")
    console.log("crecord param is")
    console.log(newCRecord)
    return {
        type: UPDATE_CRECORD_SUCCEEDED,
        payload: normalizeCRecord(newCRecord) 
    }
}

export function updateCRecord() {
    /**
     * Send the CRecord and SourceRecords to the server. the server will analyze the sourceRecord and integrate them into the 
     * CRecord, and return a new crecord.
     */
    return ((dispatch, getState) => {
        const crecord = getState().crecord;
        const sourceRecords = denormalizeSourceRecords(getState().sourceRecords);
        const normalizedData = { entities: crecord, result: CRECORD_ID };
        const denormalizedCRecord = denormalizeCRecord(normalizedData);
        const applicantInfo = getState().applicantInfo;
        const person = Object.assign({}, applicantInfo.applicant, {
            aliases: applicantInfo.applicant.aliases.map(aliasId => applicantInfo.aliases[aliasId])
        });
        delete person.editing;
        if (person.date_of_death === '') {
            delete person.date_of_death;
        }
        if (person.date_of_birth === '') {
            delete person.date_of_birth;
        } 
        denormalizedCRecord['person'] = person;


        api.integrateDocsWithRecord(denormalizedCRecord, sourceRecords).then(response => {
            console.log("response of crecord from server")
            console.log(response.data)
            dispatch(updateCRecordSucceeded(response.data.crecord))
            dispatch(addOrReplaceApplicant(response.data.crecord.person))
        }).catch(err => {
            console.log("error sending crecord and sourcerecords to server.")
            console.log(err)
        })
    })
}
