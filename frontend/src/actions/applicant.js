import { generateId } from "./helpers"

export const ADD_OR_REPLACE_APPLICANT = "ADD_OR_REPLACE_APPLICANT"
export const EDIT_APPLICANT = "EDIT_APPLICANT"

export const ADD_ALIAS = "ADD_ALIAS"
export const EDIT_ALIAS = "EDIT_ALIAS"


export function addOrReplaceApplicant(applicant) {
    return {
        type: ADD_OR_REPLACE_APPLICANT,
        payload: applicant
    }
}

export function editApplicant(field, value) {
        return {
                type: EDIT_APPLICANT,
                payload: { field, value }
        };
};

export function editAlias(id, value) {
        return {
                type: EDIT_ALIAS,
                payload: { id, value }
        };
};

export function addAlias(value) {
    const id = generateId();
    return {
        type: ADD_ALIAS,
        payload: { id, value }
    };
};