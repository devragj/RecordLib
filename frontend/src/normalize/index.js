/**
 * @file Normalizes data for use in a redux store
 *
 * The code in this file normalizes the data of a CRecord,
 * using the normalizr library.
 * The normalized data is flattened, which means that it can be
 * bound to components so that a component only rerenders if
 * its own data is changed.
 *
 * The normalized form of the data is as follows:
 * the entities key points to an object containing five entities,
 * cRecord, defendant, charges, cases, and sentences.
 * (Before normalization the data is preprocessed.
 * It is copied and each entity is given a unique id.)
 * If an entity contains another entity in the original data,
 * in the normalized data is contains the id of the child entity.
 * For example, a case contains a list of charges in the original data.
 * In the normalized data a case contains instead a list
 * of ids of charges.
 * This allows each wrapped charge component to retrieve
 * its own props from the store.
 * The case component will not rerender if a field is edited
 * in a child charge, becaues the case's data,
 * the list of charge ids, has not changed.
 */

import { normalize, denormalize, schema } from 'normalizr';

export const CRECORD_ID = "root";

/**
 * This gives each object in the normalized data a unique id.
 * @param  {Object} value  the object needing an id
 * @param  {Object} parent the object containing value
 * or containing the array which holds value
 * (or value itself if there is no containing object)
 * @param  {string | null} key    if present, the key for the field
 * within parent containing value (possibly as an item in an array)
 * @return {string}        the unique id
 */
const generateId = (value, parent, key) => {
    // Cases use their docket number as id.
    if (value.docket_number)
            return value.docket_number;
    // Defendants use their last name as id.
    if (value.last_name)
            return value.last_name;
    if (!key)
            return CRECORD_ID;

    // An object in an array starts with the parent's id,
    // then appends the key of the array containing the object
    // and then the object's index in the array.
    const index = parent[key].indexOf(value);
    return `${parent.id}${key}@${index}`
};

/**
 * options passed to normalizr
 * Note, we are computing the same id twice,
 * because of how normalizr works (I think),
 * since we don't want to mutate the original data.
 * See for example https://stackoverflow.com/questions/39681284/normalizr-how-to-generate-slug-id-related-to-parent-entity
 * @type {Object}
 */
const options = {
    // copy an entity and add an id
    processStrategy: (value, parent, key) => {
            return Object.assign({}, value, {
                    id: generateId(value, parent, key)
            });
    },
    idAttribute: (value, parent, key) => {
            return generateId(value, parent, key);
    }
};

// Schema for the normalized CRecord.
const sentenceSchema = new schema.Entity('sentences', {} ,options);
const chargeSchema = new schema.Entity('charges', {sentences: [sentenceSchema]}, options);
const caseSchema = new schema.Entity('cases', {charges: [chargeSchema]},  options);
const defendantSchema = new schema.Entity('defendant', {}, options);
const cRecordSchema = new schema.Entity('cRecord', { defendant: defendantSchema, cases: [caseSchema]}, options);

export function normalizeCRecord(data) {
        return normalize(data,  cRecordSchema);
}

export function denormalizeCRecord(entities) {
        return denormalize(entities.cRecord, cRecordSchema, {})
}