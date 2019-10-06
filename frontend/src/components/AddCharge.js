import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCharge } from "../actions";

/**
 * Component for adding a Charge to a Case.
 * It displays a button.  Once the button is clicked, a new charge is added to the redux state.
 * The new charge will then be at the bottom of the list of charges for this case, where the user can
 * enter its data.
 */
function AddCharge(props) {
    const { adder } = props;

    const handleClick = () => {
        adder();
    }

    return (
        <div className="addCharge" style={{marginTop: "15px", marginBottom: "10px"}}>
            <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>Add Charge</button>
        </div>
    );
}

AddCharge.propTypes = {
    /**
     * The callback which adds the charge to state.
     */
    adder: PropTypes.func.isRequired
}

function mapDispatchToProps(dispatch, ownProps) {
    return { adder: () => {
            dispatch(addCharge(ownProps.caseId));
        }
    };
};

const AddChargeWrapper = connect(null, mapDispatchToProps)(AddCharge);
export default AddChargeWrapper;