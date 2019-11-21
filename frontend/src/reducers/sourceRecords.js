import { UPSERT_SOURCE_RECORDS } from "../actions/sourceRecords"

export const initialState = {allIds: [], allSourceRecords: {}}

export default function sourceRecordsReducer(state = initialState, action) {
    switch (action.type) {
        case UPSERT_SOURCE_RECORDS:
            const { source_records } = action.payload
            console.log("source_records:")
            console.log(source_records)
            const source_record_ids = source_records.map(sr => sr.id)
            return (Object.assign({}, state, {
                allIds: Array.from(new Set([...state.allIds, ...source_record_ids])),
                allSourceRecords: Object.assign({}, state.allSourceRecords, source_records.reduce((acc, sr) => {
                    acc[sr.id] = sr
                    return(acc)
                }, {}))
            }))
        default: 
            return state
    }
}