import React from "react";
import PropTypes from 'prop-types';

import ChargeHolderWrapper from "./ChargeHolder";
import AddChargeWrapper from "./AddCharge";
import ShowHideList from "./ShowHideList";


function Charges(props) {
    const chargesStyle = {gridColumn: "1 / 4"};
    const { charges, caseId, editing } = props;
    const chargesRendered = charges.map(chargeId => {
            return <ChargeHolderWrapper key={chargeId} chargeId={chargeId} editing={editing}/>
        }
    );

    if (editing) {
        const addChargeKey = caseId + 'addCharge';
        const addCharge = <AddChargeWrapper caseId={caseId} key={addChargeKey}/>
        chargesRendered.push(addCharge);
    };

    return (
        <div className="charges" style={chargesStyle}>
        {chargesRendered.length > 0 &&
           <ShowHideList hidden={!editing} title="Charges" list={chargesRendered} />
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

export default Charges;