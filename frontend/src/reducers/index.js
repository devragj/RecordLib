import { combineReducers } from 'redux';

import sourceRecordsReducer from "./sourceRecords"
import ujsSearchReducer from "./ujsSearch"
import serviceAgencyReducer from "./serviceAgencies"
import cRecordReducer from "./crecord"
import attorneyReducer from "./attorney"
import userReducer from "./user"
import applicantReducer from "./applicant"
import analysisReducer from "./analysis"
import petitionsReducer from "./petitions"

const rootReducer = combineReducers({
    user: userReducer,  // the current user.
    applicantInfo: applicantReducer, // the subject of petitions to be generated. 
    crecord: cRecordReducer, // a representation of a person's criminal record.
    analysis: analysisReducer, // the server's analysis of what petitions may be generated, and why
    sourceRecords: sourceRecordsReducer, // records the user has told the server they want to use for this session.
    attorney: attorneyReducer, // attorney information is entered into generated petitions.
    petitionPackage: petitionsReducer,
    serviceAgencies: serviceAgencyReducer, // petitions can include a list of agencies that will receive service
    ujsSearchResults: ujsSearchReducer, //  results from searching the public ujs portal.
});

export default rootReducer

