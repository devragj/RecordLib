import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import Charge from "./Charge";
import EditCharge from "./EditCharge";
import { editField } from "../actions";

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
    return state.entities.charges[ownProps.chargeId];
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