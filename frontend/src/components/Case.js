import React from "react";
import PropTypes from 'prop-types';
import Charge from "./Charge";
import ShowHideList from "./ShowHideList";

function Case(props) {
    const caseStyle = {display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px', border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px'};
    const { docket_number, otn, status, county, judge, arrest_date, disposition_date, charges } = props
    const chargesRendered = charges.map((charge, index) => {
            const charge_id = docket_number + 'Charge' + (index + 1).toString();
            return <Charge {...charge} key={charge_id} charge_id={charge_id}/>
        }
    );

    return (
        <div className="case" style={caseStyle}>
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
    docket_number: PropTypes.string,
    otn:  PropTypes.string,
    status:  PropTypes.string,
    county:  PropTypes.string,
    judge:  PropTypes.string,
    arrest_date:  PropTypes.string,
    disposition_date:  PropTypes.string,
    charges: PropTypes.array.isRequired
}

export default Case;