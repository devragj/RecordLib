/*
        For developing without using the backend server,
        uncomment the code in the comment block below.
        Also, replace the first line of the function below it with

        export default function cRecordReducer(state = normalizedData, action) {
 */

/*
import { normalizeCRecord } from '../normalize';

const cRecordString = '{"defendant": {"first_name": "Garrett Paul", "last_name": "Gallagher", "date_of_birth": "1981-07-29", "date_of_death": null}, "cases": [{"docket_number": "CP-07-MD-0000230-2010", "otn": "S0132834", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "", "sentences": []}], "fines_and_costs": null, "status": "Active", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-MD-0001421-2013", "otn": "", "charges": [], "fines_and_costs": null, "status": "Active", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-MD-0000050-2014", "otn": "", "charges": [], "fines_and_costs": null, "status": "Active", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-CR-0001027-2009", "otn": "K8928065", "charges": [{"offense": "Simple Assault", "grade": "M2", "statute": "18 \u00a7 2701 \u00a7\u00a7 A1", "disposition": "Nolle Prossed", "sentences": []}, {"offense": "Simple Assault", "grade": "M2", "statute": "18 \u00a7 2701 \u00a7\u00a7 A3", "disposition": "Nolle Prossed", "sentences": []}, {"offense": "Harassment - Subject Other to", "grade": "S", "statute": "18 \u00a7 2709 \u00a7\u00a7 A1", "disposition": "Guilty Plea", "sentences": [{"sentence_date": "2009-09-18", "sentence_type": "No Further Penalty", "sentence_period": "", "sentence_length": {"min_time": "0:00:00", "max_time": "0:00:00"}}]}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-CR-0001763-2012", "otn": "T2121066", "charges": [{"offense": "Theft By Unlaw Taking-Movable Prop", "grade": "M1", "statute": "18 \u00a7 3921 \u00a7\u00a7 A", "disposition": "Guilty Plea", "sentences": [{"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": "1825 days, 0:00:00", "max_time": "1825 days, 0:00:00"}}, {"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": "1825 days, 0:00:00", "max_time": "1825 days, 0:00:00"}}]}, {"offense": "Receiving Stolen Property", "grade": "F3", "statute": "18 \u00a7 3925 \u00a7\u00a7 A", "disposition": "Nolle Prossed", "sentences": []}, {"offense": "Criminal Mischief - Damage Property", "grade": "M3", "statute": "18 \u00a7 3304 \u00a7\u00a7 A5", "disposition": "Guilty Plea", "sentences": [{"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": "365 days, 0:00:00", "max_time": "365 days, 0:00:00"}}, {"sentence_date": "2013-01-25", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": "365 days, 0:00:00", "max_time": "365 days, 0:00:00"}}]}, {"offense": "Theft By Unlaw Taking-Movable Prop", "grade": "F3", "statute": "18 \u00a7 3921 \u00a7\u00a7 A", "disposition": "Nolle Prossed", "sentences": []}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-CR-0001099-2015", "otn": "T6314722", "charges": [{"offense": "Endangering Welfare of Children -", "grade": "M1", "statute": "18 \u00a7 4304 \u00a7\u00a7 A1", "disposition": "Guilty Plea", "sentences": [{"sentence_date": "2016-01-08", "sentence_type": "Probation", "sentence_period": "Other", "sentence_length": {"min_time": "1825 days, 0:00:00", "max_time": "1825 days, 0:00:00"}}]}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-MD-0002038-2009", "otn": "", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "Found in Contempt", "sentences": []}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-MD-0000072-2010", "otn": "", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "", "sentences": []}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-07-MD-0000153-2013", "otn": "Z0000000", "charges": [{"offense": "Contempt For Violation of Order or", "grade": "IC", "statute": "23 \u00a7 6114 \u00a7\u00a7 A", "disposition": "Nolle Prossed", "sentences": []}], "fines_and_costs": null, "status": "Closed", "county": "Blair", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}, {"docket_number": "CP-11-CR-0001031-2000", "otn": "H0954343", "charges": [{"offense": "Resist Arrest/Other Law Enforce", "grade": "M2", "statute": "18 \u00a7 5104", "disposition": "", "sentences": []}, {"offense": "Harassment/Repeatedly Alarm,", "grade": "S", "statute": "18 \u00a7 2709 \u00a7\u00a7 A3", "disposition": "", "sentences": []}], "fines_and_costs": null, "status": "Closed", "county": "Cambria", "arrest_date": null, "disposition_date": null, "judge": "", "dc": ""}]}';
const cRecord = JSON.parse(data);
const normalizedData = normalizeCRecord(cRecord);
*/

/**
 * Redux reducer
 * @param  {Object} [state={}] holds normailzed data from a CRecord
 * @param  {Object} action
 * @param  {string} action.type
 * @param  {Object} action.payload - We're following the convention that
 * all other information in the action is stored in an object
 * named payload.
 * @return {Object}  the new state
 */
export default function cRecordReducer(state = {}, action) {
        switch (action.type) {
                case 'FETCH_CRECORD_SUCCEEDED': {
                        return action.payload;
                }

                // generic action to edit a field of any of the
                // entities stored in state
                // Currently, this makes shallow copies so as to edit
                // the field while keeping state immutable.
                // TODO: replace this with a library such as immutable.js
                case'EDIT': {
                        const { entityName, entityId, field, value } = action.payload;
                        const newState = {...state};
                        newState.entities = {...(newState.entities)};
                        newState.entities[entityName] = {...(newState.entities[entityName])};
                        const entityToChange = newState.entities[entityName][entityId];
                        const newEntity = {...entityToChange};
                        newEntity[field] = value;
                        newState.entities[entityName][entityId] = newEntity;
                        return newState;
                }

                default: {
                        return state;
                }
        }
}