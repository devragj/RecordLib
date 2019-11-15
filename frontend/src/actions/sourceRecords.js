
/**
 * Actions for managing the store of source records.
 * 
 * Source records are documents that the user has registered with the server as records that
 * the user will include for processing the current session's petitions. 
 * 
 * For example, uploaded dockets get registered with the server, then returned with IDs that are 
 * stored here. Dockets found from a search of UJS are also returned to the user, and the ones the user
 * wants to use for generating petitions will get stored in this slice of the store.
 * 
 * All the documents in this slice will be sent to the server for inclusion in the final petitions package.
 */

export const UPSERT_SOURCE_RECORDS = "UPSERT_SOURCE_RECORDS"


export function upsertSourceRecords(source_records) {
    /**
     * Insert or update source records 
     */
        return({
                type: UPSERT_SOURCE_RECORDS,
                payload: source_records
        })
}