import * as api from '../api';
import { normalizeCRecord, denormalizeCRecord } from '../normalize';

/**
 * This action creator parses and then normalizes
 * the data returned by the backend.
 * @param  {string} data JSON for a CRecord
 * @return {Object} an action whose payload is
 * the normalized form of the CRecord, to be used as
 * redux state
 */
function uploadRecordsSucceeded(data) {
        const cRecord = JSON.parse(data);
        const normalizedData = normalizeCRecord(cRecord);
        return {
                type: 'FETCH_CRECORD_SUCCEEDED',
                payload: normalizedData
        }
}

/**
 * An async action creator returning a function (of dispatch).
 * @param  {Object} file - uploaded Summary pdf file
 * @return {Object}
 */
export function uploadRecords(files) {
        return dispatch => {
                api.uploadRecords(files)
                        .then(
                                response => {
                                        const data = response.data;
                                        console.log("fetched data successfully")
                                        console.log(data)
                                        const action = uploadRecordsSucceeded(data);
                                        dispatch(action);
                                }
                        )
                // TODO Find out what errors we may get from the server
                // and dispatch an action so that the UI can notify the user.
                // For now, while the app is under development, I have
                // commented this block out,
                // as axios will catch other errors as well.
                // See https://github.com/facebook/react/issues/7617#issuecomment-247710003
                // If you uncomment the catch block, make sure to check
                // the console for errors.
                // Alternatively, we could install axios middleware.
                // .catch(
                //         error => {
                //                 console.log(error);
                //         }
                // );
        };
};

/**
 * a generic action creator for editing a field of
 * an entity in the store
 * @param  {string} entityName the key for this type of entity
 * in the store
 * @param  {string} entityId   the id of the specific entity
 * being edited
 * @param  {string} field      the key of the field being edited
 * @param  {string} value      the new value for the field
 * @return {Object}            an action whose payload holds
 * all the above values
 */
export function editField(entityName, entityId, field, value) {
        return {
                type: 'EDIT',
                payload: { entityName, entityId, field, value }
        };
};


function analyzeRecordsSucceeded(data) {
        // TODO - do we need to normalize 'data' here? Its an analysis from the server, so its pretty deeply 
        // nested. But we won't edit it, I think.
        return {
                type: 'ANALYZE_CRECORD_SUCCEEDED',
                payload: data 
        }
}

/**
 * Create an action to start the call to analyze a crecord to get an analysis of expungements and petitions
 */
export function analyzeCRecord() {
        return (dispatch, getState) => {
                const denormalizedCRecord = denormalizeCRecord(getState().crecord)
                console.log("denormalized crecord")
                console.log(denormalizedCRecord)
                api.analyzeCRecord(denormalizedCRecord).then(
                        response => {
                                const data = response.data;
                                console.log("fetched data successfully")
                                console.log(data)
                                const action = analyzeRecordsSucceeded(data);
                                dispatch(action);
                        }).catch(err => { console.log("error analyzing record.")})
        }
}

function fetchPetitionsSucceeded(petitionPath) {
        return {
                type: 'FETCH_PETITIONS_SUCCEEDED',
                payload: petitionPath
        }
}

/**
 * Create an action that sends a list of petitions to the server, and returns the files.
 * @param {} petitions 
 */
export function getPetitions(petitions) {
        return (dispatch, getState) => {
                api.fetchPetitions(petitions).then(
                        response => {
                                const data = response.data;
                                console.log("fetched petitions successfully")
                                dispatch( fetchPetitionsSucceeded(data) )
                        }).catch(err => console.log("error fetching petitions."))
                }
        
}