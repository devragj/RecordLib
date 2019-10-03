import React from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

import ChargeWrapper from "./Charge";
import AddChargeWrapper from "./AddCharge";
import ShowHideList from "./ShowHideList";


function Charges(props) {
    const chargesStyle = {gridColumn: "1 / 4"};
    const { charges, caseId , editing } = props;
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
    charges: PropTypes.array.isRequired,
    caseId: PropTypes.string,
    editing:PropTypes.bool
}

function mapStateToProps(state, ownProps) {
    return { charges: state.entities.cases[ownProps.caseId].charges };
};

const ChargesWrapper = connect(mapStateToProps)(Charges);
export default ChargesWrapper;