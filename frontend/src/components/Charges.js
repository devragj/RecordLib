import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import ChargeWrapper from "./Charge";
import AddChargeWrapper from "./AddCharge";
import ShowHideList from "./ShowHideList";


function Charges(props) {
    const chargesStyle = {gridColumn: "1 / 4"};
    const { charges, caseId, editing } = props;
    const chargesRendered = charges.map(chargeId => {
            return <ChargeWrapper key={chargeId} chargeId={chargeId}/>
        }
    );

    return (
        <div className="charges" style={chargesStyle}>
        {editing &&
            <AddChargeWrapper caseId={caseId} nextIndex={charges.length} />
        }
        {charges.length > 0 &&
           <ShowHideList hidden={true} title="Charges" list={chargesRendered} />
        }
        </div>
    );
}

Charges.propTypes = {
    /**
        The list of charge ids.
    */
    charges: PropTypes.array.isRequired,
    /**
        The id of the case containing the charges.
    */
    caseId: PropTypes.string.isRequired,
    /**
        This component wil be used either in the Case component,
        in which case editing is false, or in the EditCase
        component, in which case editing is true.
    */
    editing: PropTypes.bool
}

function mapStateToProps(state, ownProps) {
    return { charges: state.entities.cases[ownProps.caseId].charges };
};

const ChargesWrapper = connect(mapStateToProps)(Charges);
export default ChargesWrapper;