import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCharge } from "../actions";
import EditChargeWrapper from "./EditCharge";

function AddCharge(props) {
    const { adder, chargeId } = props;
    const [adding, setAdding] = useState(false);

    const handleClick = () => {
        if (!adding) {
            adder();
        }

        setAdding(!adding);
    }

    return (
        <div className="addCharge" style={{marginTop: "15px", marginBottom: "10px"}}>
           <button type="button" style={{marginLeft: "20px"}} onClick={handleClick}>{adding? "Done Adding Charge": "Add Charge"}</button>
           { adding && <EditChargeWrapper chargeId={chargeId}/> }
        </div>
    );
}

AddCharge.propTypes = {
    chargeId: PropTypes.string.isRequired,
    /**
     * The callback which adds the charge to state.
     */
    adder: PropTypes.func.isRequired
}

function mapStateToProps(state, ownProps) {
    const index = ownProps.nextIndex - 1;
    const chargeId = ownProps.caseId + 'charges@' + index;
    return { chargeId };
};

function mapDispatchToProps(dispatch, ownProps) {
    const index = ownProps.nextIndex;
    const chargeId = ownProps.caseId + 'charges@' + index;
    return { adder: () => {
            dispatch(addCharge(chargeId, ownProps.caseId));
        }
    };
};

const AddChargeWrapper = connect(mapStateToProps, mapDispatchToProps)(AddCharge);
export default AddChargeWrapper;