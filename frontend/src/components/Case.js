import React from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import ChargeWrapper from "./Charge";
import ShowHideList from "./ShowHideList";

function Case(props) {
    const { id, docket_number, otn, status, county, judge, arrest_date, disposition_date, charges } = props;
    const caseStyle = { display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px',
        border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px' };
    const chargesRendered = charges.map(chargeId => {
            return <ChargeWrapper key={chargeId} chargeId={chargeId}/>
        }
    );

    return (
        <div className="case" id={id} style={caseStyle}>
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

Case.propTypes = {
    id: PropTypes.string,
    docket_number: PropTypes.string,
    otn:  PropTypes.string,
    status:  PropTypes.string,
    county:  PropTypes.string,
    judge:  PropTypes.string,
    arrest_date:  PropTypes.string,
    disposition_date:  PropTypes.string,
    charges: PropTypes.array.isRequired
}

function mapStateToProps(state, ownProps) {
    return state.entities.cases[ownProps.caseId];
};

const CaseWrapper = connect(mapStateToProps)(Case);
export default CaseWrapper;