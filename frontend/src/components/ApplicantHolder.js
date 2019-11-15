import React from "react";
import { connect } from 'react-redux';

import Applicant from "./Applicant";
import EditApplicant from "./EditApplicant";
import { editApplicant } from "../actions/applicant";

/**
 * Connected component for a Applicant, which can be in edit mode.
 * The editing prop determines the mode.
 * Props which are properties of the applicant are passed to a child
 * presentational component, which is either Applicant or EditApplicant.
 * Theses components also receive a dispatching function, which is used by the
 * EditApplicant component to send changes to the redux store.
 */
function ApplicantHolder(props) {
    return (
        <div className="applicantHolder" >
            { !props.editing?
                <Applicant {...props} />
                : <EditApplicant {...props} />
            }
        </div>
    );
};

function mapStateToProps(state) {
    return state.applicantInfo.applicant;
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Applicant
 * object being edited.  It is used by the EditApplicant component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (key, value) => {
            dispatch(editApplicant(key, value))
        }
    };
};

const ApplicantHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(ApplicantHolder);
export default ApplicantHolderWrapper;