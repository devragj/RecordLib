import * as api from '../api';
import { normalizeCRecord } from '../normalize';

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
        console.log(cRecord);
        const state = normalizeCRecord(cRecord);
        state['analysis'] = cRecord.analysis.analysis;
        console.log(state);
        return {
                type: 'FETCH_CRECORD_SUCCEEDED',
                payload: state
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