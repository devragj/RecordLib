import React from "react";
import Case from "./Case";

function Cases(props) {
    const casesStyle = {margin: '15px', padding: '10px', width: '900px'};
    const casesRendered = props.cases.map((caseObject, index) => {
            const id = caseObject.docket_number;
            return <Case {...caseObject} key={id} id={id}/>
        }
    );

    return (
        <div className="cases" style={casesStyle}>
            <h5>Cases</h5>
            {casesRendered}
        </div>
    );
}

export default Cases;