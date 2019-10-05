import React, { useState }  from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import { addCharge } from "../actions";
import EditChargeWrapper from "./EditCharge";

/**
 * Component for adding a Charge to a Case.
 * It starts with a button.  Once the button is clicked, an id for the new charge
 * is generated and a charge with that id is added to the redux state.
 * The component then displays the EditCharge component, to enter the charge information.
 * Clicking the button (whose label has changed) again will hide the EditCharge component.
 */
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

/**
 * This function recreates the id of the newly-created charge, to pass to the EditCharge component.
 * @param  {Object} state    Redux state.
 * @param  {Object} ownProps
 * @param  {string} ownProps.caseId The id of the case to which
 * the charge is being added.
 * @param  {string} ownProps.index The length of the list of charges
 * of the containing case.
 * @return {Object}          Holds the generated chargeId.
 */
function mapStateToProps(state, ownProps) {
    // Since the chargeId generated by this function is used
    // by being passed to the EditCharge component after the
    // charge has been created, we need to subtract 1 from the
    // index so as to generate the correct id.
    const index = ownProps.nextIndex - 1;
    const chargeId = ownProps.caseId + 'charges@' + index;
    return { chargeId };
};

/**
 * This function constructs the id of the charge being created.
 * @param  {Object} dispatch    Redux dispatch.
 * @param  {Object} ownProps
 * @param  {string} ownProps.caseId The id of the case to which
 * the charge is being added.
 * @param  {string} ownProps.index The length of the list of charges
 * of the containing case.
 * @return {Object}          Holds the function which will store the
 * new charge in redux state.
 */
function mapDispatchToProps(dispatch, ownProps) {
    const index = ownProps.nextIndex;
    // This generates the id for the new charge,
    // using the id pattern which is used when normalizing
    // the starting CRecord.
    const chargeId = ownProps.caseId + 'charges@' + index;
    return { adder: () => {
            dispatch(addCharge(chargeId, ownProps.caseId));
        }
    };
};

const AddChargeWrapper = connect(mapStateToProps, mapDispatchToProps)(AddCharge);
export default AddChargeWrapper;