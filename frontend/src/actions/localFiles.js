import { upsertSourceRecords } from "./sourceRecords";
import { updateCRecord } from "./crecord";
import * as api from "../api"
/**
 * Actions related to uploading local files and getting back SourceRecords.
 */

/**
 * This action creator parses and then normalizes
 * the data returned by the backend.
 * @param  {string} data JSON for a CRecord
 * @return {Object} an action whose payload is
 * the normalized form of the CRecord, to be used as
 * redux state
 */
//function uploadRecordsSucceeded(data) {
//    return {
//        type: 'FETCH_CRECORD_SUCCEEDED',
//        payload: data
//    }
//}


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
                    dispatch(upsertSourceRecords(data))
                    dispatch(updateCRecord())
                    // Wrong - the response will be source records. 
                    // const cRecord = JSON.parse(data);
                    // const defendant = cRecord.defendant;
                    // delete cRecord.defendant;
                    // const normalizedData = normalizeCRecord(cRecord);
                    // const action = uploadRecordsSucceeded(normalizedData));
                    // dispatch(action);
                    // const action2 = addDefendant(defendant);
                    // dispatch(action2);
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

