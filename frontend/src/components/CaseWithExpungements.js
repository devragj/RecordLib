import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import ChargeWithExpungementsWrapper from "./ChargeWithExpungements";
import ShowHideList from "./ShowHideList";

function CaseWithExpungements(props) {
    const { id, docket_number, otn, status, county, judge, arrest_date, disposition_date, charges, hasExpungements, reasoning, type } = props;
    const caseStyle = { display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px',
        border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px' };
    const chargesRendered = charges.map( (chargeId, index) => {
            const reason = reasoning[index].reasoning;
            const isExpungeable = reasoning[index].value === 'True';
            return <ChargeWithExpungementsWrapper key={chargeId} chargeId={chargeId} reason={reason} isExpungeable={isExpungeable}/>
        }
    );

    return (
        <div className="case" id={id} style={caseStyle}>
            {hasExpungements?
                <div style={{color: 'blue'}}>{type}</div>
                : <div style={{color: 'blue'}}>No Expungement</div>
            }
            <div style={{gridColumn: "1 / 3"}}>Docket Number: {docket_number}</div>
            <div>OTN: {otn}</div>
            <div>Status: {status}</div>
            <div>County: {county}</div>
            <div>Judge: {judge}</div>
            <div>Arrest Date: {arrest_date}</div>
            <div>Disposition Date: {disposition_date}</div>
            {charges.length > 0 &&

                <div style={{gridColumn: "1 / 4"}}>
                        <ShowHideList hidden={true} title="Charges" list={chargesRendered} />
                </div>
           }
        </div>
    );
};

CaseWithExpungements.propTypes = {
    id: PropTypes.string,
    docket_number: PropTypes.string,
    otn:  PropTypes.string,
    status:  PropTypes.string,
    county:  PropTypes.string,
    judge:  PropTypes.string,
    arrest_date:  PropTypes.string,
    disposition_date:  PropTypes.string,
    charges: PropTypes.array.isRequired,
    hasExpungements: PropTypes.bool,
    type: PropTypes.string,
    reasoning: PropTypes.array
}

function mapStateToProps(state, ownProps) {
    return {...state.entities.cases[ownProps.caseId], ...state.analysis[ownProps.caseId]};
};

const CaseWithExpungementsWrapper = connect(mapStateToProps)(CaseWithExpungements);
export default CaseWithExpungementsWrapper;