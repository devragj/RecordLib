import React from "react";
import { connect } from 'react-redux';

import Charge from "./Charge";
import EditCharge from "./EditCharge";
import { editField } from "../actions";

/**
 * Connected component for a Charge, which can be in edit mode.
 * The editing prop determines the mode, and is passed in from the parent case.
 * Props which are properties of the charge are passed to a child
 * presentational component, which is either Charge or EditCharge.
 * These components also receive a dispatching function, which is used by the
 * EditCharge component to send changes to the redux store.
 */
function ChargeHolder(props) {
    return (
        <div className="chargeHolder" >
            { !props.editing?
                <Charge {...props} />
                : <EditCharge {...props} />
            }
        </div>
    );
};

function mapStateToProps(state, ownProps) {
    return state.crecord.entities.charges[ownProps.chargeId];
};

/**
 * The modifier function takes a key,value pair
 * and associates the value with that key in the Charge
 * object being edited.  It is used by the EditCharge component.
 */
function mapDispatchToProps(dispatch, ownProps) {
    return {
        modifier: (key, value) => {
            dispatch(editField('charges', ownProps.chargeId, key, value))
        }
    };
};

const ChargeHolderWrapper = connect(mapStateToProps, mapDispatchToProps)(ChargeHolder);
export default ChargeHolderWrapper;