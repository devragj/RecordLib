import React from "react";
import Charge from "./Charge";

function Case(props) {
    const caseStyle = {display: 'grid', gridTemplateColumns: '270px 270px 270px', margin: '10px', border: '1px solid black', borderRadius: '15px', padding: '10px', width: '860px'};
    const chargesRendered = props.charges.map((charge, index) => {
            const id = props.docket_number + 'Charge' + (index + 1).toString();
            return <Charge {...charge} key={id} id={id}/>
        }
    );

    return (
        <div className="case" style={caseStyle}>
            <div style={{gridColumn: "1 / 3"}}>Docket Number: {props.docket_number}</div>
            <div>OTN: {props.otn}</div>
            <div>Status: {props.status}</div>
            <div>County: {props.county}</div>
            <div>Judge: {props.judge}</div>
            <div>Arrest Date: {props.arrest_date}</div>
            <div>Disposition Date: {props.disposition_date}</div>
            {props.charges.length > 0 &&
                <div style={{gridColumn: "1 / 4"}}>
                    <h5>Charges</h5>
                    {chargesRendered}
                </div>
            }
        </div>
    );
};

export default Case;