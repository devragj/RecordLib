import * as api from '../api';
import { normalizeCRecord, CRECORD_ID } from '../normalize';

/**
 * This action creator parses and then normalizes
 * the data returned by the backend.
 * @param  {string} data JSON for a CRecord
 * @return {Object} an action whose payload is
 * the normalized form of the CRecord, to be used as
 * redux state
 */
function fetchCRecordSucceeded(data) {
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
export function fetchCRecord(file) {
        return dispatch => {
                api.fetchCRecord(file)
                .then(
                        response => {
                                const data = response.data;
                                console.log("fetched data successfully")
                                console.log(data)
                                const action = fetchCRecordSucceeded(data);
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

export function addCase(docket_number) {
    const newCase = {
        id: docket_number,
        docket_number,
        status: '',
        county: '',
        otn: '',
        dc: '',
        charges: [],
        total_fines: '',
        fines_paid: '',
        complaint_date: '',
        arrest_date: '',
        disposition_date: '',
        judge: '',
        judge_address: '',
        affiant: '',
        arresting_agency: '',
        arresting_agency_address: ''
    };

    return {
        type: 'ADD_ENTITY',
        payload: { entityName: 'cases', entity: newCase, parentId: CRECORD_ID,  parentEntityName: 'cRecord', parentListKey: 'cases' }
    };
};

export function addCharge(chargeId, caseId) {
    const newCharge = {
        id: chargeId,
        offense: '',
        grade: '',
        statute: '',
        disposition: '',
        disposition_date: '',
        sentences: []
    };

    return {
        type: 'ADD_ENTITY',
        payload: { entityName: 'charges', entity: newCharge, parentId: caseId,  parentEntityName: 'cases', parentListKey: 'charges' }
    };
};

export function addSentence(sentenceId, chargeId) {
    const SentenceLength = {
        min_time: '',
        max_time: ''
    };
    const newSentence = {
        id: sentenceId,
        sentence_date: '',
        sentence_type: '',
        sentence_period: '',
        sentence_length: SentenceLength
    };

    return {
        type: 'ADD_ENTITY',
        payload: { entityName: 'sentences', entity: newSentence, parentId: chargeId,  parentEntityName: 'charges', parentListKey: 'sentences' }
    };
};